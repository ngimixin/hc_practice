from drink import Drink
from typing import TypedDict

class DuplicateProductError(Exception):
    """すでに販売中の商品を追加しようとしたときに発生する例外"""
    pass

class StockRecord(TypedDict):
    drink: Drink
    quantity: int
    is_active: bool

class DrinkRepository:
    __pk: int = 0

    @classmethod
    def current_pk(cls) -> int:
        """現在の採番番号を返す（読み取り専用）"""
        return cls.__pk
    
    def __init__(self):
        self.__inventory: dict[int, StockRecord] = {}
        

    @property
    def inventory(self):
        return self.__inventory
    
    
    def register_brand(self, target_brand:str, price: int, add_quantity: int):
        """商品を新規追加するメソッド"""
        
        def _allocate_pk():
            DrinkRepository.__pk += 1
            return DrinkRepository.__pk

        for brand_data in self.inventory.values():
            if target_brand == brand_data["drink"].brand:
                raise DuplicateProductError(f"{target_brand}は販売中の商品です。")
            
        self.inventory.update({_allocate_pk(): {"drink": Drink(target_brand, price), "quantity": add_quantity, "is_active": True}})