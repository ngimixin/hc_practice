class ConsoleStyle:
    """CLI画面用の装飾定数"""
    SEPARATOR_LINE1 = "----------------------------------------"
    SEPARATOR_LINE2 = "========================================"

    @staticmethod
    def print_line(line_type: int = 1) -> None:
        line = (
            ConsoleStyle.SEPARATOR_LINE1
            if line_type == 1
            else ConsoleStyle.SEPARATOR_LINE2
        )
        print(line)
