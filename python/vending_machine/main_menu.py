from vending_machine import VendingMachine
from suica import Suica, InvalidChargeAmountError, InsufficientBalanceError
from utils.console_style import ConsoleStyle
from utils.input_validator import InputValidator

class MainMenu:
    def __init__(self):
        self.__is_running = True
        self.__ven = VendingMachine()
        self.__suica = Suica()
        
    def display_main_menu(self):
        
        while self.__is_running:
            print("自販機メニュー")
            print()
            
            print("使用したい機能を選んでください：")
            print("1：Suicaの残高を確認する")
            print("2：Suicaにチャージする")
            print("3：購入可能なドリンクを表示する")
            print("4：全てのドリンクを表示する")
            print("5：ドリンクを購入する")
            print("6：ドリンクの在庫を補充する")
            print("7：売上金額を確認する")
            print("0：終了")
            
            
            choice = InputValidator.get_valid_int(
                "> ",
                lambda x: 0 <= x <= 7
                )
            print()
            
            actions = {
                1: self._show_suica_balance,
                2: self._charge_suica,
                3: self._show_parchasable_drinks,
                4: self._show_all_drinks,
                5: self._purchase_drink,
                6: self._restock_drink,
                7: self._show_sales,
                0: self._exit_progam,
            }
            
            action = actions.get(choice)
            if action:
                action()
            print()

    def _show_suica_balance(self):
        print(self.__suica.balance)
        
    def _charge_suica(self):
        amount = InputValidator.get_valid_int(
            "> ",
            lambda x: x > 0
            )
        
        try:
            self.__suica.charge(amount)
            print(f"{amount}円をチャージしました。")
        except InvalidChargeAmountError as e:
            print(e)
            
        ConsoleStyle.print_line()
