class Drink:
    """ドリンクを表すクラス。

    ブランド名と価格を保持するだけのシンプルな値オブジェクト。
    """

    def __init__(self, brand: str, price: int) -> None:
        self.__brand = brand
        self.__price = price

    @property
    def brand(self) -> str:
        return self.__brand

    @property
    def price(self) -> int:
        return self.__price

    @price.setter
    def price(self, price) -> None:
        self.__price = price

    def __repr__(self) -> str:
        return f"Drink(brand={self.brand!r}, price={self.price})"
