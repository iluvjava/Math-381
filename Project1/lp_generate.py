"""
Name: Group 4
Class: math 381

This file contains all the codes that read the data collected from the model; and the producing the input for the
complete lp problem.
"""

__all__ = ["DietModel", "read_all_data", "try_reducedLP"]
from typing import List
FILE_LIST = ["All Meals(fixed).txt", "DM All Food.txt", "Starbucks Food.txt"]

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
    fileslist = FILE_LIST if filelist is None else filelist
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
    """
    The class is the internal model for everything that is involved for the lp problem.
    __FoodMatrixTranspose:
        Literally the transpose of the food matrix as it describes in the paper.
    """
    def __init__(self, Alldata: List[List[str]], vegetarian=False, vegan=False, obj="max"):
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

    def markup_constraints(self):
        """
        This is a method that is created for the convenience and robustness for generating the constraints
        for the problem.
        :return:
            (I: Row number, operator, rhs)
        """
        row_number = list(range(1, 14)) + [16, 2]
        operators = ["<="]*14 + [">="]
        rhs = [67 * 0.06 * 1000, 2000, 65, 20, 300, 2400, 300, 50, 20, 2500, 45, 2400, 400, 3, 931]
        return [(I, J, K) for I, J, K in zip(row_number, operators, rhs)]

    def __getitem__(self, indx):
        """
        Index the food matrix, first index specifies the row, second number specifies the
        column
        :param indx:
            a tuple of len 2, representing the index of the element you want to visit.
            indexing start with 0, and ends with n - 1,
            set
        :return:
            A float, the value of that entry, in the Food Matrix.
        """
        I, J = indx
        if J == ":":
            return [self.__FoodMatrixTranspose[K][I] for K in range(len(self.__FoodMatrixTranspose))]
        return self.__FoodMatrixTranspose[J][I]

    def format_objfxn(self):
        res = "max: "
        for I in range(self.food_matrix_width()):
            res += f"{self[0, I]}*{self.__Decision_Variables[I]}{' + ' if I != self.food_matrix_width() - 1 else ';'}"
            # Assume there is no food with cost 0.
        return res + "\n"

    def format_constraints(self):
        w = self.food_matrix_width()
        constraints = []
        for I, J, K in self.markup_constraints():
            non_Zero = {}
            for L in range(w):
                if self[I, L] != 0:
                    non_Zero[L] = self[I, L]
            if len(non_Zero):
                constraints.append((non_Zero, J, K))
        lp_string = ""

        # Formats above constraints:
        for constraint in constraints:
            line = [f"{(str(V) + '*') if V != 1 else ''}x{K}" for K, V in constraint[0].items()]
            line = " + ".join(line)
            line += f"{constraint[1]}{constraint[2]};\n"
            lp_string += line
        # Non negativity constraint
        for X in self.__Decision_Variables:
            lp_string += f"{X}>=0;"
        return lp_string + "\n"


    def format_vartype(self):
        res = "int "
        res += ", ".join(self.__Decision_Variables) + ";"
        return res + "\n"

    def format_lp(self):
        output_LP = "//This is the obj fxn for diet problem:\n"
        output_LP += self.format_objfxn()
        output_LP += "//These are the constraints:\n"
        output_LP += self.format_constraints()  # self.format_constraints()
        output_LP += "//Make all variable type integers :\n"
        output_LP += self.format_vartype()
        return output_LP

    def get_food_list(self, indx_list):
        return [self.__FoodNames[I] for I in indx_list]

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
    print("--------------------------------------COMPLETE LP---------------------------")
    project1_lp = d.format_lp()
    print(project1_lp)
    # Writing the LP input file into a file.
    with open("project1_lp.lp", "w+") as f:
        f.write(project1_lp)


if __name__ == "__main__":
    main()