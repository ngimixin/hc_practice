from drink_repository import DrinkRepository, SoldOutError
from drink import Drink
from suica import Suica


class VendingMachine:
    """自販機のユースケースを司るアプリケーションクラス。

    ドメインオブジェクト（Drink, Suica）とリポジトリ（DrinkRepository）の橋渡しを行い、
    「在庫補充」「購入可否の判定」「販売処理」などを提供する。
    """

    def __init__(self, repo: DrinkRepository, initial_amount: int = 0) -> None:
        """VendingMachine を初期化する。

        Args:
            repo: ドリンク在庫を管理するリポジトリ。
            initial_amount: 売上の初期値（単位: 円）。
        """
        self.__repo = repo
        self.__total_amount = initial_amount

    @property
    def total_amount(self) -> int:
        return self.__total_amount

    @total_amount.setter
    def total_amount(self, amount: int) -> None:
        self.__total_amount = amount

    def get_brands(self) -> dict[int, list]:
        """全ドリンク一覧（在庫情報つき）を返す。

        Returns:
            product_id をキー、(brand, price, stock_deque) を値とする辞書。
        """
        return self.__repo.get_all()

    def get_available_brands(self, suica: Suica) -> dict[int, list]:
        """購入可能なドリンク一覧を返す。

        「Suica 残高で購入可能」かつ「在庫が 1 本以上」の商品だけを抽出する。

        Args:
            suica: 残高判定に用いる Suica。

        Returns:
            条件を満たす product_id -> (brand, price, stock_deque) の辞書。
        """
        inventory: dict[int, list] = self.get_brands()
        available_brands: dict[int, list] = {}

        for product_id, drink_info in inventory.items():
            _, price, stock = drink_info
            if stock and suica.balance >= price:
                available_brands[product_id] = drink_info

        return available_brands

    def restock(self, product_id: int, quantity: int) -> None:
        """指定商品の在庫を追加する。

        Args:
            product_id: 在庫を追加する商品の ID。
            quantity: 追加本数（1 以上）。

        Raises:
            ProductNotFoundError: product_id が存在しない場合（リポジトリ実装に依存）。
        """
        self.__repo.increase_stock(product_id, quantity)

    def vend(self, product_id: int, suica: Suica) -> tuple[int, Drink]:
        """指定商品を 1 本販売する。

        Suica から価格分を決済し、在庫を 1 本減らしてドリンクを払い出す。
        在庫切れの場合は決済をロールバック（返金）して SoldOutError を伝播する。

        Args:
            product_id: 購入する商品の ID。
            suica: 決済に使用する Suica。

        Returns:
            (product_id, drink) のタプル。

        Raises:
            InsufficientBalanceError: 残高不足（`suica.pay` が送出）。
            SoldOutError: 在庫なし。
        """
        price = self.__repo.get_price(product_id)

        # 残高不足時は suica.pay が InsufficientBalanceError を送出（自動伝播）
        suica.pay(price)

        try:
            drink = self.__repo.decrease_stock(product_id)
        except SoldOutError as e:
            # 在庫なしなら決済をロールバック（内部的にはチャージと同義）
            suica.charge(price)
            raise e

        self.total_amount += price
        return (product_id, drink)
