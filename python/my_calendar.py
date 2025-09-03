import sys
from datetime import datetime, timedelta


day_of_week_l = ["月", "火", "水", "木", "金", "土", "日"]

end_of_month_d = {28: [2],
                30: [4, 6, 9, 11],
                31: [1, 3, 5, 7, 8, 10, 12]}

input_date = None;

def main():
    # print(sys.argv) 
    #エディタから実行の場合
    if len(sys.argv) == 1:
        input_date = datetime.today().replace(day=1)
        # begining_of_month = input_date.replace(day=1)
    # コマンドライン実行の場合
    else:
        if sys.argv[1] == "-m":
            input_date = datetime(2025, int(sys.argv[2]), 1)

    begining_of_month = input_date
    this_year = begining_of_month.year
    this_month = begining_of_month.month
    this_month_jp = str(begining_of_month.month) + "月"
    first_weekday = begining_of_month.weekday()
    first_weekday_jp = day_of_week_l[first_weekday]
    week_column = " ".join(day_of_week_l)
    
    # 月末算出（閏年か考慮）
    if is_leap_year(this_year):
        end_of_month = 29
    else:
        key = [k for k, v in end_of_month_d.items() if this_month in v]
        end_of_month = key[0]
        

    print(f"今年：{this_year}")
    print(f"今月：{this_month_jp}")
    print(f"月初曜日：{first_weekday_jp}")
    print(f"月初：{begining_of_month}")
    print(f"月末：{end_of_month}")
    

    print(f"     {this_month_jp} 2025")
    print(week_column)
    generate_monthly_weeks(first_weekday, end_of_month)
    
# 一ヶ月の日数を5ないし6週間に分割し2次元リストにする関数
def generate_monthly_weeks(first_weekday, end_of_month):
    days = [v for v in range(1, end_of_month+1)]
    for _ in range(first_weekday):
        days.insert(0, "") # type: ignore  # Pylance の誤検知を無視

    weeks = [[], [], [], [], [], []]
    days_iter = iter(days)
    try:
        for j in range(6):
            while len(weeks[j]) < 7:
                weeks[j].append(next(days_iter))        
    except StopIteration:
        raise
    finally:
        print(weeks)
        return weeks


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

# TODO: cmd+d を　fn+f2と同じ動作にカスタムする
