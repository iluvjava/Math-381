"""
Name: Group 4
Class: Math 381

This file contains codes that read the results output from the lp_generate.
Given the file name in the source codes, it will read the file and get the result,
then it will print it out and tell the user what the solution is.
"""

from lp_generate import *
import os.path as p

# Macro Settings
RESULT_FILE_NAME = "solutions/objective.csv"


def try_read_lp_results(datafile = RESULT_FILE_NAME):
    if p.isfile(datafile):
        file_Content = ""
        with open(datafile) as f:
            file_Content = f.read();
            file_Content = file_Content.split("\n")
            file_Content = [l.split(";") for l in file_Content]
            trimmed = []
            for ROW in file_Content:
                if len(ROW) > 1:
                    trimmed.append(ROW)
            return trimmed
    return None


def interpret_results(results, obj_fxn_values):
    """
    Using the full instance of the dietary model, it will interpret
    the results and print out what food is involved.
    :return:
        a string that can be read.
    """
    d = DietModel(read_all_data())
    solutions = []
    for C in range(1, len(results[0])): # all columns except the first one (The variables columns )
        non_zero_values = {}
        for R in results:
            if R[C] != '0':
                non_zero_values[R[0]] = R[C]
        solutions.append(non_zero_values)
    output = ""
    for S, I in zip(solutions, range(len(solutions))):
        output += f"--- Solution {I + 1}, obj fxn value: {obj_fxn_values[I + 1]}---\n"
        for K, V in zip(S.keys(), S.values()):
            output += f"\t{d.get_food_name(K)}: {V}\n"
    return output


def main():
    lp_Results = try_read_lp_results()
    if lp_Results is None:
        print(f"expect \"{RESULT_FILE_NAME}\" under root directory but it does not exists. ")
        return

    first_Row = lp_Results.pop(0) # Trim off the first row.
    obj_Fxn_Values = lp_Results.pop(0)
    # Remove the x letter in the first columns.
    # convert them numbers at the same time.
    print(first_Row)
    print(obj_Fxn_Values)
    for ROW in lp_Results:
        ROW[0] = int(ROW[0][1:])

    print(interpret_results(lp_Results, obj_Fxn_Values))
    pass

if __name__ == "__main__":
    main()
