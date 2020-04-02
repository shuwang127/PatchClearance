import os
import re
import Levenshtein
import pandas as pd

# global path.
rootPath = './'
posPath = rootPath + '/security_patch/'
negPath = rootPath + '/random_commit/'

def main():
    ReadData()
    return

def ReadData():
    # define variable.
    posFeat = []
    negFeat = []
    # read data from csv file.
    dset = pd.read_csv('feature.csv')
    # extract data features.
    dfeat = dset.values.tolist()

    print(dfeat[1000])
    print(len(dfeat[1000]))
    for item in dfeat:
        if 'security_patch' in item[1]:
            print('1')
            pass
        else:
            print('0')
            pass

    return


if __name__ == '__main__':
    main()