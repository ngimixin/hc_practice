"""自販機シミュレーター（main.py）

このモジュールはアプリ全体の依存関係を組み立てて `MainMenu` を返し、
`python main.py` で実行された場合はメニュー画面を起動します。
"""

from utils import drink_seed_factory as dsf
from drink_repository import DrinkRepository
from suica import Suica
from vending_machine import VendingMachine
from main_menu import MainMenu


def create_app() -> MainMenu:
    """アプリの依存関係一括組み立て"""
    inventory = dsf.create_default_inventory()
    repo = DrinkRepository(inventory)
    vm = VendingMachine(repo)
    suica = Suica(500)
    return MainMenu(vm, suica)


if __name__ == "__main__":
    app = create_app()
    app.display()
