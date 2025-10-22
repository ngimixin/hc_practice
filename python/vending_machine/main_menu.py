from vending_machine import VendingMachine
from suica import Suica, InvalidChargeAmountError, InsufficientBalanceError
from utils import console_style as cs
from utils import input_validator as iv

MSG_CANCELLED_TO_MENU = "キャンセルしました。メインメニューに戻ります。"
CANCEL_GUIDE_MESSAGE = "※ Enter（空入力）または q でキャンセルしてメインメニューに戻れます。"

class MainMenu:
    def __init__(self, vm: VendingMachine, suica: Suica):
        self.__is_running = True
        self.__vm = vm 
        self.__suica = suica
        
    def display(self):
        
        while self.__is_running:
            print("【メニュー】")
            print()
            print("1：Suicaの残高を確認する")
            print("2：Suicaにチャージする")
            print("3：購入可能なドリンクを表示する")
            print("4：全てのドリンクを表示する")
            print("5：ドリンクを購入する")
            print("6：ドリンクの在庫を補充する")
            print("7：売上金額を確認する")
            print("8：購入したドリンク一覧を確認する")
            print("0：終了")
            print()
            print("使用したい機能の番号を入力してください。")
            choice = iv.get_valid_int(lambda x: 0 <= x <= 7, False)
            print()
            
            actions = {
                1: self._show_suica_balance,
                2: self._charge_suica,
                # 3: self._show_parchasable_drinks,
                # 4: self._show_all_drinks,
                # 5: self._purchase_drink,
                # 6: self._restock_drink,
                # 7: self._show_sales,
                # 8: self._show_purchased_drinks
                # 0: self._exit_progam,
            }
            
            action = actions.get(choice)
            if action:
                action()
            print()

    def _show_suica_balance(self):
        print(self.__suica.balance)
        cs.print_line()
        
    def _charge_suica(self):
        print("チャージ金額を数字で入力してください。")
        print(f"※ {Suica.MIN_CHARGE}円〜{Suica.MAX_BALANCE - self.__suica.balance}円までチャージ可能です。")
        print(CANCEL_GUIDE_MESSAGE)
        
        try:
            amount = iv.get_valid_int(lambda x: x > 0)
        except iv.CancelledInput:
            print(MSG_CANCELLED_TO_MENU)
            cs.print_line()
            return
            
        try:
            self.__suica.charge(amount)
            print(f"{amount}円をチャージしました。")
        except InvalidChargeAmountError as e:
            print(e)
            
        print(f"現在のSuica残高：{self.__suica.balance}")
        cs.print_line()
