from datetime import datetime
from typing import Optional

class Drink:
    """ブランドごとの管理情報"""
    def __init__(
            self,
            brand: str,
            price: int,
            active: bool = True,
            discontinued_at: Optional[datetime] = None):
        self.__brand = brand
        self.__price = price
        self.__active = True
        self.__created_at = datetime.now()
        self.__discontinued_at = discontinued_at
        
    @property
    def brand(self):
        return self.__brand
    
    @property
    def price(self):
        return self.__price
    
    
    @property
    def active(self):
        return self.__active
    
    @property
    def created_at(self):
        return self.__created_at
    
    @property
    def discontinued_at(self):
        return self.__discontinued_at

    @price.setter
    def price(self, new_price):
        self.__price = new_price 

    @active.setter
    def active(self, flag):
        self.__active = flag
        
    @discontinued_at.setter
    def discontinued_at(self, discontinued_datetime):
        self.__discontinued_at = discontinued_datetime
    
    def discontinue(self) -> None:
        """販売停止にする"""
        self.active = False
        self.discontinued_at = datetime.now()

    def __str__(self):
        return f"{self.brand}"

    def __repr__(self):
        return f"Drink(brand={self.brand!r}, price={self.price!r})"
