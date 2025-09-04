import sys
from datetime import datetime, timedelta


day_of_week_l = ["月", "火", "水", "木", "金", "土", "日"]
# カレンダーのヘッダ（曜日）
week_header = " ".join(day_of_week_l)

def print_calendar(this_year, this_month_jp, week_header, weeks_str_l):
    print(f"     {this_month_jp} {this_year}")
    print(week_header)
    for i in weeks_str_l:
        print(i[0])
    

def main():
    # 引数なし実行の場合
    if len(sys.argv) == 1:
        input_date = datetime.now().replace(day=1)
    # 引数あり実行の場合
    else:
        if sys.argv[1] == "-m" and int(sys.argv[2]) >= 1 and int(sys.argv[2]) <= 12:
            input_date = datetime.now().replace(month=int(sys.argv[2]), day=1)
            print(input_date)
    # TODO: エラー時の処理はあとで追加
    # print(f"{int(sys.argv[2])}")
                
    # 月初
    begining_of_month = input_date # type: ignore  # Pylance の誤検知を無視
    # 月初の曜日
    first_weekday = begining_of_month.weekday()
    this_year = begining_of_month.year
    this_month = begining_of_month.month
    this_month_jp = str(begining_of_month.month) + "月"
    
    # 月末算出（閏年か考慮）
    if this_month == 2:
        end_of_month = 29 if is_leap_year(this_year) else 28
    elif this_month in (4, 6, 9, 11):
        end_of_month = 30
    else:
        end_of_month = 31
        

    # 月初が月曜以外の場合、開始位置を調整するために空要素をプレースホルダーとして挿入し、    
    # 一ヶ月を5ないし6週間に分割し2次元リストにする
    weeks_l = generate_monthly_weeks(first_weekday, end_of_month)

    # 週ごとに分けた2次元リストを1週間毎に文字列化
    weeks_str_l = [[], [], [], [], [], []]
    for i in range(len(weeks_l)):
        weeks_str_l[i].append(" ".join(weeks_l[i]))

    print_calendar(this_year, this_month_jp, week_header, weeks_str_l)

# 一ヶ月の日数を5ないし6週間に分割し2次元リストにする関数
def generate_monthly_weeks(first_weekday, end_of_month):
    days = [f"{v:>2}" for v in range(1, end_of_month+1)]
    for _ in range(first_weekday):
        days.insert(0, "  ") # type: ignore  # Pylance の誤検知を無視

    weeks_l = [[], [], [], [], [], []]
    days_iter = iter(days)
    try:
        for j in range(6):
            while len(weeks_l[j]) < 7:
                weeks_l[j].append(next(days_iter))        
    except StopIteration:
        raise
    finally:
        return weeks_l


# 閏年判定関数
def is_leap_year(this_year):
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

if __name__ == "__main__":
    main()


# 以下一時的メモ。後で消す
# print(f"今年：{this_year}")
# print(f"今月：{this_month_jp}")
# print(f"月初曜日：{first_weekday_jp}")
# print(f"月初：{begining_of_month}")
# print(f"月末：{end_of_month}")
