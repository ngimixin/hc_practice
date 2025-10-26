from drink import Drink


class SoldOutError(Exception):
    """指定した商品が売り切れのときに発生する例外。"""


class ProductNotFoundError(KeyError):
    """指定された商品IDが存在しない場合に発生する例外。"""

    def __init__(self, product_id: int) -> None:
        """例外を初期化する。

        Args:
            product_id: 存在しなかった商品ID。
        """
        self.product_id = product_id
        super().__init__(f"■商品ID：{product_id} は存在しません。")

    def __str__(self) -> str:
        """print()などで文字列として出力されたときの表現。"""
        return self.args[0]


class DrinkRepository:
    """ドリンク在庫を管理するリポジトリ。

    在庫は `dict[int, list]` として保持する。
    各要素は `[brand: str, price: int, drinks: deque[Drink]]` の並びを想定する。
    """

    def __init__(self, inventory: dict[int, list]) -> None:
        """リポジトリを初期化する。

        Args:
            inventory: product_id をキーに、[brand, price, deque(Drink)] を値に持つ辞書。
        """
        self.__inventory = inventory

    def get_all(self) -> dict[int, list]:
        """取扱商品一覧を取得する。

        Returns:
            在庫辞書の浅いコピー。各商品の `deque[Drink]` は共有される点に注意。

        Note:
            呼び出し側で `get_all()[id][2].append(...)` などを行うと
            内部状態に影響する（浅いコピーのため）。
        """
        return self.__inventory.copy()

    def get_price(self, product_id: int) -> int:
        """商品価格を取得する。

        Args:
            product_id: 価格を取得したい商品のID。

        Returns:
            その商品の価格（円）。

        Raises:
            ProductNotFoundError: 指定IDの商品が存在しない場合。
        """
        if product_id not in self.__inventory:
            raise ProductNotFoundError(product_id)

        return self.__inventory[product_id][1]

    def increase_stock(self, product_id: int, quantity: int) -> None:
        """指定商品の在庫を quantity 本追加する。

        Args:
            product_id: 対象商品のID。
            quantity: 追加本数（1以上を想定）。

        Raises:
            ProductNotFoundError: 指定IDの商品が存在しない場合。
        """
        if product_id not in self.__inventory:
            raise ProductNotFoundError(product_id)

        brand, price, drinks = self.__inventory[product_id]
        drinks.extend(Drink(brand, price) for _ in range(quantity))

    def decrease_stock(self, product_id: int) -> Drink:
        """指定商品の在庫を1本減らし、そのドリンクを返す。

        Args:
            product_id: 対象商品のID。

        Returns:
            取り出された `Drink` インスタンス。

        Raises:
            ProductNotFoundError: 指定IDの商品が存在しない場合。
            SoldOutError: 在庫が0本の場合。
        """
        if product_id not in self.__inventory:
            raise ProductNotFoundError(product_id)

        brand, _, drinks = self.__inventory[product_id]
        if not drinks:
            raise SoldOutError(f"■{brand}は売り切れです。")

        return drinks.popleft()
