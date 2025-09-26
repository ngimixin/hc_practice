"""ゴルフスコア判定（標準入力または ./tests/*.txt から読み込み、和名で出力）。

挙動:
    - 標準入力がある場合は 1 ケースのみを判定し、[stdin] 見出しで出力。
    - 標準入力が無い場合は ./tests/*.txt を **ファイル名の昇順** で処理し、
      各ファイル（1 ケース）ごとに [<ファイル名>] 見出しで出力。

入力前提:
    - 各ケースは2行（pars, strokes）。
    - 各行は18要素の整数をカンマ区切りで並べる（例: "4,4,5,..."）。
    - 本スクリプトでは妥当性チェックは最小限（int変換失敗で終了）。

判定仕様:
    - diff = stroke - par
    - par=5 のとき、stroke=1→CONDOR(-4)、stroke=2→ALBATROSS(-3)（特例）
    - それ以外で stroke=1 は「ホールインワン」
    - diff >= 2 は「nボギー」（例: diff=3 → "3ボギー"）
    - 上記以外は diff を Score(Enum) に変換して和名へ:
        - -4: "コンドル" / -3: "アルバトロス" / -2: "イーグル"
        - -1: "バーディ" /  0: "パー" /  1: "ボギー"

出力形式:
    - 1ケース=18ホール分の判定をカンマ区切りで1行に出力。
    - 複数ケース時は各行の先頭に角括弧で見出し（ファイル名）を付与。

使用例:
    $ python golf_score.py
    [case_1.txt] パー,バーディ,パー,...

    $ cat tests/case_1.txt | python golf_score.py
    [stdin] パー,バーディ,パー,...
"""

import os
import glob
import sys
from typing import TextIO, TypeAlias, Literal
from enum import Enum
from pathlib import Path


# --- type aliases ---
Row: TypeAlias = list[int]  # 18個想定
Case: TypeAlias = list[Row]  # 2行想定（pars, strokes）
Cases: TypeAlias = list[Case]  # 複数ケース


class Score(Enum):
    BOGEY = 1
    PAR = 0
    BIRDIE = -1
    EAGLE = -2
    ALBATROSS = -3
    CONDOR = -4


SCORE_LABELS: dict[Score, str] = {
    Score.BOGEY: "ボギー",
    Score.PAR: "パー",
    Score.BIRDIE: "バーディ",
    Score.EAGLE: "イーグル",
    Score.ALBATROSS: "アルバトロス",
    Score.CONDOR: "コンドル",
}

# --- Outcome 型（タグ付きタプル）---
# ① 通常スコア用：「enum」タグ ＋ Score（例: Score.BIRDIE）を入れる2要素タプル
OutcomeEnum: TypeAlias = tuple[Literal["enum"], Score]
# ② 複数ボギー用：「multi_bogey」タグ ＋ 何ボギーか（int）
OutcomeMultiBogey: TypeAlias = tuple[Literal["multi_bogey"], int]
# ③ ホールインワン用：「hole_in_one」タグのみ（値は不要なので1要素タプル）
OutcomeHoleInOne: TypeAlias = tuple[Literal["hole_in_one"]]
# ④ 上の3つの“どれか”である、という和（Union）
Outcome: TypeAlias = OutcomeEnum | OutcomeMultiBogey | OutcomeHoleInOne


def parse_two_lines(stream: TextIO) -> Case:
    """標準入力から2行（pars, strokes）を読み取り、intに変換した Case を1件だけ返す。

    挙動:
        - 標準入力から全行を読み取る（2行想定）。
        - 各行のカンマ区切り要素をintへ変換し、Case（[pars, strokes]）を作る。
        - 返り値は単一の Case。

    エラー時:
        - int変換に失敗した場合はメッセージを表示して終了コード 1 で終了。

    Returns:
        Case: 標準入力から読み込んだ 1ケース（[pars, strokes]）。
    """
    lines = stream.readlines()
    case_rows_strs = [line.rstrip("\n").split(",") for line in lines]

    try:
        case: Case = [[int(s) for s in line] for line in case_rows_strs]
    except ValueError as e:
        print("入力データに問題があります。")
        print(f"詳細: {e}")
        sys.exit(1)

    return case


def read_input() -> tuple[list[str], Cases]:
    """./tests/*.txt をファイル名の昇順リストで取得し、
        各ファイルを1ケース（pars 行 + strokes行）として読み込んで返す。

    挙動:
        - ./tests/*.txt をファイル名の昇順で列挙。
        - 各ファイルを2行（pars, strokes）として読み、各要素をintへ変換。
        - 変換済みの Case を Cases に蓄積。

    エラー時:
        - int変換に失敗した場合はメッセージを表示して終了コード 1 で終了。

    Returns:
        tuple[list[str], Cases]:
            - list[str]: 読み込んだファイルパスのリスト（昇順）
            - Cases:     各ファイルから得た Case を並べたリスト
    """
    dir_path = "./tests/"
    file_list = sorted(glob.glob(os.path.join(dir_path, "*.txt")))
    case_rows_strs = [[] for _ in range(len(file_list))]
    for i, file_path in enumerate(file_list):
        with open(file_path, "r") as f:
            lines = f.readlines()
            case_rows_strs[i] = [line.rstrip("\n").split(",") for line in lines]
    try:
        cases = [[[int(s) for s in line2] for line2 in line] for line in case_rows_strs]
    except ValueError as e:
        print("入力データに問題があります。")
        print(f"詳細: {e}")
        sys.exit(1)
    return file_list, cases


def judge_outcomes(cases: Cases) -> list[list[Outcome]]:
    """各ケースの18ホールを判定し、Outcome（タグ付きタプル）の二次元リストを返す。

    判定仕様:
        - diff = stroke - par
        - par=5 かつ stroke=1→("enum", Score.CONDOR)、stroke=2→("enum", Score.ALBATROSS)
        - 上記以外で stroke=1 → ("hole_in_one",)
        - diff >= 2 → ("multi_bogey", diff)
        - それ以外 → ("enum", Score(diff))  # diff を Enum にマップ

    Returns:
        list[list[Outcome]]: cases（ケース配列）× 18ホールの Outcome 二次元リスト。
    """

    def judge_one(par: int, stroke: int) -> Outcome:
        diff = stroke - par

        # Par5の1打/2打はコンドル/アルバトロス
        if par == 5 and (stroke == 1 or stroke == 2):
            return ("enum", Score(diff))

        # それ以外の1打はホールインワン
        if stroke == 1:
            return ("hole_in_one",)

        # +2以上はnボギー
        if diff >= 2:
            return ("multi_bogey", diff)

        # それ以外はEnumにマップ
        return ("enum", Score(diff))

    outcomes: list[list[Outcome]] = []
    for one_case in cases:
        pars, strokes = one_case
        row_outcomes: list[Outcome] = []
        for par, stroke in zip(pars, strokes):
            row_outcomes.append(judge_one(par, stroke))
        outcomes.append(row_outcomes)
    return outcomes


def format_outcomes_jp(outcomes: list[list[Outcome]]) -> list[list[str]]:
    """Outcome を日本語ラベル（文字列）に変換する。

    変換規則:
        - ("enum", Score.*)     → SCORE_LABELS で和名へ
        - ("multi_bogey", n)    → f"{n}ボギー"
        - ("hole_in_one",)      → "ホールインワン"

    Returns:
        list[list[str]]: ケース×18ホールの日本語ラベル二次元リスト。
    """
    labels: list[list[str]] = []
    for row in outcomes:
        row_labels: list[str] = []
        for outcome in row:
            match outcome:
                case ("enum", score):
                    row_labels.append(
                        SCORE_LABELS[score]
                    )  # score は Score と推論される
                case ("multi_bogey", n):
                    row_labels.append(f"{n}ボギー")  # n は int
                case ("hole_in_one",):
                    row_labels.append("ホールインワン")
        labels.append(row_labels)
    return labels


def main():
    """エントリーポイント。

    フロー:
        1) 標準入力が端末か（isatty）で入力経路を分岐
            - 非端末（パイプ/リダイレクト）: parse_two_lines(sys.stdin) で1ケース読込、見出しは "stdin"
            - 端末                 : read_input() で ./tests/*.txt を全件処理
        2) judge_outcomes() で判定
        3) format_outcomes_jp() で和名に変換
        4) 見出し（[stdin] または [<ファイル名>]）＋ カンマ区切りで出力

    Returns:
        None: 標準出力へ結果を出す。
    """
    file_list: list[str] = []

    if not sys.stdin.isatty():
        one_case = parse_two_lines(sys.stdin)
        cases = [one_case]
        file_list = ["stdin"]
    else:
        file_list, cases = read_input()
    outcomes = judge_outcomes(cases)
    jp_labels = format_outcomes_jp(outcomes)

    for i, label_row in enumerate(jp_labels):
        joined_scores = ",".join(label_row)
        path = file_list[i]
        file_name = Path(path).name
        print(f"[{file_name}]", joined_scores)


if __name__ == "__main__":
    main()
