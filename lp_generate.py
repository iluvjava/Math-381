"""
Name: Hongda Li
Class: Math 381
This file is dedicated to creating LP solve text for the Lpsolve IDE.

The codes needs python 3.6 or higher.
"""

__all__ = ["ChromaticNumberProblem"]

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
    def __init__(self, N=12 ,Var_Matrix=None, Adj_Matrix=None):
        def var_matrix():
            mtx = [[f"y{I + 1}" for I in range(N)]]
            mtx += [[f"x_{J + 1}_{I + 1}" for I in range(N)] for J in range(N)]
            return mtx
        var_matrix = var_matrix if Var_Matrix is None else Var_Matrix
        def adj_matrix():
            return [[1 if bool(I != J and m.cos(I) + m.cos(J) > 0) else 0 for J in range(N)] for I in range(N)]
        adj_matrix = adj_matrix if Adj_Matrix is None else Adj_Matrix
        self.__AdjMatrix = adj_matrix()
        self.__VarMatrix = var_matrix()
        self.__N = N
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
        """
        constraints = []
        opt = "<="
        rhs = 1
        for I in range(1, self.__N + 1):
            coeff = [(I, J, 1) for J in range(self.__N)]
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
        rhs = 0
        opt = "<="
        for I in range(self.__N):
            for J in range(self.__N):
                coeff = [(I + 1, J, 1), (0, J, -1)]
                constraints.append({"coeff": coeff, "opt": opt, "rhs": rhs})
        return constraints

    def no_sharing_color(self):
        """
        This function creates the constraints representing the following conditions from the problem:
            * None of the adjacent vertex shares the same color:
        :return:
        """
        constraints = []
        rhs = 1
        opt = "<="
        for I in range(1, self.__N + 1):
            for J in range(I + 1, self.__N):# vertex No looping back on itself.
                if self.__edge(I - 1, J):
                    for K in range(self.__N): # for all the color
                        coeff = [(I, K, 1), (J, K, 1)]
                        constraints.append({"coeff": coeff, "rhs": rhs, "opt": opt})
        return constraints

    def color_in_sequence(self):
        """
            * Generating a list of constraints representing that the color should be used in sequence.
            y_{i + 1}-y_{i}>=0
            which is basically:
            y1<=y2<=y3...<y12
        :return:
        """
        constraints = []
        opt = "<="
        rhs = 0
        for J in range(1, self.__N):
            coeff = [(0, J, 1), (0, J - 1, -1)]
            constraints.append({"coeff": coeff, "opt": opt, "rhs": rhs})
        return constraints

    def format_objective_fxn(self):
        """
        :return:
            A string that is the objective function for the LP problem.
        """
        pass

    def format_variable_type(self):
        """
        :return:
            A string that defines the variable types for the Lp problem.
        """
        pass

    def format_constraint(self, constraint):
        """
        This function takes the constraints and use the variable matrix to produce one instance of the constraint
        inequality.
        :param constraint:
            a map in the format of: {"coeff": ???, "opt": ???, "rhs":??}
        :return:
            A string that one line of inequality for the ststen.
        """
        tail = constraint["opt"] + str(constraint["rhs"]) + ';'
        output = ""
        coeff = constraint["coeff"]
        for I, J, c in coeff:
            v = self.__VarMatrix[I][J]
            output += f"{'+' if c > 0 else ''}{'' if c == 1 else ('-' if c == -1 else str(c) + '*')}{v}"
        return (output if output[0] is not "+" else output[1:]) + tail



if __name__ == "__main__":
    p = ChromaticNumberProblem()
    uni_Color_Constraint = p.uni_color()
    print("This is the uni color consraint for the hw problem: ")
    print(uni_Color_Constraint)
    print(p.format_constraint(uni_Color_Constraint[0]))

    print("Printing out all of the unique coloring constraints for the system: ")
    for I in p.uni_color():
        print(p.format_constraint(I))
    print("Print out: Only use valid color constraints: ")
    for I in p.only_use_valid_color():
        print(p.format_constraint(I))

    print("Print out: adjacent vertext doesn't share color constraints:")
    for I in p.no_sharing_color():
        print(p.format_constraint(I))
    ###################################################################################################################
    print("Experimenting with the 3 vertice full graph. ")
    def Adj_Matrix():
        return [[1 for I in range(3)] for J in range(3)]
    def Var_Matrix(N=3):
        mtx = [[f"y{I + 1}" for I in range(N)]]
        mtx += [[f"x_{J + 1}_{I + 1}" for I in range(N)] for J in range(N)]
        return mtx
    p = ChromaticNumberProblem(N=3, Adj_Matrix=Adj_Matrix, Var_Matrix = Var_Matrix)
    print("Here are the no sharing color constraints: ")
    for c in p.no_sharing_color():
        print(p.format_constraint(c))
    print("Here is the: Only use valid color constraints: ")
    for c in p.only_use_valid_color():
        print(p.format_constraint(c))
    print("Here is the uni color constraints: ")
    for c in p.uni_color():
        print(p.format_constraint(c))
    print("Here is color in sequence constraints: ")
    for c in p.color_in_sequence():
        print(p.format_constraint(c))
    pass


