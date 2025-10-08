class Drink:
    def __init__(self, brand, price):
        self.__brand = brand
        self.__price = price
        
    @property
    def brand(self):
        return self.__brand
    
    @property
    def price(self):
        return self.__price
    
    # デバッグ用
    def __str__(self):
        return f"{self.brand}（{self.price}円）"