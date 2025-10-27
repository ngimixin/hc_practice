"""自販機シミュレーターの初期ドリンクデータを生成するモジュール"""

from collections import deque
from drink import Drink


def create_default_inventory() -> dict[int, list]:
    """初期ドリンク3種類を生成して返す。

    Returns:
        商品IDをキー、[ブランド名, 価格, ドリンク在庫(deque)] を値とする辞書。
    """
    seeds = [
        (1, "ペプシ", 150, 5),
        (2, "モンスター", 230, 5),
        (3, "いろはす", 120, 5),
    ]

    # product_idごとに [brand, price, drinks] を格納する
    return {
        product_id: [brand, price, deque(Drink(brand, price) for _ in range(quantity))]
        for product_id, brand, price, quantity in seeds
    }
