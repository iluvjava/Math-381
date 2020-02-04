"""
Name: Group 4
Class: Math 381

"""

from lp_generate import *

if __name__ == "__main__":
    the_data = read_all_data()
    d = DietModel(the_data)
    d.get_food_list(input("Give me a list of index of variable in the solution; eg. "
                          "[0, 2, 3] means x0, x2, x3 are the lp solution \n"))
