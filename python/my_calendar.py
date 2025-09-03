import sys
from datetime import datetime, timedelta


# month = {1: "January", 2: "February", 3: "March", 4: "April", 
#          5: "May", 6: "June", 7: "July", 8: "August", 
#          9: "September", 10: "October", 11: "November", 12: "December"}

day_of_week = ["月", "火", "水", "木", "金", "土", "日"]

end_of_month = {28: 2,
                30: [4, 6, 9, 11],
                31: [1, 3, 5, 7, 8, 10, 12]}

def main():
    # print("test")
    # print(sys.argv) 
    if len(sys.argv) == 1:
        input_date = datetime.today()
        begining_of_the_month  = input_date.replace(day=1)
         
    else:
        if sys.argv[1] == "-m":
            begining_of_the_month = datetime(2025, int(sys.argv[2]), 1)

    this_year = begining_of_the_month.year
    this_month = str(begining_of_the_month.month) + "月"
    first_weekday = begining_of_the_month.weekday()

    print(f"今年：{this_year}")
    print(f"今月：{this_month}")
    print(f"月初曜日：{first_weekday}")
    print(f"月初：{begining_of_the_month}")
    

    print(f"    {this_month} 2025")
    

    print(begining_of_the_month)
    # end_of_month = begining_of_the_month  + datetime.date(2015, 1, 1) - relativedelta(days=1)
    # print(end_of_month)
    # hantei = is_leap_year(year)
    # print(hantei)
    # if 



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