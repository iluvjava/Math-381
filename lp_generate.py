"""
Name: Hongda Li
Class: Math 381
This file is dedicated to creating LP solve text for the Lpsolve IDE.

The codes needs python 3.6 or higher.
"""

__all__ = ["Problem"]

from typing import List, Union, Dict
import math as m
Number = Union[int, float]
MyCoefficients = Dict[int, Number]
T1 = Union[List[str], List[List[str]], str]


class ChromaticNumberProblem:
    """
    The problem store the matrix in a 13 x 12 2d array, first row is dedicated to all

    For this problem, we have 144 variables for the x, and we will make a 13 by 12 matrix to
    store all the variables in the following format:
        [
            [y1, y2, y3,... y12],
            [x_1_1, x_1_2, ... x_1_12],
            ...
            [x_12_1, x_12, 2, ... x_12_12]
        ]
    """
    def __init__(self):
        def var_matrix(N=12):
            mtx = [[f"y{I + 1}" for I in range(N)]]
            mtx += [[f"x_{J + 1}_{I + 1}" for I in range(N)] for J in range(N)]
            return mtx
        def adj_matrix(N=12):
            return [[1 if bool(I != J and m.cos(I) + m.cos(J) > 0) else 0 for J in range(N)] for I in range(N)]
        self.__AdjMatrix = adj_matrix()
        self.__VarMatrix = var_matrix()
        self.__N = 12
        pass

    def __edge(self, I, J):
        """
        :return:
        True if {I, J} is an edge of in the graph.
        False it's not an edge in the graph.
        """
        return self.__AdjMatrix[I][J] == 1

    def uni_color(self):
        """
        Each vertex uses only one color at at time.
        :return:
        A list of constraints.
        A constraints is in the following formats:
        {"coeff": ???, "opt": ???, "rhs":??}
        coeff:
            A map with tuple, tuple maps to a value which is the coefficients of the variables.
        """
        constraints = []
        for I in range(1, self.__N + 1):
            coeff = dict()
            for J in range(self.__N):
                coeff[(I, J)] = 1
            opt = "<="
            rhs = 1
            constraints.append({"coeff": coeff, "opt": opt, "rhs": rhs})
        return constraints

    def only_use_valid_color(self):
        """
            Create a list of constraints.

            if a color is zero, then non of the vertex should be using that color:

            * for all I, J: x_I_J - y_J <= 0
            * There should be 144 constrains in total
        :return:
            A list of constraints in the usual format.
        """
        constraints = []
        for I in range(self.__N):
            for J in range(self.__N):
                coeff = dict()
                coeff[(I + 1, J)] = 1
                coeff[(0, J)] = -1
                rhs = 0
                opt = "<="
                constraints.append({"coef": coeff, "opt": opt, "rhs": rhs})
        return constraints

    def no_sharing_color(self):
        """
        This function creates the constraints representing the following conditions from the problem:
            * None of the adjacent vertex shares the same color:
        :return:
        """
        constraints = []
        for I in range(1, self.__N + 1):
            for J in range(I, self.__N):
                if self.__edge(I - 1, J):
                    for K in range(self.__N): # for all the color
                        coeff = dict()
                        rhs = 1
                        opt = "<="
                        coeff[(I, K)] = 1
                        coeff[(J, K)] = 1
                        constraints.append({"coeff": coeff, "rhs": rhs, "opt": opt})
                    pass
                pass
        return constraints

    def color_in_sequence(self):
        """
            * Generating a list of constraints representing that the color should be used in sequence.
        :return:
        """

        pass

    def format_consraint(self, constraint):
        """
        This function takes the constraints and use the variable matrix to produce one instance of the constraint
        inequality.
        :param constraint:
            a map in the format of: {"coeff": ???, "opt": ???, "rhs":??}
        :return:
            A string that represents the inequality.
        """
        tail = constraint["opt"] + str(constraint["rhs"])
        output = ""
        coeff = constraint["coeff"]
        for I in range(self.__N + 1):
            for J in range(self.__N):
                v = self.__VarMatrix[I][J]
                if (I, J) in coeff.keys():
                    c = coeff[(I, J)]
                    output += f"{'+' if c > 0 else ''}{'' if c == 1 else (c + '*')}{v}"
        return (output if output[0] is not "+" else output[1:]) + tail


if __name__ == "__main__":
    p = ChromaticNumberProblem()
    uni_Color_Constraint = p.uni_color()
    print("This is the uni color consraint for the hw problem: ")
    print(uni_Color_Constraint)
    print(p.format_consraint(uni_Color_Constraint[0]))

    print("Printing out all of the unique coloring constraints for the system: ")
    for I in p.uni_color():
        print(p.format_consraint(I))
    pass


