"""
This is a lovely module that is going to bridge with the "sympy" module
to make linear algebra in python a fun fun experience.
This file is focusing on the following:

1. Matrix
2. Linear Algebra
3. Fractional Arithmetic.

It's for math 407 not math 381, I am just too lazy to change the directory.
"""

__all__ = ["get_tableau"]

from sympy import Matrix as mx, init_printing
from fractions import Fraction
init_printing()

from typing import List, Type, Union;
MyNumber = Union[Type[Fraction], float, int]



def main():
    print("Main is empty. ")

def Stuff():
    pass

# OK
def get_tableau(A:List[List[MyNumber]], b: List[MyNumber], c: List[MyNumber]):
    """
        Pads with 0 for c, the objective vector. s
    :param A: A matrix
    :param b: B constraint vector
    :param c:
    :return:
        The whole tableau except the objective, which returned as the second parameter,
        separately.
        * dimension of the returned matrix len(A) by len(A) + len(A[0])
        * left part is the A matrix, then the Identity, the augmented part is the b vector.
    """
    A = [I.copy() for I in A.copy()]
    assert len(A) == len(b), "b and A doesn't match."
    for Row in A:
        assert len(Row) == len(c), "Objective and rows doesn't match."
    for R, I in zip(A, range(len(A))):
        temp = [0]*len(A)
        temp[I] = 1
        R += temp
        R.append(b[I])
    return A, c.copy()

def pivot_tableau():
    pass



class SimplexTableau:
    """
    Put in the simplex method in standard form, and help us
    to create the SimpleTableau to help with stuff.
    The class assume the following:

    1. Standard form
    2. All b_i is positive.
    """

    def __init__(self, ConstraintMatrix, bVec, obj):
        """

        :param ConstraintMatrix:
        :param bVec:
        :param obj:
        """
        self.__Tableau, self.__Obj = get_tableau(ConstraintMatrix, obj, bVec)
        self.__BasicIndex = set([I for I in range(len(ConstraintMatrix[0]))])
        for b in bVec:
            assert b >= 0, "Cannot do 2 phase simplex, no negative in b. "
        self.__Tableau += obj.copy() + [0]
        self.__Tableau = mx(self.__Tableau)
        self.__Width = len(ConstraintMatrix) + len(ConstraintMatrix[0]) # The width of the tableau.

    def get_tableau(self):
        return self.__Tableau

    def find_pivot(self):
        # Smallest Subscript:

        pass

    def pivot_on(self, entering, leaving):
        pass




if __name__ == "__main__":
    main()
    print("Matrix from sympy is imported as mx")
