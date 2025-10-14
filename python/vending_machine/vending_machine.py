from __future__ import annotations
from drink import Drink
from suica import Suica, InvalidChargeAmountError, InsufficientBalanceError

class SoldOutError(Exception):
    """在庫切れのときに発生する例外"""
    pass

class UnknownBrandError(Exception):
    """取り扱っていない銘柄を選択した場合に発生する例外"""
    pass

class DuplicateProductError(Exception):
    """すでに販売中の商品を追加しようとしたときに発生する例外"""
    pass

class VendingMachine:
    def __init__(self, initial_amount=0, initial_brand="ペプシ", initial_price=150, initial_quantity=5):
        self.__total_amount = initial_amount
        # 取扱商品一覧辞書。0番はダミー
        self.__catalog: dict[str, Drink | None] = {"0": None, initial_brand: Drink(initial_brand, initial_price)}

        # 商品在庫数辞書
        self.__inventory: dict[str, int] = {initial_brand:initial_quantity}

    @property
    def total_amount(self): 
        return self.__total_amount

    @property
    def inventory(self):
        return self.__inventory
    
    @property 
    def catalog(self):
        return self.__catalog
    
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

    # def register_brand(self, target_brand: str, price: int, quantity: int):
    #     """商品を新規追加するメソッド"""
    #     
    #     if target_brand in self.catalog:
    #         raise DuplicateProductError(f"{target_brand}は販売中の商品です。")
    #     
    #     self.catalog.update({target_brand: Drink(target_brand, price)})
    #     self.inventory.update({target_brand: quantity})

    def add_stock(self, target_brand_num: int, quantity: int):
        """商品在庫を追加するメソッド"""

        catalog_list = list(self.catalog.keys())
        target_brand = catalog_list[target_brand_num]
        self.inventory.update({target_brand: self.inventory[target_brand] + quantity})

    
    def get_brand_names(self):
        """購入可能商品のみを取得するメソッド"""
        return self.catalog
 
    def get_stock(self, target_brand_num: int) -> int:
        """指定銘柄の在庫数を返す。

        Args:
            target_brand_num (int): 在庫数を確認する銘柄。

        Returns:
            int: 在庫本数。

        Raises:
            UnknownBrandError: 取り扱っていない銘柄の場合。
        """

        catalog_list = list(self.catalog.keys())
        target_brand = catalog_list[target_brand_num]

        if target_brand not in self.catalog:
            raise UnknownBrandError(f"{target_brand}は扱っていません。")
        return self.inventory[target_brand]
    
    def buy(self, target_brand_num: int, suica: Suica):
        """指定ブランドの飲料を購入する。

        在庫がない場合は `SoldOutError` を送出する。残高不足など決済に
        失敗した場合は `suica.pay` が例外を送出する想定（自販機側では捕捉しない）。

        Args:
            target_brand_num (int): 購入する銘柄。
            suica (Suica): 決済に使用するSuicaインスタンス。

        Returns:
            Drink: 排出されたドリンクインスタンス。

        Raises:
            SoldOutError: 指定銘柄の在庫がない場合。
            UnknownBrandError: 取り扱っていない銘柄を選択した場合。
            InsufficientBalanceError: 残高不足により決済できない場合。
        """

        catalog_list = list(self.catalog.keys())
        target_brand = catalog_list[target_brand_num]

        if target_brand_num not in self.inventory:
            raise UnknownBrandError(f"{target_brand_num}は扱っていません。")

        drinks = self.inventory[target_brand_num]
        if not drinks:
            raise SoldOutError(f"{target_brand_num}は在庫切れです。")
        
        price = self.catalog[target_brand].price
        suica.pay(price)
        self.total_amount = self.total_amount + price
        
        drinks -+ 1


# def _debug():
#     """簡易スモークテスト"""
#     print("=== VendingMachineクラス単体テスト ===")
#
#     suica = Suica(1000)
#     ven = VendingMachine()
#
#     ven.add_drink("ペプシ", 150, )
#     print("[DEBUG]", ven.inventory)
#
#     bought = ven.buy("ペプシ", suica)
#     print(bought)
#     print(repr(bought))
#     print("在庫:", ven.get_stock("ペプシ"))
#
#     # 在庫が尽きるまで買ってみる
#     while True:
#         try:
#             # suica.charge(20000)
#             bought = ven.buy("ペプシ", suica)
#             print(f"{bought}を購入。残高:{suica.balance}")
#         except (UnknownBrandError, SoldOutError, InvalidChargeAmountError, InsufficientBalanceError) as e:
#             print(e)
#             break
#
#     # ven.get_brand_names()
#     print("[DEBUG]", ven.inventory)
#
#     print("=== テスト完了 ===")
#
#
# if __name__ == "__main__":
#     _debug()
#
#
#