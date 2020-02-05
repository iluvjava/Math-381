"""
Name: Group 4
Class: Math 381

This file contains codes that read the results output from the lp_generate.
Given the file name in the source codes, it will read the file and get the result,
then it will print it out and tell the user what the solution is.
"""

from lp_generate import *
import os.path as p


def try_read_lp_results(datafile = "lp_results.csv"):
    if p.isfile(datafile):
        file_Content = ""
        with open(datafile) as f:
            file_Content = f.read();
            file_Content = file_Content.split("\n")
            file_Content = [l.split(";") for l in file_Content]
            return file_Content
    return None

def main():
    lp_Results = try_read_lp_results()
    if lp_Results is None:
        print("expect \"lp_results.csv under\" under root directory but it does exists. ")
        return

    pass

if __name__ == "__main__":
    main()
