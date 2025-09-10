"""月曜始まり・cal風のカレンダーを標準出力に描画するスクリプト。

- `python calendar.py`             : 今月を表示し、当日を反転表示する
- `python calendar.py -m <1..12>`  : 指定月を表示（今月を指定した場合のみ当日を反転表示）
- 曜日見出しは日本語、表示は6行×7列、日付は2桁右寄せ、タイトルは幅20で中央寄せ。
"""
import sys
from datetime import datetime 


DAY_OF_WEEK_L = ["月", "火", "水", "木", "金", "土", "日"]
WEEK_HEADER = " ".join(DAY_OF_WEEK_L)
class Color:
    REVERSE = '\033[07m' #文字色と背景色を反転
    RESET = '\033[0m'    #全てリセット


def parse_args() -> tuple[datetime, int | None]:
    """コマンドライン引数を解析し、(表示対象の月初, ハイライトする日) を返す。

    挙動:
        - 引数なし:
            今月の1日と、今日の日付（ハイライト）を返す。
        - `-m <1..12>`:
            指定月の1日を返す。指定月が「今月」なら今日をハイライト、それ以外は None。
        - エラー時:
            * `-m` 以外のオプションが来たら:  "illegal option -- <文字>" を表示して終了(1)。
            * `-m` の値が無い/数値でない/1..12 範囲外/余計な引数あり:
                "is neither a month number (1..12) nor a name" を表示して終了(1)。

    Returns:
        tuple[datetime, int | None]: (表示対象の月初, ハイライトする「日」または None)
    """
    today = datetime.today()

    if len(sys.argv) >= 2:
        _ , m_option, *month_arg = sys.argv

        if m_option != "-m":
            if m_option.startswith("-"):
                print(f"illegal option -- {m_option.lstrip('-')}")
            else:
                print("is neither a month number (1..12) nor a name")
            sys.exit(1)

        if len(month_arg) != 1:
            print("is neither a month number (1..12) nor a name")
            sys.exit(1)

        try:
            int_month = int(month_arg[0])
        except ValueError:
            print(f"{month_arg[0]} is neither a month number (1..12) nor a name")
            sys.exit(1)

        if not (1 <= int_month <= 12):
            print(f"{int_month} is neither a month number (1..12) nor a name")
            sys.exit(1)

        beginning_of_month = today.replace(month=int_month, day=1)
        highlight_day = today.day if today.month == int_month else None
        return beginning_of_month, highlight_day

    # 引数なしの場合
    beginning_of_month = today.replace(day=1)
    highlight_day = today.day
    return beginning_of_month, highlight_day


def is_leap_year(this_year: int) -> bool:
    """与えられた西暦年が閏年かを判定する。

    判定規則:
        - 400で割り切れる年は閏年
        - 100で割り切れる年は平年
        - 4で割り切れる年は閏年
        - それ以外は平年

    Args:
        this_year (int): 判定する年

    Returns:
        bool: 閏年なら True、平年なら False
    """
    if this_year % 4 == 0:
        if this_year % 100 == 0:
            if this_year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def generate_monthly_weeks(first_weekday: int, end_of_month: int,  highlight_day: int | None) -> list[list[str]]:
    """月初の曜日と月末日をもとに、cal風（最大6行×7列）の週配列を生成する。

    仕様:
        - 出力は「週」を単位とした二次元リスト（各行が1週間、各要素が日付文字列）。
        - 日付は2桁右寄せ。先頭の空きは "  "（半角スペース2つ）で埋める。
        - `highlight_day` が指定されている場合、その「日」に
          反転表示（Color.REVERSE ... Color.RESET）を付与する。
        - 行数は最大6行（6×7=42セル）に整形する。

    Args:
        first_weekday (int): 月初の曜日（0=月, 1=火, …, 6=日）※ datetime.weekday() 準拠
        end_of_month (int): その月の最終日（28, 29, 30, 31 のいずれか）
        highlight_day (int | None): 反転表示する「日」。ハイライトしない場合は None

    Returns:
        list[list[str]]: 週ごとの文字列リストを並べた二次元リスト（最大6行×7列）
    """
    def fmt(v: int) -> str:
        cell = f"{v:>2}"
        return f"{Color.REVERSE}{cell}{Color.RESET}" if highlight_day is not None and v == highlight_day else cell

    # 先頭の空きを first_weekday個だけ "  " で埋めて、1日〜月末を後ろに並べる
    days = ["  "]*first_weekday + [fmt(v) for v in range(1, end_of_month + 1)]
    # 6行×7列で固定（cal準拠）。7日ごとにスライスして週を作る。
    # 1行の横幅は (2桁の数字 + 区切りスペース1)×7 - 1 = 20 文字
    return [days[i:i+7] for i in range(0, 42, 7)]


def print_calendar(this_year: int, this_month_jp: str, weeks_l: list[list[str]]) -> None:
    """タイトル・曜日見出し・週配列を標準出力に描画する（cal風）。

    レイアウト:
        - タイトルは幅20で中央寄せ（例: "      1月 2025      "）
        - 見出しはグローバル定数 WEEK_HEADER を使用
        - 各週（list[str]）はスペース区切りで結合して1行出力

    Args:
        this_year (int): 表示する西暦年
        this_month_jp (str): 表示する月の日本語表記（例: "2月"）
        weeks_l (list[list[str]]): generate_monthly_weeks の出力（週ごとの二次元リスト）
    """
    title = f"{this_month_jp} {this_year}".center(20)
    print(title)
    print(WEEK_HEADER)
    for w in weeks_l:
        print(" ".join(w))


def main() -> None:
    """エントリーポイント。

    フロー:
        1) 引数解析で「表示対象の月初」と「ハイライト日」を取得
        2) 閏年判定を含む月末日の算出
        3) 週配列（6行×7列）の生成
        4) カレンダーの描画（タイトル・見出し・各週）

    スクリプトとして直接実行されたときのみ実行される想定。
    """

    beginning_of_month, highlight_day = parse_args()
    first_weekday, this_year, this_month = beginning_of_month.weekday(), beginning_of_month.year, beginning_of_month.month 
    this_month_jp = f"{this_month}月"

    # 月末算出（閏年か考慮）
    if this_month == 2:
        end_of_month = 29 if is_leap_year(this_year) else 28
    elif this_month in (4, 6, 9, 11):
        end_of_month = 30
    else:
        end_of_month = 31

    weeks_l = generate_monthly_weeks(first_weekday, end_of_month, highlight_day)
    print_calendar(this_year, this_month_jp,  weeks_l)


if __name__ == "__main__":
    main()
