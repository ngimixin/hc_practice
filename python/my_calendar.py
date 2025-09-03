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
    week = " ".join(day_of_week_l)
    
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
    print(week)



# 閏年判定関数
def is_leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

if __name__ == "__main__":
    main()