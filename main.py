import os
import re
import Levenshtein
import pandas as pd

# global path.
rootPath = './'
posPath = rootPath + '/security_patch/'
negPath = rootPath + '/random_commit/'
candiPath = rootPath + '/candidates/'
judPosPath = rootPath + '/judged/positives/'
judNegPath = rootPath + '/judged/negatives/'

def main():
    posFeat, negFeat = ReadData()
    negFeat = RefineNegative(negFeat)
    GetDistMatrix(posFeat, negFeat)
    return

def ReadData():
    # define variable.
    posFeat = []
    negFeat = []
    # read data from csv file.
    dset = pd.read_csv('feature.csv')
    dfeat = dset.values.tolist()
    # find file names for positive samples.
    posList = [file for root, ds, fs in os.walk(posPath) for file in fs]
    posListExt = [file for root, ds, fs in os.walk(judPosPath) for file in fs]
    if len(posListExt):
        posList.extend(posListExt)
    # separate the data.
    for item in dfeat:
        fileName = item[1]
        # check positive.
        posSign = 0
        for posName in posList:
            if posName in fileName:
                posSign = 1
                posList.remove(posName)
                break
        # arrange positives and negatives.
        if posSign:
            posFeat.append(item[1:])
        else:
            negFeat.append(item[1:])
    # complete check.
    print('[Info] Loaded %d positives and %d negatives (totally %d).' % (len(posFeat), len(negFeat), len(posFeat)+len(negFeat)))
    if 0 == len(posList):
        print('[Info] Complete loading all positive samples.')
    else:
        print('[Error] Not all positive samples loaded!')
        print(posList)
    return posFeat, negFeat

def RefineNegative(negFeat):
    # define variables.
    negFeatNew = []
    # get negative list.
    negList = [file for root, ds, fs in os.walk(judNegPath) for file in fs]
    if 0 == len(negList):
        print('[Info] No negative refined!')
        return negFeat
    # refine data.
    for item in negFeat:
        fileName = item[0]
        # check negatives.
        negSign = 0
        for negName in negList:
            if negName in fileName:
                negSign = 1
                negList.remove(negName)
                break
        # refine negatives.
        if negSign:
            pass
        else:
            negFeatNew.append(item)
    # complete check.
    if 0 == len(negList):
        print('[Info] Complete refining all negative samples.')
    else:
        print('[Error] Not all negative samples refined!')
        print(negList)
    return negFeatNew

def GetDistMatrix(posFeat, negFeat):
    print('[Info] Processing %d positives and %d candidates (totally %d).' % (len(posFeat), len(negFeat), len(posFeat) + len(negFeat)))
    pos

    return

def Dist(list1, list2):
    return

if __name__ == '__main__':
    main()