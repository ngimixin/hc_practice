import sys
from datetime import datetime


def main():
    # print("test")
    # print(sys.argv) 
    if len(sys.argv) == 1:
        cal_base = datetime(2025, 1, 1)
    else:
        if sys.argv[1] == "-m":
            cal_base = datetime(2025, int(sys.argv[2]), 1)
    print(cal_base)

if __name__ == "__main__":
    main()