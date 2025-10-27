from abc import ABC, abstractmethod


# インタフェース風
class NameService(ABC):
    @abstractmethod
    def change_name(self, new_name: str) -> None:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class Pokemon(NameService, ABC):
    def __init__(self) -> None:
        self.__name = ""  # private相当

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

    def change_name(self, new_name: str) -> None:
        # 不適切な名前はエラー
        if new_name == "うんこ":
            print("不適切な名前です")
            return
        self.__name = new_name

    def get_name(self) -> str:
        return self.__name


class Pikachu(Pokemon):
    def __init__(self, type1: str, type2: str, hp: int) -> None:
        super().__init__()
        self.__type1 = type1
        self.__type2 = type2
        self.__hp = hp

    @property
    def type1(self) -> str:
        return self.__type1

    @property
    def type2(self) -> str:
        return self.__type2

    @property
    def hp(self) -> int:
        return self.__hp

    def attack(self) -> None:
        print(f"{super().get_name()} の10万ボルト!")


class Player(NameService):
    def __init__(self) -> None:
        self.__name = "プレイヤー"

    def change_name(self, new_name: str) -> None:
        """プレイヤーは自由に名前変更可能"""
        print(f"プレイヤー名を『{new_name}』に変更しました。")
        self.__name = new_name

    def get_name(self) -> str:
        return self.__name


if __name__ == "__main__":
    pika = Pikachu("でんき", "", 100)
    player = Player()
    
    pika.change_name("ピカチュウ")
    print(pika.get_name())  # ピカチュウ
    pika.attack()

    pika.change_name("うんこ")  # 不適切な名前です と表示される
    print(pika.get_name())  # 太郎

    player.change_name("サトシ")
    print(player.get_name())  # ピカチュウ
