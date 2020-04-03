import os
import shutil
import numpy as np
import pandas as pd

# global path.
rootPath = './'
posPath = rootPath + '/security_patch/'
negPath = rootPath + '/random_commit/'
tmpPath = rootPath + '/temp/'
candiPath = rootPath + '/candidates/'
# judgement path.
judPath = rootPath + '/judged/'
judPosPath = judPath + '/positives/'
judNegPath = judPath + '/negatives/'

def main():
    posFeat, negFeat = ReadData()
    negFeat = RefineNegative(negFeat)
    distMatrix = GetDistMatrix(posFeat, negFeat)
    #distMatrix = np.load(tmpPath + '/distMatrix.npy')
    outIndex = FindTomekLinks(distMatrix)
    #outIndex = np.load(tmpPath + '/outIndex.npy')
    GetCandidates(outIndex, negFeat)
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
    if os.path.exists(judPosPath):
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
    # validate.
    if not os.path.exists(judNegPath):
        print('[Info] No negative refined!')
        return negFeat
    # get negative list.
    negList = [file for root, ds, fs in os.walk(judNegPath) for file in fs]
    if 0 == len(negList):
        print('[Info] No negative refined!')
        return negFeat
    # define variables.
    negFeatNew = []
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
    # get distance between two lists.
    def GetDist(list1, list2):
        dist = [(list1[i] - list2[i]) ** 2 for i in range(len(list1))]
        #print(dist)
        #print(sum(dist))
        return sum(dist)
    # get distance matrix
    posNum = len(posFeat)
    negNum = len(negFeat)
    print('[Info] Processing %d positives and %d candidates (totally %d).' % (posNum, negNum, posNum + negNum))
    distMatrix = np.zeros((posNum, negNum))
    for iPos in range(posNum):
        for iNeg in range(negNum):
            distMatrix[iPos][iNeg] = GetDist(posFeat[iPos][1:], negFeat[iNeg][1:])
    # save to local.
    if not os.path.exists(tmpPath):
        os.mkdir(tmpPath)
    np.save(tmpPath + '/distMatrix.npy', distMatrix)
    print('[Info] Get the distance matrix.')
    return distMatrix

def FindTomekLinks(distMatrix):
    # dimension.
    posNum = len(distMatrix)
    negNum = len(distMatrix[0])
    # init the minimum index.
    minDist = [np.min(item) for item in distMatrix]
    minIndex = [np.argmin(item) for item in distMatrix]
    # find the index.
    outIndex = (-1 * np.ones(posNum)).tolist()
    while (-1 in outIndex):
        ind = np.argmin(minDist)
        minInd = minIndex[ind]
        # if minInd has been used.
        if minInd in outIndex:
            distList = distMatrix[ind]
            banList = list(set(outIndex))
            banList.remove(-1)
            for i in banList:
                distList[i] = float("inf")
            minInd = np.argmin(distList)
        outIndex[ind] = minInd
        minDist[ind] = float("inf")
    # save file
    if not os.path.exists(tmpPath):
        os.mkdir(tmpPath)
    np.save(tmpPath + '/outIndex.npy', outIndex)
    print('[Info] Get the tomek link index.')
    return outIndex

def GetCandidates(outIndex, negFeat):
    # validate.
    if os.path.exists(candiPath):
        shutil.rmtree(candiPath)
    os.mkdir(candiPath)
    # copy file
    for i in outIndex:
        source = negFeat[i][0]
        shutil.copy(source, candiPath)
    print('[Info] Get all the candidates.')
    return 1

if __name__ == '__main__':
    main()