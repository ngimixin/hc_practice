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
    def __init__(self, price, shortage: int, balance: int, message: str):
        self.price = price
        self.shortage = shortage
        self.balance = balance
        super().__init__(message)

    def __str__(self):
        return f"{self.args[0]}（商品価格: {self.price} / 不足額: {self.shortage}円 / 残高: {self.balance}円）"
    
class Suica:
    """Suica（実物準拠の仕様）

    Notes:
        デポジット(500円)は「預かり金」。支払い・チャージの計算には含めない。
        返却時の返金対象として別管理する（本課題では未使用）。

    Attributes:
        DEPOSIT (int): 500。預かり金（利用不可）。
        MIN_CHARGE (int): 最小チャージ額。
        MAX_BALANCE (int): 利用可能残高の上限。
    """
    DEPOSIT = 500
    MIN_CHARGE = 100
    MAX_BALANCE = 20000

    def __init__(self, balance=0):
        # 生成時の保証：初期値の妥当性
        if balance < 0 or balance > Suica.MAX_BALANCE:
            raise ValueError("不正な初期残高です。")
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    def charge(self, amount: int) -> None:
        self._update_balance(amount)

    def pay(self, amount: int) -> None:
        self._update_balance(-amount)

    def _update_balance(self, amount: int) -> None:
        # チャージ処理
        if amount >= 0:
            if amount < Suica.MIN_CHARGE:
                raise InvalidChargeAmountError(amount, self.balance, f"■{Suica.MIN_CHARGE}円以上の額をチャージして下さい。")
            new_balance = self.balance + amount
            if new_balance > Suica.MAX_BALANCE:
                raise InvalidChargeAmountError(amount, self.balance, f"■チャージ上限額（{Suica.MAX_BALANCE}円）を超えています。")
            self.__balance = new_balance
        # 支払い処理
        else:
            # 支払い金額を正の数で取得
            price = -amount
            if price > self.balance:
                # 不足額を計算
                shortage = price - self.balance
                # 残高が支払い金額より少ない場合はエラー
                raise InsufficientBalanceError(price, shortage, self.balance, f"■残高不足です。")
            self.__balance = self.__balance + amount


if __name__ == "__main__":
    print("=== Suicaクラス単体テスト ===")
    suica = Suica()
    print("Suica初期残高:", suica.balance)

    suica.charge(1000)
    print("チャージ後のSuica残高:", suica.balance)

    suica.pay(1100)
    print("支払い後のSuica残高:", suica.balance)
    print("=== テスト完了 ===")
