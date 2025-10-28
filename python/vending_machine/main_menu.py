import sys
from collections import Counter

from vending_machine import VendingMachine
from drink_repository import SoldOutError, ProductNotFoundError
from suica import Suica, InvalidChargeAmountError, InsufficientBalanceError
from drink import Drink
from utils import console_style as cs
from utils import input_validator as iv


APP_NAME = "自販機シミュレーター"
CANCEL_GUIDE_MESSAGE = "※ Enter（空入力）または q でキャンセル。"
RETURN_PROMPT = "Enterで戻る > "
MSG_CANCELLED_TO_MENU = "キャンセルしました。"


class MainMenu:
    """コンソールUIのメインメニュー。

    自販機本体（VendingMachine）とSuicaを受け取り、
    ユーザー操作の入口となるクラス。
    """

    def __init__(self, vm: VendingMachine, suica: Suica) -> None:
        """依存を受け取って初期化する。

        Args:
            vm: 自販機本体（在庫管理・販売を担当）。
            suica: ユーザーのSuica（残高管理を担当）。
        """
        self.__is_running = True
        self.__vm = vm
        self.__suica = suica
        self.__purchased_drinks: list[tuple[int, Drink]] = []

    def display(self) -> None:
        """メインメニューを表示し、ループで入力を受け付ける。

        各ループの先頭で現在のSuica残高を表示する。
        """
        while self.__is_running:
            print(f"【{APP_NAME} メニュー】")
            self._show_suica_balance()
            print()
            print("1：Suicaにチャージする")
            print("2：全ドリンク一覧を表示する")
            print("3：購入可能なドリンクを表示する")
            print("4：ドリンクを購入する")
            print("5：ドリンクの在庫を補充する")
            print("6：自販機の売上金額を確認する")
            print("7：購入したドリンク一覧を確認する")
            print("0：終了")
            print()
            print("使用したい機能の番号を入力してください。")

            try:
                choice = iv.get_valid_int(lambda x: 0 <= x <= 7)
            except iv.CancelledInput:
                cs.print_line()
                continue

            print()
            actions = {
                1: self._charge_suica,
                2: self._show_all_drinks,
                3: self._show_purchasable_drinks,
                4: self._purchase_drink,
                5: self._restock_drink,
                6: self._show_sales,
                7: self._show_purchased_drinks,
                0: self._exit_program,
            }

            action = actions.get(choice)
            if action:
                # 入力キャンセル時用フラグ
                is_cancelled = action()
                print()
                if is_cancelled:
                    print(MSG_CANCELLED_TO_MENU)
                    cs.print_line()
                    print()
                    continue

            input(RETURN_PROMPT)
            cs.print_line()
            print()

    def _show_suica_balance(self) -> None:
        """現在のSuica残高を表示する。"""
        print(f"■現在のSuica残高：{self.__suica.balance}円")

    def _charge_suica(self) -> bool | None:
        """Suicaに金額をチャージする。

        Returns:
            True: 入力がキャンセルされた場合。
            None: 正常終了またはエラー表示時。
        """
        print("チャージ金額を数字で入力してください。")
        print(
            f"※ {Suica.MIN_CHARGE}円〜"
            f"{Suica.MAX_BALANCE - self.__suica.balance}円までチャージ可能です。"
        )
        print(CANCEL_GUIDE_MESSAGE)

        try:
            amount = iv.get_valid_int(lambda x: x > 0)
        except iv.CancelledInput:
            return True

        try:
            self.__suica.charge(amount)
            print()
            print(f"■{amount}円をチャージしました。")
        except InvalidChargeAmountError as e:
            print()
            print(e)
            return

        self._show_suica_balance()

    def _show_all_drinks(self) -> None:
        """自販機で取り扱っている全ドリンクを一覧表示する。

        在庫数が0本の商品や、Suica残高では購入できない商品も含めて表示する。
        """
        inventory = self.__vm.get_brands()
        print("■商品一覧")

        for product_id, drink_info in inventory.items():
            brand, price, stock = drink_info
            print(f"[{product_id}] {brand}：{price}円 / 在庫数：{len(stock)}本")

    def _show_purchasable_drinks(self) -> None:
        """現在のSuica残高で購入可能なドリンクのみを一覧表示する。

        在庫が1本以上あり、かつSuica残高が価格以上の商品を抽出して表示する。
        """
        available_brands = self.__vm.get_available_brands(self.__suica)

        if not available_brands:
            print("■現在購入可能な商品はありません。")
        else:
            print("■購入可能商品一覧")

            for product_id, drink_info in available_brands.items():
                brand, price, stock = drink_info
                print(f"[{product_id}] {brand}：{price}円 / 在庫数：{len(stock)}本")

    def _purchase_drink(self) -> bool | None:
        """ドリンク購入処理を実行する。

        Returns:
            True: 入力がキャンセルされた場合。
            None: 正常終了またはエラー表示時。
        """
        self._show_all_drinks()
        print()

        print("購入したい商品の番号を入力してください。")
        print(CANCEL_GUIDE_MESSAGE)

        try:
            product_id = iv.get_valid_int(lambda x: x > 0)
        except iv.CancelledInput:
            return True

        try:
            product_id, drink = self.__vm.vend(product_id, self.__suica)
        except ProductNotFoundError as e:
            print()
            print(e)
            return
        except InsufficientBalanceError as e:
            print()
            print(e)
            return
        except SoldOutError as e:
            print()
            print(e)
            return
        else:
            print()
            print(f"■{drink.brand}を購入しました。")
            self.__purchased_drinks.append((product_id, drink))
            self._show_suica_balance()

    def _restock_drink(self) -> bool | None:
        """指定された商品を補充する。

        Returns:
            True: 入力がキャンセルされた場合。
            None: 正常終了またはエラー表示時。
        """
        try:
            print("補充したい商品の番号を入力してください。")
            print(CANCEL_GUIDE_MESSAGE)
            print()
            self._show_all_drinks()
            product_id = iv.get_valid_int(lambda x: x > 0)
            print()
            print("補充する数を入力してください。")
            print(CANCEL_GUIDE_MESSAGE)
            quantity = iv.get_valid_int(lambda x: x > 0)
        except iv.CancelledInput:
            return True

        try:
            self.__vm.restock(product_id, quantity)
        except ProductNotFoundError as e:
            print()
            print(e)
            return
        else:
            inventory = self.__vm.get_brands()
            brand = inventory[product_id][0]
            print()
            print(f"■{brand}を{quantity}本補充しました。")

    def _show_sales(self) -> None:
        """自販機の売上金額を表示する。"""
        print(f"■自販機の売上金額：{self.__vm.total_amount}円")

    def _show_purchased_drinks(self) -> None:
        """購入履歴を product_id ごとに集計して表示する。"""
        if not self.__purchased_drinks:
            print("■購入履歴はありません。")
            return

        print("■購入ドリンク一覧（商品ID順）")
        id_counts = Counter(pid for pid, _ in self.__purchased_drinks)
        for product_id in sorted(id_counts):
            drink = next(d for pid, d in self.__purchased_drinks if pid == product_id)
            count = id_counts[product_id]
            print(f"{product_id}：{drink.brand}（{count}本）")

    def _exit_program(self) -> bool | None:
        """アプリケーションを終了する（確認付き）。

        Returns:
            True: 入力がキャンセルされた場合（終了せずメニューに戻る）。
            None: 終了が確定した場合（システム終了）。
        """
        print(f"{APP_NAME}を終了します。")
        print("よろしいでしょうか？ はい（y）/ いいえ（n）")
        try:
            iv.get_valid_yes_no(lambda s: len(s) == 1 and s.lower() == "y")
        except iv.CancelledInput:
            return True

        print()
        print("ご利用ありがとうございました。")
        sys.exit()
