class Suica:
    DEPOSIT = 500

    def __init__(self, balance = 0):
        self.__balance = balance

    # 内部用
    @property
    def balance(self):
        return self.__balance
    
    # 内部用
    @balance.setter
    def balance(self, amount):
        self.__balance += amount

    def charge(self, amount):
        MIN_AMOUNT = 100
        MAX_AMOUNT = 20000

        if amount < MIN_AMOUNT:
            print(f"{MIN_AMOUNT}円以上の額をチャージして下さい。")
        elif (self.balance + amount) > MAX_AMOUNT:
            print(f"チャージ上限額（{MAX_AMOUNT}円）を超えています。")
        else:
            print(f"{amount}円チャージしました。")
            self.balance = amount

if __name__ == "__main__":
    print("=== Suicaクラス単体テスト ===")
    suica = Suica()
    print("Suica初期残高:", suica.balance)

    suica.charge(100)
    print("チャージ後のSuica残高:", suica.balance)
    print("=== テスト完了 ===")