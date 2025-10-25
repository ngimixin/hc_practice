from __future__ import annotations
from drink_repository import DrinkRepository, SoldOutError
from drink import Drink
from suica import Suica

class VendingMachine:
    def __init__(self, repo: DrinkRepository, initial_amount=0):
        self.__total_amount = initial_amount
        self.__repo = repo

    @property
    def total_amount(self): 
        return self.__total_amount
    
    @total_amount.setter
    def total_amount(self, amount):
        self.__total_amount = amount

    def get_brands(self):
        """全ドリンク一覧を返す"""
        inventory = self.__repo.get_all()
        return inventory

    def get_available_brands(self, suica: Suica):
        """購入可能なドリンク一覧を返す（現在の残高で購入可能かつ在庫が1本以上あるドリンク）"""
        inventory = self.get_brands()
        available_brands = {}

        for product_id, drink_info in inventory.items():
            _, price, stock = drink_info
            if stock and suica.balance >= price:
                available_brands[product_id] = drink_info

        return available_brands

    def restock(self, product_id: int, quantity: int) -> None:
        """商品在庫を追加するメソッド"""
        self.__repo.increase_stock(product_id, quantity)

    def vend(self, product_id: int, suica: Suica) -> tuple[int, Drink]:
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
        
        self.total_amount += price
        return (product_id, drink)

#
# if __name__ == "__main__":
#     _debug()
#