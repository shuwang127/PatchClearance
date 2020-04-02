import os
import re
import Levenshtein
import pandas as pd

# global path.
rootPath = './'
posPath = rootPath + '/security_patch/'
negPath = rootPath + '/random_commit/'

def main():
    posFeat, negFeat = ReadData()
    print((posFeat[0]))
    return

def ReadData():
    # define variable.
    posFeat = []
    negFeat = []
    # read data from csv file.
    dset = pd.read_csv('feature.csv')
    # extract data features.
    dfeat = dset.values.tolist()
    # separate the data.
    for item in dfeat:
        if 'security_patch' in item[1]:
            posFeat.append(item[2:])
        else:
            negFeat.append(item[2:])
    return posFeat, negFeat


if __name__ == '__main__':
    main()