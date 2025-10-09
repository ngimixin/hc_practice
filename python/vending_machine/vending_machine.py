from __future__ import annotations
from drink import Drink
from suica import Suica, InvalidChargeAmountError, InsufficientBalanceError

class SoldOutError(Exception):
    """在庫切れのときに発生する例外"""
    pass

class UnknownBrandError(Exception):
    """取り扱っていない銘柄を選択した場合に発生する例外"""
    pass

class VendingMachine:
    def __init__(self, initial_amount=0):
        self.__total_amount = initial_amount
        self.__inventory = {
            "ペプシ": [Drink("ペプシ", 150) for _ in range(5)]
        }

    @property
    def total_amount(self): 
        return self.__total_amount

    @property
    def inventory(self):
        return self.__inventory
    
    @total_amount.setter
    def total_amount(self, amount):
        """自販機全体の売上金額を設定するSetter。

        このSetterは「単純な代入のみ」を行う。加算などの演算処理は、
        呼び出し元（例：buyメソッド）で実行する設計としている。

        これはSetterが本来持つ「値をセットするだけの責務」を保ち、
        副作用を避けるため。また、Suicaクラスと同じ設計方針で
        状態管理の一貫性を保つ目的がある。

        Args:
            amount (int): 売上金額として設定する値。
        """
        self.__total_amount = amount
    
    def get_stock(self, brand: str) -> int:
        """指定銘柄の在庫数を返す。

        Args:
            brand (str): 在庫数を確認する銘柄。

        Returns:
            int: 在庫本数。

        Raises:
            UnknownBrandError: 取り扱っていない銘柄の場合。
        """
        if brand not in self.inventory:
            raise UnknownBrandError(f"{brand}は扱っていません。")
        return len(self.inventory[brand])
    
    def buy(self, selected_brand: str, suica: Suica) -> Drink:
        """指定ブランドの飲料を購入する。

        在庫がない場合は `SoldOutError` を送出する。残高不足など決済に
        失敗した場合は `suica.pay` が例外を送出する想定（自販機側では捕捉しない）。

        Args:
            selected_brand (str): 購入する銘柄。
            suica (Suica): 決済に使用するSuicaインスタンス。

        Returns:
            Drink: 排出されたドリンクインスタンス。

        Raises:
            SoldOutError: 指定銘柄の在庫がない場合。
            UnknownBrandError: 取り扱っていない銘柄を選択した場合。
            InsufficientBalanceError: 残高不足により決済できない場合。
        """

        if selected_brand not in self.inventory:
            raise UnknownBrandError(f"{selected_brand}は扱っていません。")

        drinks = self.inventory[selected_brand]
        if not drinks:
            raise SoldOutError(f"{selected_brand}は在庫切れです。")
        
        price = drinks[0].price
        suica.pay(price)     
        selected_drink = drinks.pop()
        self.total_amount = self.total_amount + price
        return selected_drink       
        

def _debug():
    """簡易スモークテスト"""
    print("=== VendingMachineクラス単体テスト ===")

    suica = Suica(1000)
    ven = VendingMachine()

    bought = ven.buy("ペプシ", suica)
    print(bought)
    print(repr(bought))
    print("在庫:", ven.get_stock("ペプシ"))

    # 在庫が尽きるまで買ってみる
    while True:
        try:
            # suica.charge(20000)
            bought = ven.buy("ペプシ", suica)
            print(f"{bought}を購入。残高:{suica.balance}")
        except (UnknownBrandError, SoldOutError, InvalidChargeAmountError, InsufficientBalanceError) as e:
            print(e)
            break

    print("=== テスト完了 ===")


if __name__ == "__main__":
    _debug()


