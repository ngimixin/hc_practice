from abc import ABC, abstractmethod


class Pokemon(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def type1(self) -> str:
        pass

    @property
    @abstractmethod
    def type2(self) -> str:
        pass

    @property
    @abstractmethod
    def hp(self) -> int:
        pass

    @abstractmethod
    def attack(self) -> None:
        pass

    # 抽象基底クラスでメソッドを実装した場合
    # def attack(self) -> None:
    #     print(f"{self.name} のこうげき！")


class Pikachu(Pokemon):
    def __init__(self, name: str, type1: str, type2: str, hp: int) -> None:
        self._name = name
        self._type1 = type1
        self._type2 = type2
        self._hp = hp

    @property
    def name(self) -> str:
        return self._name

    @property
    def type1(self) -> str:
        return self._type1

    @property
    def type2(self) -> str:
        return self._type2

    @property
    def hp(self) -> int:
        return self._hp

    def attack(self) -> None:
        print(f"{self.name} の10万ボルト！")


# 抽象クラスとインタフェース風（pythonにインタフェースは無い）
# 抽象クラス：インスタンス変数を持てる
class AbstractEx1(ABC):
    def __init__(self):
        super().__init__()  # 協調的super()にしておくと多重継承で安全
        self.value = 100

    def greet(self):
        print("hello!")  # メソッド実装


# インタフェース風
class InterfaceLike(ABC):
    @property
    @abstractmethod
    def value(self) -> int: ...

    @abstractmethod
    def greet(self) -> None: ...


# pythonでは多重継承が可能
class AbstractEx2(ABC):
    def __init__(self):
        super().__init__()
        self.value = 200

    def greet(self):
        print("こんにちは!")


class Child(AbstractEx1, AbstractEx2):
    def __init__(self):
        super().__init__()  # MROに従って AbstractEx1→AbstractEx2→ABC と辿る


if __name__ == "__main__":
    pika: Pikachu = Pikachu("ピカチュウ", "でんき", "", 100)
    # Pokemon.attack(pika) # 親クラスの attack をインスタンスを明示して呼び出す場合
    pika.attack()
