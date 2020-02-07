from lp_generate import *


def main():
    d = DietModel(read_all_data())
    while True:
        index = input("Index of x please: ")
        index = parse(index)
        if not index:
            print("Please enter integer in between 0 to 179.")
        print(f"food name: {d.get_food_name(index)}")
    pass

def parse(number):
    try:
        result = int(number)
        return result if result >=0 and result <= 179 else None
    except:
        return None

if __name__ == "__main__":
    main()