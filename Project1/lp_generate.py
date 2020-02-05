"""
Name: Group 4
Class: math 381
"""

__all__ = ["DietModel", "read_all_data", "try_reducedLP"]
from typing import List

def read_csv(filename: str, ignore_1strow = False):
    with open(filename) as f:
        lines = f.read()
    lines = lines.split("\n")
    lines = [l.split(",") for l in lines]
    if ignore_1strow:
        lines.pop(0)
    return lines

def read_all_data(filelist = None):
    """
        First tile in the array must be all the meals!
    :param filelist:
        List if file names.
    :return:
    """
    fileslist = ["All Meals.txt", "DM All Food.txt", "Starbucks Food.txt"] if filelist is None else filelist
    merged_Data = []
    for fname, I in zip(fileslist, range(len(fileslist))):
        the_data = read_csv(fname, I != 0)
        # Append 1 or 0 depending on whether the food is a meal.
        for J in range(len(the_data)):
            the_data[J].append(1 if I == 0 else 0)
        merged_Data += the_data
    # Sanity Checks
    l = len(merged_Data[0])
    for I in merged_Data:
        assert l == len(I), F"Data Corrupted. line :{I}"
    return merged_Data

def is_number(s):
    """
    This piece of code is copied from the internet:
    https://www.pythoncentral.io/how-to-check-if-a-string-is-a-number-in-python-including-unicode/
    :param s:
    :return:
    """
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


class DietModel:

    def __init__(self, Alldata: List[List[str]]):
        self.__Columns = Alldata.pop(0)
        # Convert String data to numbers in python.
        food_Matrix = []
        for Row, I in zip(Alldata, range(len(Alldata))):
            food_Matrix.append([float(J) if is_number(J) else (1 if J == "N" else 0) for J in Row[1:]])
        self.__FoodMatrixTranspose = food_Matrix
        self.__Decision_Variables = [f"x{I}" for I in range(len(food_Matrix))]
        self.__FoodNames = [Row[0] for Row in Alldata]

    def get_columns(self):
        return self.__Columns

    def get_food_matrix_transpose(self):
        return self.__FoodMatrixTranspose

    def get_decision_variables(self):
        return self.__Decision_Variables

    def food_matrix_height(self):
        return len(self.__FoodMatrixTranspose[0])

    def food_matrix_width(self):
        return len(self.__FoodMatrixTranspose)

    def get_food_names(self):
        return self.__FoodNames

    def get_constraint_vector(self):
        res = []
        res.append(500/7) # Money he spend on each for the last week, eating the same food per day.
        res.append(67*0.06*1000) # The total amount of weight of food he can eat per day.
        res.append(2000) # He is on a 2000 calorie diet.
        res += [65, 20, 300, 2400, 300, 50, 20, 2500, 45, 2400, 400] # nutrition constraints
        res.append(len(self.__FoodMatrixTranspose)) # not on vegan diet.
        res.append(len(self.__FoodMatrixTranspose)) # not on vegetarian diet.
        res.append(3) # only 3 meals a day.
        return res

    def __getitem__(self, indx):
        """
        Index the food matrix, first index specifies the row, second number specifies the
        column
        :param indx:
            a tuple of len 2, representing the index of the element you want to visit.
            indexing start with 0, and ends with n - 1
        :return:
            A float, the value of that entry, in the Food Matrix.
        """
        I, J = indx
        return self.__FoodMatrixTranspose[J][I]

    def format_objfxn(self):
        res = "max: "
        for I in range(self.food_matrix_width()):
            res += f"{self[0, I]}*{self.__Decision_Variables[I]}{' + ' if I != self.food_matrix_width() - 1 else ';'}"
            # Assume there is no food with cost 0.
        return res + "\n"

    def format_constraints(self):
        res = ""
        h = self.food_matrix_height()
        w = self.food_matrix_width()
        # 17 nutrition constraints.
        for I in range(1, h): # Ignore the first money constraints
            counter = 0 # no right hand side if all coefficients are 0s.
            for J in range(w):
                if self[I, J] == 0:
                    continue
                counter += 1
                c = "" if self[I, J] == 1 else (str(self[I, J]) + "*")
                res += f"{'' if J == 0 else ' + '}" f"{c}{self.__Decision_Variables[J]}"
            res += "" if counter == 0 else f"<= {self.get_constraint_vector()[I]};\n"
        # non-negativity constraints
        res += "\n"
        for X in self.__Decision_Variables:
            res += f"{X}>=0; "
        return res + "\n"

    def format_vartype(self):
        res = "int "
        res += ", ".join(self.__Decision_Variables) + ";"
        return res + "\n"

    def format_lp(self):
        output_LP = "//This is the obj fxn for diet problem:\n"
        output_LP += self.format_objfxn()
        output_LP += "//These are the constraints:\n"
        output_LP += self.format_constraints()
        output_LP += "//Make all variable type integers :\n"
        output_LP += self.format_vartype()
        return output_LP

    def get_food_list(self, variablesindices):
        return [self.__FoodNames[I] for I in variablesindices]

    def get_food_name(self, var_indx: int):
        return self.__FoodNames[var_indx]

def try_reducedLP():
    the_data = read_all_data(filelist=["All Meals.txt", "Starbucks Food.txt"])
    reduced_lp = DietModel(the_data)
    reduced_lp_string = reduced_lp.format_lp()
    print(reduced_lp_string)
    with open("reduced_lp.lp", "w+") as f:
        f.write(reduced_lp_string)
    return reduced_lp

def main():
    the_data = read_all_data()
    print(the_data)
    print("----------------------------------------")
    d = DietModel(the_data)
    print(d.get_columns())
    print(f"The length is:{d.get_columns()}")
    print("---------------------------------------")
    print(d.get_food_matrix_transpose())
    print(f"The matrix is {len(d.get_food_matrix_transpose())} x {len(d.get_food_matrix_transpose()[0])}")
    print(f"The (2, 0) element of the food matrix is: {d[2, 0]}")
    print(f"These are the decision variables: {d.get_decision_variables()}")
    print(f"These are the constraints vectors: {d.get_constraint_vector()}, len = {len(d.get_constraint_vector())}")
    print(f"There is the objective function: {d.format_objfxn()}")
    print(f"format constraints:\n{d.format_constraints()}")
    print(f"format the variable types:\n{d.format_vartype()}")
    print("--------------------------------------COMPLETE LP---------------------------")
    project1_lp = d.format_lp()
    print(project1_lp)
    with open("project1_lp.lp", "w+") as f:
        f.write(project1_lp)


    print("--------------------------------------reduced LP--------------------------------")
    try_reducedLP()
    pass

if __name__ == "__main__":
    main()