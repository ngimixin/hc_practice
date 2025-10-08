import drink


class VendingMachine:
    def __init__(self):
        self.__inventory = {
            "ペプシ": [drink.Drink("ペプシ", 150) for _ in range(5)]
        }

    @property
    def inventory(self):
        return self.__inventory
    
    def get_stock(self, brand):
        return len(self.inventory[brand])

if __name__ == "__main__":
    print("=== VendingMachineクラス単体テスト ===")
    ven = VendingMachine()
    
    print("ペプシの在庫数:", ven.get_stock("ペプシ"))
    print("=== テスト完了 ===")
