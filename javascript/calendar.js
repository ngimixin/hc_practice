// calendar.js
// cal風カレンダーを標準出力に描画するスクリプト（ライブラリ不使用）
//
// - `node calendar.js`            : 今月を表示し、当日を反転表示する
// - `node calendar.js -m <1..12>` : 指定月を表示（今月を指定した場合のみ当日を反転表示）
// - 曜日見出しは日本語、表示は6行×7列、日付は2桁右寄せ、タイトルは幅20で中央寄せ。
// - 曜日は日曜始まり（macの cal と同じ）

"use strict";

// 曜日見出し（日曜始まり）
const WEEK_HEADER = "日 月 火 水 木 金 土";

// 反転表示（ANSIエスケープ）
const Color = {
  REVERSE: "\x1b[07m", // 文字色と背景色を反転
  RESET: "\x1b[0m", // リセット
};

/**
 * コマンドライン引数を解析し、表示対象（年, 月）とハイライト日を返す。
 *
 * 挙動:
 * - 引数なし:
 *   今月（今年）を表示し、今日の日付をハイライト
 * - `-m <1..12>`:
 *   指定月（今年）を表示。指定月が今月なら今日をハイライト、それ以外はハイライトしない
 * - 不正月:
 *   "<入力> is neither a month number (1..12) nor a name" を出して終了(1)
 *
 * Returns:
 *   { year: number, month: number, highlightDay: number | null }
 *   month は 1..12
 */
function parseArgs() {
  const today = new Date();
  const thisYear = today.getFullYear();
  const thisMonth = today.getMonth() + 1; // 1..12
  const thisDay = today.getDate();

  // process.argv: [node, script, ...args]
  const args = process.argv.slice(2);

  if (args.length === 0) {
    // 引数なし
    return { year: thisYear, month: thisMonth, highlightDay: thisDay };
  }

  // `-m <month>` のみ許可
  if (!(args.length === 2 && args[0] === "-m")) {
    const bad = args[0] ?? "";
    console.error(`${bad} is neither a month number (1..12) nor a name`);
    process.exit(1);
  }

  const rawMonth = args[1];

  // 数値として解釈（"06" などもOKにする）
  // ※正規表現で整数かどうかを厳密に見る
  if (!/^\d+$/.test(rawMonth)) {
    console.error(`${rawMonth} is neither a month number (1..12) nor a name`);
    process.exit(1);
  }

  const month = Number(rawMonth);

  if (!(1 <= month && month <= 12)) {
    console.error(`${month} is neither a month number (1..12) nor a name`);
    process.exit(1);
  }

  const highlightDay = month === thisMonth ? thisDay : null;
  return { year: thisYear, month, highlightDay };
}

/**
 * その月の最終日（28/29/30/31）を返す。
 * JSの Date を使うことで、うるう年判定は不要。
 *
 * Args:
 *   year: number
 *   month: number (1..12)
 *
 * Returns:
 *   number
 */
function getEndOfMonth(year, month) {
  // 「翌月の0日」＝「当月の最終日」
  const monthIndex = month - 1; // 0..11
  return new Date(year, monthIndex + 1, 0).getDate();
}

/**
 * cal風（最大6行×7列）の週配列を生成する。
 *
 * 仕様:
 * - 日曜始まり
 * - 日付は2桁右寄せ
 * - 空欄は "  "（半角スペース2つ）
 * - highlightDay が指定されている場合、その日付を反転表示
 * - 6行×7列（42セル）に固定
 *
 * Args:
 *   firstWeekday: number (0=日, 1=月, …, 6=土) ※ Date.getDay() 準拠
 *   endOfMonth: number
 *   highlightDay: number | null
 *
 * Returns:
 *   string[][]  // 6行×7列
 */
function generateMonthlyWeeks(firstWeekday, endOfMonth, highlightDay) {
  // 日付セルを2桁右寄せに整形し、必要なら反転を付ける
  const fmt = (v) => {
    const cell = String(v).padStart(2, " ");
    if (highlightDay !== null && v === highlightDay) {
      return `${Color.REVERSE}${cell}${Color.RESET}`;
    }
    return cell;
  };

  // 先頭の空きを firstWeekday 個だけ "  " で埋める（= 1日が始まる曜日まで埋める）
  const days = Array(firstWeekday)
    .fill("  ")
    .concat(Array.from({ length: endOfMonth }, (_, i) => fmt(i + 1)));

  // 42セルまで埋める（cal風に6行固定）
  while (days.length < 42) {
    days.push("  ");
  }

  // 7日ごとに切って6行作る
  const weeks = [];
  for (let i = 0; i < 42; i += 7) {
    weeks.push(days.slice(i, i + 7));
  }
  return weeks;
}

/**
 * タイトル・曜日見出し・週配列を標準出力に描画する。
 *
 * Args:
 *   year: number
 *   month: number (1..12)
 *   weeks: string[][]
 */
function printCalendar(year, month, weeks) {
  const title = `${month}月 ${year}`
    .padStart(Math.floor((20 + `${month}月 ${year}`.length) / 2), " ")
    .padEnd(20, " ");
  console.log(title);
  console.log(WEEK_HEADER);
  for (const w of weeks) {
    console.log(w.join(" "));
  }
}

function main() {
  const { year, month, highlightDay } = parseArgs();

  // 月初（1日）の曜日を取得（0=日..6=土）
  const monthIndex = month - 1;
  const firstWeekday = new Date(year, monthIndex, 1).getDay();

  // 月末日
  const endOfMonth = getEndOfMonth(year, month);

  // 週配列生成 & 出力
  const weeks = generateMonthlyWeeks(firstWeekday, endOfMonth, highlightDay);
  printCalendar(year, month, weeks);
}

main();
