class InvalidChargeAmountError(ValueError):
    """Suicaのチャージ額の範囲外を表す例外。"""

    def __init__(self, amount: int, balance: int, message: str) -> None:
        self.amount = amount
        self.balance = balance
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.args[0]}（入金額: {self.amount}円 / 残高: {self.balance}円）"


class InsufficientBalanceError(ValueError):
    """Suicaの残高不足を表す例外。"""

    def __init__(self, price, shortage: int, balance: int, message: str) -> None:
        self.price = price
        self.shortage = shortage
        self.balance = balance
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.args[0]}（商品価格: {self.price} / 不足額: {self.shortage}円 / 残高: {self.balance}円）"


class Suica:
    """Suica 残高を扱うドメインモデル。

    Attributes:
        MIN_CHARGE (int): 1回あたりの最小チャージ額。
        MAX_BALANCE (int): Suicaの残高上限額。
    """

    MIN_CHARGE = 100
    MAX_BALANCE = 20000

    def __init__(self, balance: int = 0) -> None:
        """Suicaを初期化する。

        Args:
            balance: 初期残高（100〜20000 の範囲で指定）。

        Raises:
            ValueError: 初期残高が100未満、または20000を超える場合。
        """
        # 生成時の保証：初期値の妥当性
        if balance <= Suica.MIN_CHARGE or balance > Suica.MAX_BALANCE:
            raise ValueError("不正な初期残高です。")
        self.__balance = balance

    @property
    def balance(self) -> int:
        return self.__balance

    def charge(self, amount: int) -> None:
        """金額をチャージする。"""
        self._update_balance(amount)

    def pay(self, amount: int) -> None:
        """金額を支払う（残高から減算）。"""
        self._update_balance(-amount)

    def _update_balance(self, amount: int) -> None:
        """内部用：残高を増減させる（符号で加減算を切り替え）。

        Raises:
            InvalidChargeAmountError: チャージ額が下限未満、または上限超過になるとき。
            InsufficientBalanceError: 支払いが残高を上回るとき。
        """
        # チャージ処理
        if amount >= 0:
            if amount < Suica.MIN_CHARGE:
                raise InvalidChargeAmountError(
                    amount,
                    self.balance,
                    f"■{Suica.MIN_CHARGE}円以上の額をチャージして下さい。",
                )
            new_balance = self.balance + amount
            if new_balance > Suica.MAX_BALANCE:
                raise InvalidChargeAmountError(
                    amount,
                    self.balance,
                    f"■チャージ上限額（{Suica.MAX_BALANCE}円）を超えています。",
                )
            self.__balance = new_balance

        # 支払い処理
        else:
            # 支払い金額を正の数で取得
            price = -amount
            if price > self.balance:
                # 不足額を計算
                shortage = price - self.balance
                # 残高が支払い金額より少ない場合はエラー
                raise InsufficientBalanceError(
                    price, shortage, self.balance, "■残高不足です。"
                )
            self.__balance = self.__balance + amount  # amount は負数
