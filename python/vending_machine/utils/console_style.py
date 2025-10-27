"""CLI出力用のユーティリティ。

現在は SEPARATOR_LINE1 のみ使用しているが、
今後のUI拡張に備えて SEPARATOR_LINE2 も定義している。
"""

SEPARATOR_LINE1 = "----------------------------------------"
SEPARATOR_LINE2 = "========================================"


def print_line(line_type: int = 1) -> None:
    """区切り線を出力する。

    Args:
        line_type: 線の種類。1ならハイフン、2ならイコール。
    """
    line = SEPARATOR_LINE1 if line_type == 1 else SEPARATOR_LINE2
    print(line)
