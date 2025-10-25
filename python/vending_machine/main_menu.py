from vending_machine import VendingMachine
from drink_repository import SoldOutError, ProductNotFoundError
from suica import Suica, InvalidChargeAmountError, InsufficientBalanceError
from drink import Drink
from utils import console_style as cs
from utils import input_validator as iv
from collections import Counter
import sys


APP_NAME = "自販機シミュレーター"
CANCEL_GUIDE_MESSAGE = "※ Enter（空入力）または q でキャンセル。"
RETURN_PROMPT = "Enterで戻る > "
MSG_CANCELLED_TO_MENU = "キャンセルしました。"

class MainMenu:
    def __init__(self, vm: VendingMachine, suica: Suica):
        self.__is_running = True
        self.__vm = vm 
        self.__suica = suica
        self.__purchased_drinks: list[tuple[int, Drink]] = []
        
    def display(self):
        
        while self.__is_running:
            print(f"【{APP_NAME} メニュー】")
            print()
            print("1：Suicaの残高を確認する")
            print("2：Suicaにチャージする")
            print("3：全てのドリンクを表示する")
            print("4：購入可能なドリンクを表示する")
            print("5：ドリンクを購入する")
            print("6：ドリンクの在庫を補充する")
            print("7：自販機の売上金額を確認する")
            print("8：購入したドリンク一覧を確認する")
            print("0：終了")
            print()
            print("使用したい機能の番号を入力してください。")

            try:
                choice = iv.get_valid_int(lambda x: 0 <= x <= 8)
            except iv.CancelledInput:
                cs.print_line()
                continue

            print()
            actions = {
                1: self._show_suica_balance,
                2: self._charge_suica,
                3: self._show_all_drinks,
                4: self._show_parchasable_drinks,
                5: self._purchase_drink,
                6: self._restock_drink,
                7: self._show_sales,
                8: self._show_purchased_drinks,
                0: self._exit_progam,
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

    def _show_suica_balance(self):
        print(f"■現在のSuica残高：{self.__suica.balance}円")
    
    def _charge_suica(self):
        print("チャージ金額を数字で入力してください。")
        print(f"※ {Suica.MIN_CHARGE}円〜{Suica.MAX_BALANCE - self.__suica.balance}円までチャージ可能です。")
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

    def _show_all_drinks(self):
        inventory = self.__vm.get_brands()
        print("■商品一覧")

        for product_id, drink_info in inventory.items():
            brand, price, stock = drink_info
            print(f"[{product_id}] {brand}：{price}円 / 在庫数：{len(stock)}本")
            

    def _show_parchasable_drinks(self):
        available_brands = self.__vm.get_available_brands(self.__suica)
        
        if not available_brands:
            print("■現在購入可能な商品はありません。")
        else:
            print("■購入可能商品一覧")
            
            for product_id, drink_info in available_brands.items():
                brand, price, stock = drink_info
                print(f"[{product_id}] {brand}：{price}円 / 在庫数：{len(stock)}本")

        
    def _purchase_drink(self):
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

    def _restock_drink(self):

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
            return
            
    def _show_sales(self):
        print(f"■自販機の売上金額：{self.__vm.total_amount}円")
        
    def _show_purchased_drinks(self):
        """購入履歴を product_id ごとにまとめて表示する"""
        if not self.__purchased_drinks:
            print("■購入履歴はありません。")
            return

        print(f"■購入ドリンク一覧（商品ID順）")
        id_counts = Counter(pid for pid, _ in self.__purchased_drinks)
        for product_id in sorted(id_counts):
            drink = next(d for pid, d in self.__purchased_drinks if pid == product_id)
            count = id_counts[product_id]
            print(f"{product_id}：{drink.brand}（{count}本）")
            
    def _exit_progam(self):
        """アプリケーションを終了する"""
        print(f"{APP_NAME}を終了します。")
        print("よろしいでしょうか？ はい（y）/ いいえ（n）")
        try:
            yes = iv.get_valid_yes_no(
                lambda s: len(s) == 1 and s.lower() == "y"
            )
        except iv.CancelledInput:
            return True
        
        print()
        print("ご利用ありがとうございました。")
        sys.exit()
            

    #TODO: docstring、型ヒントなど追加。モジュールのディレクトリ仕分けすべきか。