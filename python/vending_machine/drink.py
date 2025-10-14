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
    def price(self, new_price):
        self.__price = new_price 

    def __str__(self):
        return f"{self.brand}"

    def __repr__(self):
        return f"Drink(brand={self.brand!r}, price={self.price!r})"
