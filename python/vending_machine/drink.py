class Drink:
    def __init__(self, brand: str, price: int):
        self.__brand = brand
        self.__price = price
        
    @property
    def brand(self):
        return self.__brand
    
    @property
    def price(self):
        return self.__price
    
    @price.setter
    def price(self, price):
        self.__price = price 
        

    def __repr__(self):
        return f"Drink(brand={self.brand!r}, price={self.price})"
