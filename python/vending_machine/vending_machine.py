from __future__ import annotations
from drink import Drink
from suica import Suica
from drink_repository import DrinkRepository

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
    def __init__(self, initial_amount=0):
        self.__total_amount = initial_amount
        self.__repo = DrinkRepository()

    @property
    def total_amount(self): 
        return self.__total_amount
    
    @total_amount.setter
    def total_amount(self, amount):
        self.__total_amount = amount

    def restock(self, product_id: int, quantity: int) -> None:
        """商品在庫を追加するメソッド"""

        self.__repo.increase_stock(product_id, quantity)

    def vend(self, product_id: int, suica: Suica) -> Drink:
        """商品を一本購入するメソッド"""
        
        _, price, _ = self.__repo.inventory[product_id]

        # 残高不足時はInsufficientBalanceErrorが自動伝播
        suica.pay(price)

        try:
            drink = self.__repo.decrease_stock(product_id)
        except SoldOutError as e:
            # 返金処理（内部的にはチャージと同義）
            suica.charge(price) 
            raise e

        return drink
 
    # def get_stock(self, target_brand_num: int) -> int:
    #     """指定銘柄の在庫数を返す。
    #
    #     Args:
    #         target_brand_num (int): 在庫数を確認する銘柄。
    #
    #     Returns:
    #         int: 在庫本数。
    #
    #     Raises:
    #         UnknownBrandError: 取り扱っていない銘柄の場合。
    #     """
    #
    #     catalog_list = list(self.catalog.keys())
    #     target_brand = catalog_list[target_brand_num]
    #
    #     if target_brand not in self.catalog:
    #         raise UnknownBrandError(f"{target_brand}は扱っていません。")
    #     return self.inventory[target_brand]
    
    # def buy(self, target_brand_num: int, suica: Suica):
    #     """指定ブランドの飲料を購入する。
    #
    #     在庫がない場合は `SoldOutError` を送出する。残高不足など決済に
    #     失敗した場合は `suica.pay` が例外を送出する想定（自販機側では捕捉しない）。
    #
    #     Args:
    #         target_brand_num (int): 購入する銘柄。
    #         suica (Suica): 決済に使用するSuicaインスタンス。
    #
    #     Returns:
    #         Drink: 排出されたドリンクインスタンス。
    #
    #     Raises:
    #         SoldOutError: 指定銘柄の在庫がない場合。
    #         UnknownBrandError: 取り扱っていない銘柄を選択した場合。
    #         InsufficientBalanceError: 残高不足により決済できない場合。
    #     """
    #
    #     catalog_list = list(self.catalog.keys())
    #     target_brand = catalog_list[target_brand_num]
    #
    #     if target_brand_num not in self.inventory:
    #         raise UnknownBrandError(f"{target_brand_num}は扱っていません。")
    #
    #     drinks = self.inventory[target_brand_num]
    #     if not drinks:
    #         raise SoldOutError(f"{target_brand_num}は在庫切れです。")
    #     
    #     price = self.catalog[target_brand].price
    #     suica.pay(price)
    #     self.total_amount = self.total_amount + price
    #     
    #     drinks -+ 1


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