from __future__ import annotations
from drink import Drink
from suica import Suica
from drink_repository import DrinkRepository

class SoldOutError(Exception):
    """在庫切れのときに発生する例外"""
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

    def get_brands(self):
        """全ドリンク一覧を返す"""
        
        inventory = self.__repo.get_all()
        brands = []

        for brand, price, stock in inventory.values():
            brands.append((brand, price, stock))
                
        return brands

    def get_available_brands(self):
        """購入可能なドリンク一覧を返す（現在の残高で購入可能かつ在庫が1本以上あるドリンク）"""
        
        brands = self.get_brands()
        available_brands = []
        
        for brand, price, stock in brands:
            if stock and self.total_amount >= price:
                available_brands.append((brand, price))
        
        return available_brands
    


    def restock(self, product_id: int, quantity: int) -> None:
        """商品在庫を追加するメソッド"""

        self.__repo.increase_stock(product_id, quantity)

    def vend(self, product_id: int, suica: Suica) -> Drink:
        """商品を一本購入するメソッド"""
        
        price = self.__repo.get_price(product_id)

        # 残高不足時はInsufficientBalanceErrorが自動伝播
        suica.pay(price)

        try:
            drink = self.__repo.decrease_stock(product_id)
        except SoldOutError as e:
            # 返金処理（内部的にはチャージと同義）
            suica.charge(price) 
            raise e

        return drink



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