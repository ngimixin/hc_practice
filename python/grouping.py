import random


ALL_MEMBERS = ["A", "B", "C", "D", "E", "F"]


def split_group():
    """メンバーをランダムに 2-4 または 3-3 に分割して返す。

    各グループはアルファベット順にソートされて返される。

    Returns:
        tuple[list[str], list[str]]: 2つのグループのリスト
    """
    size = random.choice([2, 3])
    g1 = sorted(random.sample(ALL_MEMBERS, size))
    g2 = sorted(set(ALL_MEMBERS) - set(g1))
    return g1, g2


if __name__ == "__main__":
    g1, g2 = split_group()
    print(g1)
    print(g2)
