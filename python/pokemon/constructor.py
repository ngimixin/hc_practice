class Pokemon:
    def __init__(self, name: str, type1: str, type2: str, hp: int) -> None:
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.hp = hp

    def attack(self) -> None:
        print(f"{self.name} のこうげき！")


def demo_constructor() -> None:
    poke: Pokemon = Pokemon("ピカチュウ", "でんき", "なし", 100)
    print(poke.name)  # ピカチュウ
    print(poke.type1)  # でんき
    poke.attack()  # ピカチュウ のこうげき！


# 余談パート
class PokemonEx:
    def __init__(self, name: str, type1: str) -> None:
        self.ex_text = f"{name} は {type1} タイプのポケモン。"

    def show_info(self) -> None:
        print(self.ex_text)


def demo_ex_text() -> None:
    poke = PokemonEx("リザードン", "ほのお")
    poke.show_info()


if __name__ == "__main__":
    demo_constructor()
    demo_ex_text()
