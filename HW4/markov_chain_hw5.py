"""
Name: Hongda Li
Class: math 381

This file is for writing assignment 5.
"""

from fractions import Fraction
from sympy import Matrix as Mtx
from sympy import latex

def main():
    """
    :return:
    """
    P = generate_transitional_matrix()
    P = Mtx(P)
    print(latex(P))
    print("-----------------------------------------------------------------------------------------------")
    print(latex(P.T ** 10))


def generate_transitional_matrix():
    Sixth = Fraction(1, 6)
    Dice = [(1, Sixth), (2, Sixth), (4, 2*Sixth), (5, Sixth), (6, Sixth)]
    StatesToValue = {0:0, 1:1, 2:4, 3:6, 4:8, 5:9, 6:10, 7:12, 8:14, 9:15, 10:16}
    ValuesToStates = {0:0, 1:1, 4:2, 6:3, 8:4, 9:5, 10:6, 12:7, 14:8, 15:9, 16:10}
    LoseValues = [2, 3, 5, 7, 11, 13, 17]
    P = [[0 for I in range(13)] for J in range(13)] # Initialize the Transition matrix as all zeros.
    P[-1][-1] = 1 # The losing state. Absorbing state.
    P[-2][-2] = 1 # the wining state. Absorbing state.
    for I, Sum in StatesToValue.items():
        for DiceValue, Probability in Dice:
            if Sum + DiceValue >= 18:
                P[I][-1] += Probability # Wins!
            elif (Sum + DiceValue) in LoseValues:
                P[I][-2] += Probability # Lose....
            else:
                P[I][ValuesToStates[Sum + DiceValue]] += Probability
    # Sanity check that this is indeed a markov transition matrix.
    for R in P:
        assert sum(R), "Row sum not 1, not markov transition matrix. "
    return P


if __name__ == "__main__":
   main()