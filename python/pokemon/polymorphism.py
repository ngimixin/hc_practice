class Pokemon:
    def __init__(self, name: str, type1: str, type2: str, hp: int) -> None:
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.hp = hp

    def attack(self) -> None:
        print(f"{self.name} のこうげき！")


class Pikachu(Pokemon):
    def attack(self) -> None:
        super().attack()
        print(f"{self.name} の10万ボルト！")  # ピカチュウ の10万ボルト！


class Zenigame(Pokemon):
    def attack(self) -> None:
        print(f"{self.name} のみずでっぽう！")


def demo_override() -> None:
    pika: Pikachu = Pikachu("ピカチュウ", "でんき", "", 100)
    zeni: Zenigame = Zenigame("ゼニガメ", "みず", "", 90)

    pika.attack()  # ピカチュウ の10万ボルト！
    zeni.attack()  # ゼニガメ のみずでっぽう！


def demo_polymorphism() -> None:
    pokes: list[Pokemon] = [
        Pikachu("ピカチュウ", "でんき", "", 100),
        Zenigame("ゼニガメ", "みず", "", 90),
    ]

    for p in pokes:  # どのクラスでも Pokemon 型として扱える
        p.attack()  # 同じ attack() 呼び出しでも振る舞いが異なる（多態）


if __name__ == "__main__":
    demo_override()
    print("-----")
    demo_polymorphism()
