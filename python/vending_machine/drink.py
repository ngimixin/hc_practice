class Drink:
    def __init__(self, brand: str, price: int, quantity: int):
        self.__pk = None
        self.__brand = brand
        self.__price = price
        self.__quantity = quantity
        
    @property
    def pk(self):
        return self.__pk

    @property
    def brand(self):
        return self.__brand
    
    @property
    def price(self):
        return self.__price
    
    @property
    def quantity(self):
        return self.__quantity
    
    @price.setter
    def price(self, price):
        self.__price = price 
        
    @quantity.setter
    def quantity(self, quantity):
        self.__quantity = quantity
        
    @pk.setter
    def pk(self, pk):
        self.__pk = pk

    def __repr__(self):
        return f"Drink(pk={self.pk}, brand={self.brand!r}, price={self.price}, quantity={self.quantity})"
