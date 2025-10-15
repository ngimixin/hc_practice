from drink import Drink

class DuplicateProductError(Exception):
    """すでに販売中の商品を追加しようとしたときに発生する例外"""
    pass

class DrinkRepository:
    def __init__(self):
        self.__pk: int = 0
        self.__inventory: dict[int, Drink] = {}
        

    @property
    def pk(self):
        return self.__pk

    @property
    def inventory(self):
        return self.__inventory
    
    @pk.setter
    def pk(self, pk):
        self.__pk = pk
    
    def register_brand(self, brand: str, price: int, quantity: int):
        """商品を新規追加するメソッド"""
        
        # 一致するブランドが存在する場合の処理
        if any(brand == drink.brand for drink in self.inventory.values()):
            raise DuplicateProductError(f"{brand}は販売中の商品です。")
            
        self.pk += 1
        self.inventory[self.pk] = Drink(self.pk, brand, price, quantity)
