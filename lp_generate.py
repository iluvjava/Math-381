"""
Name: Hongda Li
Class: Math 381
This file is dedicated to creating LP solve text for the Lpsolve IDE.

The codes needs python 3.6 or higher.
"""

__all__ = ["ChromaticNumberProblem"]

from typing import Union, List, Tuple
import math as m
Number = Union[int, float]


class ChromaticNumberProblem:
    """
        This is a class that is desinged to solve the chromatic number problem for any given graph.
        [
            [y1, y2, y3,... y12],
            [x_1_1, x_1_2, ... x_1_12],
            ...
            [x_12_1, x_12, 2, ... x_12_12]
        ]
    """
    def __init__(self, N=12 ,Var_Matrix=None, Adj_Matrix=None):
        """
        :param N:
            The number of vertex involved, by default.
        :param Var_Matrix:
            A function that returns the variable matrix.
            By default it's None and it will be replaced by the var_matrix of the homework problem.
        :param Adj_Matrix:
            A function that returns the adjacency matrix of the graph.
            By default it's None and it wil be replaced by the adj_matrix function of the homework problem.
        """
        def var_matrix():
            mtx = [[f"y{I + 1}" for I in range(N)]]
            mtx += [[f"x_{J + 1}_{I + 1}" for I in range(N)] for J in range(N)]
            return mtx
        var_matrix = var_matrix if Var_Matrix is None else Var_Matrix
        def adj_matrix():
            return [[1 if bool(I != J and m.cos(I + 1) + m.cos(J + 1) > 0) else 0 for J in range(N)] for I in range(N)]
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
        the coefficient is a list of tuples in the format of (I, J, K)
        where the first 2 numbers are the double index for accessing the variable name
        and the third number is the coefficient of that variable.
        """
        constraints = []
        opt = "="
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
            A list of constraints.
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
            A list of constraints.
        """
        constraints = []
        rhs = 1
        opt = "<="
        for I in range(self.__N):
            for J in range(I + 1, self.__N):  # vertex No looping back on itself.
                # print(f"{(I, J)} n = {self.__N}")
                if self.__edge(I, J):
                    for K in range(self.__N): # for all the color
                        coeff = [(I + 1, K, 1), (J + 1, K, 1)]
                        constraints.append({"coeff": coeff, "rhs": rhs, "opt": opt})
        return constraints

    def color_in_sequence(self):
        """
            * Generating a list of constraints representing that the color should be used in sequence.
            y_{i + 1}-y_{i}>=0
            which is basically:
            y1<=y2<=y3...<y12
        :return:
            A list of constraints
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
        return "min: " + "+".join([f"y{I + 1}" for I in range(self.__N)]) + ";"

    def format_variable_type(self):
        """
            For the hw problem, we want all variables involved to be a binary variable.
        :return:
            A string that defines the variable types for the Lp problem.
        """
        head = "bin "
        tail = ";"
        return head + ",".join(J for I in self.__VarMatrix for J in I) + tail

    def format_constraint(self, constraint: List[Tuple]):
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

    def produce_lp(self):
        """
        It produce the constraints for the LP in the following order:
        * The obj fxn
        * the uni color constraints
        * The only use valid color constraint.
        * the no adj vertex sharing color constraint
        * the color in sequence constraint.
        * the variable type constraint.
        :return:
        A string that is all the stuff need to solve that lp in the lpsolve ide.
        """
        result = self.format_objective_fxn() + "\n";

        result += "/*Here is all the constraints that make all the vertex uses one color at a time: */\n"
        uni_Color_Constraints = self.uni_color()
        for constraint in uni_Color_Constraints:
            result += self.format_constraint(constraint) + "\n"
        result += f"/*For the unique color constraints, we have {len(uni_Color_Constraints)} of them.*/\n"

        result += "/*Here is all the constraints that make each vertex only uses valid color: */\n"
        valid_Color_Constraints = self.only_use_valid_color()
        for constraint in valid_Color_Constraints:
            result += self.format_constraint(constraint) + "\n"
        result += f"/*Constraint counts: {len(valid_Color_Constraints)}*/\n"

        result += "/*No adj vertex share color consraints: */\n"
        adj_Sharing = self.no_sharing_color()
        for constraint in adj_Sharing:
            result += self.format_constraint(constraint) + "\n"
        result += f"/*Constraints count: {len(adj_Sharing)}*/\n"

        result += "/*Here is all the color in sequence constraint*/\n"
        color_Sequence = self.color_in_sequence()
        for constraint in color_Sequence:
            result += self.format_constraint(constraint) + "\n"
        result += f"/*constraint count: {len(color_Sequence)}*/\n"

        result += self.format_variable_type()

        return result + "\n/*That is the end of the lp problem*/"

    def get_adj_matrix(self):
        return self.__AdjMatrix


def generate_problem():
    """
    4 points square problem
    :return:
    The string for the lpsolver input.
    """
    def adj_M():
        return [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0]]

    def var_matrix(N=4):
        mtx = [[f"y{I + 1}" for I in range(N)]]
        mtx += [[f"x_{J + 1}_{I + 1}" for I in range(N)] for J in range(N)]
        return mtx
    p = ChromaticNumberProblem(N=4, Adj_Matrix= adj_M, Var_Matrix=var_matrix)
    print(p.produce_lp())
    pass


def generate_HWproblem():
    """
    function generate the hw problem using the adjacency matrix for the hw.
    :return:
        The string, which is the text for the lp_solve.
    """
    p = ChromaticNumberProblem()
    res = p.produce_lp()
    print(res)
    print("This is the adjacency matrix: ")
    for row in p.get_adj_matrix():
        print(str(row)[1:-1])
    return res

if __name__ == "__main__":
    res = generate_HWproblem()
    with open("lp.lp", "w+") as f:
        f.write(res)
    pass


