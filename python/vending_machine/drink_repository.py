from drink import Drink

class SoldOutError(Exception):
    """指定した商品が売り切れのときに発生する例外"""
    pass
class DuplicateProductError(Exception):
    """すでに販売中の商品を追加しようとしたときに発生する例外"""
    pass

class DrinkRepository:
    def __init__(self):
        self.__pk: int = 0
        self.__inventory: dict[int, Drink] = {}
        
    @property
    def pk(self) -> int:
        return self.__pk

    @property
    def inventory(self) -> dict[int, Drink]:
        return self.__inventory
    
    def get_all(self) -> dict[int, Drink]:
        """取扱商品一覧を取得するメソッド"""
        return self.inventory.copy()
    
    def increase_stock(self, pk: int, quantity: int) -> None:
        """指定された商品の在庫をX本追加する"""
        
        drink = self.inventory[pk]
        drink.quantity += quantity
    
    def decrease_stock(self, pk: int) -> None:
        """指定された商品の在庫を1本減らす"""
        
        drink = self.inventory[pk]
        
        if drink.quantity == 0:
            raise SoldOutError(f"{drink.brand}は売り切れです。")
        
        drink.quantity -= 1
    
    def add(self, brand: str, price: int, quantity: int) -> None:
        """商品を新規追加するメソッド"""
        
        if self._exists_by_brand(brand):
            # 一致するブランドが存在する場合
            raise DuplicateProductError(f"{brand}は販売中の商品です。")
            
        self.__pk += 1
        self.inventory[self.__pk] = Drink(self.__pk, brand, price, quantity)
        
    def _exists_by_brand(self, brand: str) -> bool:
        """指定したブランドの商品がすでに登録済みかを判定"""
        return any(brand == drink.brand for drink in self.inventory.values())
