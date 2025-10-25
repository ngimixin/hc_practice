from drink import Drink
from collections import deque

class SoldOutError(Exception):
    """指定した商品が売り切れのときに発生する例外"""

class ProductNotFoundError(KeyError):
    """指定された商品IDが存在しない場合に発生する例外"""
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"■商品ID：{product_id} は存在しません。")

    def __str__(self) -> str:
        return self.args[0]

class DrinkRepository:
    def __init__(self, inventory: dict[int, list]):
        self.__inventory = inventory
    
    def get_all(self) -> dict[int, list]:
        """取扱商品一覧を取得するメソッド"""
        return self.__inventory.copy()
    
    def get_price(self, product_id: int) -> int:
        """商品価格を取得するメソッド"""
        # 存在しない product_id を指定したらエラー
        if product_id not in self.__inventory:
            raise ProductNotFoundError(product_id)

        return self.__inventory[product_id][1]
    
    def increase_stock(self, product_id: int, quantity: int) -> None:
        """指定された商品の在庫を quantity 本追加する"""
        # 存在しない product_id を指定したらエラー
        if product_id not in self.__inventory:
            raise ProductNotFoundError(product_id)

        brand, price, drinks = self.__inventory[product_id]
        drinks.extend(Drink(brand, price) for _ in range(quantity))
    
    def decrease_stock(self, product_id: int) -> Drink:
        """指定された商品の在庫を1本減らす"""
        brand, _, drinks = self.__inventory[product_id]
        if not drinks:
            raise SoldOutError(f"■{brand}は売り切れです。")
        
        return drinks.popleft()
    
