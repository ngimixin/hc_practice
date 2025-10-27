class Pokemon:
    def __init__(self) -> None:
        self.name: str = "リザードン"
        self.type1: str = "ほのお"
        self.type2: str = "ひこう"
        self.hp: int = 100
        self.mp: int = 10

    def attack(self):
        print(f"{self.name} のこうげき！")


def demo_basic() -> None:
    poke: Pokemon = Pokemon()
    print(poke.name)
    print(poke.type1)
    poke.attack()
    print(poke.mp)


# クラスなしの場合
def demo_without_class() -> None:
    pokemon1_name: str = "ヒトカゲ"
    pokemon2_name: str = "ゼニガメ"
    # ...
    pokemon100_name: str = "ミュウ"
    pokemon1_type1: str = "ほのお"
    # ...


# クラスなしの場合（リストで管理する場合）
def demo_list_variant() -> None:
    pokemon_name: list[str] = ["ヒトカゲ", "ゼニガメ", "...", "ミュウ"]
    pokemon_type1: list[str] = ["..."]


# クラスありの場合
def create_pokemon100() -> list[Pokemon]:
    """100匹のポケモンを作る処理（ダミー）"""
    return [Pokemon() for _ in range(100)]


if __name__ == "__main__":
    demo_basic()

    # ポケモンのインスタンスを100匹分作る処理とする
    pokemons: list[Pokemon] = create_pokemon100()

    print(pokemons[0].name)  # 1匹目のポケモンの名前
    print(pokemons[9].type1)  # 10匹目のポケモンのタイプ1
    pokemons[99].attack()  # 100匹目のポケモンの攻撃
