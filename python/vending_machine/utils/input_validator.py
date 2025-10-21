from collections.abc import Callable
from utils.console_style import ConsoleStyle
from utils.input_validator import InputValidator

class InputValidator:
    INVALID_INPUT_MESSAGE = "\n無効な入力です。"
    
    @staticmethod
    def get_valid_int(prompt: str, condition: Callable[[int], bool]) -> int:
        """入力を受け取り、整数変換と条件チェックを行う"""

        while True:
            user_input = input(prompt)        
            
            try:
                number = int(user_input)
            except ValueError:
                print(InputValidator.INVALID_INPUT_MESSAGE)
                ConsoleStyle.print_line()
                continue
            
            if condition(number):
                return number

            print(InputValidator.INVALID_INPUT_MESSAGE)
            ConsoleStyle.print_line()
            
    @staticmethod
    def get_valid_yes_no(prompt: str, condition: Callable[[str], bool]) -> str:
        """y/n入力を受け、条件を満たすまで繰り返す。返り値は 'y' または 'n' 相当の1文字を返す想定。"""

        while True:
            user_input = input(prompt)        
            s = user_input.strip()

            # 空文字は 'n' 扱い
            if condition(s):
                return "n" if s == "" else s
            print(f"{InputValidator.INVALID_INPUT_MESSAGE}もう一度入力してください。")
            ConsoleStyle.print_line()

