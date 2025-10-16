from drink import Drink
from collections import deque

class SoldOutError(Exception):
    """指定した商品が売り切れのときに発生する例外"""
    pass

class DrinkRepository:
    def __init__(self):
        seeds = [
            (1, "ペプシ",   150, 5),
            (2, "モンスター", 230, 5),
            (3, "いろはす", 120, 5),
        ]
        # product_idごとに [brand, price, drinks] を格納する
        self.__inventory: dict[int, list] = {
            product_id: [brand, price, deque(Drink(brand, price) for _ in range(quantity))]
            for product_id, brand, price, quantity in seeds
        }

    @property
    def inventory(self) -> dict[int, list]:
        return self.__inventory
    
    def get_all(self) -> dict[int, list]:
        """取扱商品一覧を取得するメソッド"""
        return self.inventory.copy()
    
    def increase_stock(self, product_id: int, quantity: int) -> None:
        """指定された商品の在庫を quantity 本追加する"""
        
        brand, price, drinks = self.inventory[product_id]
        drinks.extend(Drink(brand, price) for _ in range(quantity))
    
    def decrease_stock(self, product_id: int) -> Drink:
        """指定された商品の在庫を1本減らす"""
        
        brand, _, drinks = self.inventory[product_id]
        if not drinks:
            raise SoldOutError(f"{brand}は売り切れです。")
        
        return drinks.popleft()
    
