class InvalidChargeAmountError(ValueError):
    """Suicaのチャージ額の範囲外を表す例外"""
    
    def __init__(self, amount: int, balance: int, message: str):
        self.amount = amount
        self.balance = balance
        super().__init__(message)
    
    def __str__(self):
        return f"{self.args[0]}（入金額: {self.amount}円 / 残高: {self.balance}円）"
class InsufficientBalanceError(ValueError):
    """Suicaの残高不足を表す例外"""

    def __init__(self, required_amount: int, balance: int, message: str):
        self.required_amount = required_amount
        self.balance = balance
        super().__init__(message)

    def __str__(self):
        return f"{self.args[0]}（必要額: {self.required_amount}円 / 残高: {self.balance}円）"
class Suica:
    # デポジット500円は定義しているがSuica残高とは別ものなので今回未使用
    DEPOSIT = 500
    MIN_CHARGE = 100
    MAX_BALANCE = 20000

    def __init__(self, balance=0):
        # 生成時の保証：初期値の妥当性
        if balance < 0 or balance > self.MAX_BALANCE:
            raise ValueError("不正な初期残高です。")
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, new_value):
        self.__balance = new_value

    def charge(self, amount):
        self._update_balance(amount)

    def pay(self, amount):
        self._update_balance(-amount)

    def _update_balance(self, amount):
        # チャージ処理
        if amount >= 0:
            if amount < self.MIN_CHARGE:
                raise InvalidChargeAmountError(amount, self.balance, f"{self.MIN_CHARGE}円以上の額をチャージして下さい。")
            new_balance = self.balance + amount
            if new_balance > self.MAX_BALANCE:
                raise InvalidChargeAmountError(amount, self.balance, f"チャージ上限額（{self.MAX_BALANCE}円）を超えています。")
            self.balance = new_balance
        # 支払い処理
        else:
            required_amount = -amount
            if required_amount > self.balance:
                raise InsufficientBalanceError(required_amount, self.balance, f"残高不足です。")
            self.balance = self.balance + amount


if __name__ == "__main__":
    print("=== Suicaクラス単体テスト ===")
    suica = Suica()
    print("Suica初期残高:", suica.balance)

    suica.charge(1000)
    print("チャージ後のSuica残高:", suica.balance)

    suica.pay(1100)
    print("支払い後のSuica残高:", suica.balance)
    print("=== テスト完了 ===")
