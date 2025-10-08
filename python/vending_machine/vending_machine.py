from drink import Drink
from suica import Suica

class VendingMachine:
    def __init__(self, initial_amount=0):
        self.__total_amount = initial_amount
        self.__inventory = {
            "ペプシ": [Drink("ペプシ", 150) for _ in range(5)]
        }
        
    @property
    def total_amount(self): 
        return self.__total_amount

    @property
    def inventory(self):
        return self.__inventory
    
    @total_amount.setter
    def total_amount(self, amount):
        # TODO: ↓setterでは原則代入しかしてはいけないのでsuicaクラスのように修正すること
        self.__total_amount += amount
    
    def get_stock(self, brand):
        return len(self.inventory[brand])
    
    def buy(self, selected_brand, suica):
        def decrease_stock(selecter_drink):
            """指定した銘柄の在庫を1本減らす"""
            selected_drink.pop()

        selected_drink = self.inventory[selected_brand]
        price = selected_drink[0].price

        if self.get_stock(selected_brand) > 0 and suica.balance >= price:
            decrease_stock(selected_drink)
            self.total_amount = price
            suica.pay(price)            
        

if __name__ == "__main__":
    print("=== VendingMachineクラス単体テスト ===")
    suica = Suica(1000)

    print("=== テスト完了 ===")
