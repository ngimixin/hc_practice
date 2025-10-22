"""バリデーションモジュール"""

from collections.abc import Callable
from utils import console_style as cs

class CancelledInput(Exception):
    """ユーザーが入力をキャンセルしたことを表す例外"""

PROMPT_DEFAULT = "> "
INVALID_INPUT_MESSAGE = "\n無効な入力です。"
CANCEL_TOKENS = {"", "q"} 

def _check_cancel(user_input: str, allow_cancel: bool) -> None:
    """キャンセル入力を検知し、該当すれば CancelledInput を送出する。
    
    Args:
        user_input: 入力された文字列。
        allow_cancel: キャンセルを許可するか。
    
    Raises:
        CancelledInput: キャンセル入力が検出された場合。
    """
    if allow_cancel and user_input.strip() in CANCEL_TOKENS:
        raise CancelledInput()


def get_valid_int(condition: Callable[[int], bool], allow_cancel: bool = True) -> int:
    """入力を受け取り、整数変換と条件チェックを行う。

    Args:
        condition: 入力値が満たすべき条件（Trueで受理）。
        allow_cancel: 空Enterやqでキャンセルを許可するか。

    Raises:
        CancelledInput: キャンセルが指示された場合。

    Returns:
        条件を満たした整数。
    """
    while True:
        user_input = input(PROMPT_DEFAULT)        
        
        _check_cancel(user_input, allow_cancel)
        
        try:
            number = int(user_input)
        except ValueError:
            print(INVALID_INPUT_MESSAGE)
            cs.print_line()
            continue
        
        if condition(number):
            return number

        print(INVALID_INPUT_MESSAGE)
        cs.print_line()
        
def get_valid_yes_no(condition: Callable[[str], bool], allow_cancel: bool = False) -> str:
    """y/n入力を受け、条件を満たすまで繰り返す。返り値は 'y' または 'n' 相当の1文字を返す想定。"""
    while True:
        user_input = input(PROMPT_DEFAULT)
        s = user_input.strip()

        _check_cancel(user_input, allow_cancel)

        # 空文字は 'n' 扱い
        if condition(s):
            return "n" if s == "" else s

        print(f"{INVALID_INPUT_MESSAGE}もう一度入力してください。")
        cs.print_line()
