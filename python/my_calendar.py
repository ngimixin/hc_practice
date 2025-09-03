import sys
from datetime import datetime

month = {1: "January", 2: "February", 3: "March", 4: "April", 
         5: "May", 6: "June", 7: "July", 8: "August", 
         9: "September", 10: "October", 11: "November", 12: "December"}

def main():
    # print("test")
    # print(sys.argv) 
    if len(sys.argv) == 1:
        cal_base = datetime.now()
    # else:
    #     if sys.argv[1] == "-m":
    #         cal_base = datetime(2025, int(sys.argv[2]), 1)

    print(cal_base)
    print(f"    {month[cal_base.month]} 2025")
    print(cal_base.weekday())

if __name__ == "__main__":
    main()