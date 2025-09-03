import sys
from datetime import datetime, timedelta

month = {1: "January", 2: "February", 3: "March", 4: "April", 
         5: "May", 6: "June", 7: "July", 8: "August", 
         9: "September", 10: "October", 11: "November", 12: "December"}

day_of_week = {0: "Mo", 1: "Tu", 2: "We", 3: "Th", 4: "Fr", 5: "Sa", 6: "Su"}

def main():
    # print("test")
    # print(sys.argv) 
    if len(sys.argv) == 1:
        input_date = datetime.now()
        base_date = input_date.replace(day=1)
    else:
        if sys.argv[1] == "-m":
            base_date = datetime(2025, int(sys.argv[2]), 1)

    print(base_date)
    print(f"    {month[base_date.month]} 2025")
    print(base_date.weekday())

    print(base_date)

if __name__ == "__main__":
    main()