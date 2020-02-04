"""
Name: Group 4
Class: math 381
"""

from typing import List

def read_csv(filename: str, ignore_1strow = False):
    with open(filename) as f:
        lines = f.read()
    lines = lines.split("\n")
    lines = [l.split(",") for l in lines]
    if ignore_1strow:
        lines.pop(0)
    return lines

def read_all_csv():
    fileslist = ["All Meals.txt", "DM All Food.txt", "Starbucks Food.txt"]
    merged_Data = []
    for fname, I in zip(fileslist, range(len(fileslist))):
        merged_Data += read_csv(fname, I == 0)
    # Sanity Checks
    l = len(merged_Data[0])
    for I in merged_Data:
        assert l == len(I), F"Data Corrupted. line :{I}"
    return merged_Data


class DietModel:
    def __int__(self, Alldata: List[List[str]]):
        self.__Columns = Alldata[0]
        Alldata.pop(0)
        # Convert String data to numbers in python.
        for R in Alldata:
            pass
        pass




if __name__ == "__main__":
    print(read_all_csv())
    pass