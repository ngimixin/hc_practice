"""入力値を検証するバリデーターモジュール"""

from collections.abc import Callable
from utils import console_style as cs


class CancelledInput(Exception):
    """ユーザーが入力をキャンセルしたことを表す例外。"""


PROMPT_DEFAULT = "> "
INVALID_INPUT_MESSAGE = "無効な入力です。もう一度入力してください。"
CANCEL_TOKENS: set[str] = {"", "q", "n", "N"}


def _check_cancel(user_input: str) -> None:
    """キャンセル入力を検知し、該当すれば CancelledInput を送出する。

    Args:
        user_input: 入力された文字列。

    Raises:
        CancelledInput: キャンセル入力が検出された場合。
    """
    if user_input.strip() in CANCEL_TOKENS:
        raise CancelledInput()


def get_valid_int(condition: Callable[[int], bool], allow_cancel: bool = True) -> int:
    """整数入力を受け取り、条件を満たすまで繰り返す。

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

        if allow_cancel:
            _check_cancel(user_input)

        try:
            number = int(user_input)
        except ValueError:
            print()
            print(INVALID_INPUT_MESSAGE)
            cs.print_line()
            continue

        if condition(number):
            return number

        print()
        print(INVALID_INPUT_MESSAGE)
        cs.print_line()


def get_valid_yes_no(
    condition: Callable[[str], bool], allow_cancel: bool = True
) -> None:
    """y/n入力を受け取り、条件を満たすまで繰り返す。

    Args:
        condition: 入力値が満たすべき条件（Trueで受理）。
        allow_cancel: 空Enterやqでキャンセルを許可するか。

    Raises:
        CancelledInput: キャンセルが指示された場合。
    """
    while True:
        user_input = input(PROMPT_DEFAULT)
        cleaned_input = user_input.strip()

        if allow_cancel:
            _check_cancel(cleaned_input)

        if condition(cleaned_input):
            return

        print()
        print(INVALID_INPUT_MESSAGE)
        cs.print_line()
