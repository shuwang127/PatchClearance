'''
    Security Patch Group: Data Cleaning Task.
    Developer: Shu Wang
    Date: 2020-04-03
    File Structure:
    Patch
        |-- candidates              # found samples need to be judged.
        |-- judged                  # already judged samples.
                |-- negatives
                |-- positives
        |-- matlab                  # matlab program.
        |-- random_commit           # unknown patches.
        |-- security_patch          # positive patches.
        |-- temp                    # temporary stored variables.
                |-- distMatrix.npy
                |-- outIndex.npy
        |-- extract_features.py     # extract features for random_commit and security_patch.
        |-- feature.csv             # feature file.
        |-- main.py                 # main entrance.
    Usage:
        python main.py
'''

import os
import time
import shutil
import random
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
# global variable.
start_time = time.time() #mark start time

def main():
    posFeat, negFeat = ReadData()
    negFeat = RefineNegative(posFeat, negFeat)
    VerifyNegative(posFeat, negFeat)
    # feature space matching.
    #distMatrix = GetDistMatrix(posFeat, negFeat) # tmpPath + '/distMatrix.npy'
    #outIndex = FindTomekLinks(distMatrix) # tmpPath + '/outIndex.npy'
    #GetCandidates(outIndex, negFeat)
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
    else:
        if not os.path.exists(judPath):
            os.mkdir(judPath)
        os.mkdir(judPosPath)

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
    print('[Info] Loaded %d positive and %d random samples (totally %d).' % (len(posFeat), len(negFeat), len(posFeat)+len(negFeat)))
    if 0 == len(posList):
        print('[Info] Complete loading all positive samples. [TIME: %s sec]' % (round((time.time() - start_time),2)))
    else:
        print('[Error] Not all positive samples loaded! (para: %d)' % (len(posList)))
        print(posList)
    return posFeat, negFeat

def RefineNegative(posFeat, negFeat):
    # validate.
    if not os.path.exists(judNegPath):
        if not os.path.exists(judPath):
            os.mkdir(judPath)
        os.mkdir(judNegPath)
        print('[Info] No negative refined! [TIME: %s sec]' % (round((time.time() - start_time),2)))
        return negFeat

    # get negative list.
    negList = [file for root, ds, fs in os.walk(judNegPath) for file in fs]
    numList = len(negList)
    if 0 == numList:
        print('[Info] No negative refined! [TIME: %s sec]' % (round((time.time() - start_time),2)))
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
    print('[Info] Loaded %d positive, %d negative, %d random samples (totally %d).' % (len(posFeat), numList - len(negList), len(negFeatNew), len(posFeat) + len(negFeatNew) + numList - len(negList)))
    if 0 == len(negList):
        print('[Info] Complete refining all random samples. [TIME: %s sec]' % (round((time.time() - start_time),2)))
    else:
        print('[Error] Not all random samples refined! (para: %d)' % (len(negList)))
        print(negList)
    return negFeatNew

def VerifyNegative(posFeat, negFeat):
    # get existing
    negList = [file for root, ds, fs in os.walk(negPath) for file in fs]
    judNegList = [file for root, ds, fs in os.walk(judNegPath) for file in fs]
    judList = [file for root, ds, fs in os.walk(judPath) for file in fs]
    # define variables.
    negFeatNew = []
    # verify data.
    for item in negFeat:
        fileName = item[0]
        for negName in negList:
            if negName in fileName:
                negFeatNew.append(item)
                negList.remove(negName)
                break

    # complete check.
    print('[Info] Loaded %d positive, %d negative, %d random samples (totally %d).' % (len(posFeat), len(judNegList), len(negFeatNew), len(posFeat) + len(judNegList) + len(negFeatNew)))
    if len(judList) == len(negList):
        print('[Info] Complete verify all random samples. [TIME: %s sec]' % (round((time.time() - start_time),2)))
    else:
        print('[Error] Find new random samples in %s! (para: %d)' % (negPath, len(negList) - len(judList)))
        for file in judList:
            if file in negList:
                negList.remove(file)
        print(negList)
    return negFeatNew

def GetDistMatrix(posFeat, negFeat):
    # get distance between two lists.
    def GetDist(list1, list2, weights):
        dist = [((list1[i] - list2[i]) * weights[i]) ** 2 for i in range(len(weights))]
        # print(dist)
        # print(sum(dist))
        return sum(dist)
    # get weights.
    weights = GetWeights()
    #GetDist(posFeat[0][1:], negFeat[0][1:], weights)
    # get distance matrix
    posNum = len(posFeat)
    negNum = len(negFeat)
    print('[Info] Processing %d positives and %d candidates (totally %d).' % (posNum, negNum, posNum + negNum))
    distMatrix = np.zeros((posNum, negNum))
    for iPos in range(posNum):
        for iNeg in range(negNum):
            distMatrix[iPos][iNeg] = GetDist(posFeat[iPos][1:], negFeat[iNeg][1:], weights)
        print('> [Proc] Sample %d / %d ... [TIME: %s sec]' % (iPos+1, posNum, round((time.time() - start_time),2)))
    # save to local.
    if not os.path.exists(tmpPath):
        os.mkdir(tmpPath)
    np.save(tmpPath + '/distMatrix.npy', distMatrix)
    print('[Info] Get the distance matrix. [TIME: %s sec]' % (round((time.time() - start_time),2)))
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
        print('> [Proc] Tomek Link %d / %d ... [TIME: %s sec]' % (len(set(outIndex))-1, posNum, round((time.time() - start_time), 2)))
    # save file
    if not os.path.exists(tmpPath):
        os.mkdir(tmpPath)
    np.save(tmpPath + '/outIndex.npy', outIndex)
    print('[Info] Get the tomek link index. [TIME: %s sec]' % (round((time.time() - start_time),2)))
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
    print('[Info] Get all the candidates. [TIME: %s sec]' % (round((time.time() - start_time),2)))
    return 1

def GetWeights():
    # input the data set.
    dset = pd.read_csv('feature.csv')
    dfeat = dset.values.tolist()
    # convert to array..
    for item in dfeat:
        item.pop(1)
        item.pop(0)
    nfeat = np.array(dfeat).T
    # print(nfeat)
    # max and min of features.
    dimNum = len(nfeat)
    dimMax = [max(item) for item in nfeat]
    dimMin = [min(item) for item in nfeat]
    dimAbs = [max(abs(dimMax[i]), abs(dimMin[i])) for i in range(dimNum)]
    # weights = 1 / max(abs(maxV), abs(minV))
    scales = 10e4
    weights = [(scales/w) if w else scales for w in dimAbs]
    # maxDist would be 61 * (2 * scales)**2
    # print(max(weights)) # 10000
    # print(min(weights)) # 1/300
    return weights

def RandomChoose(Feat):
    featLen = len(Feat)
    featList = list(range(featLen))
    random.shuffle(featList)
    for i in range(500):
        index = featList[i]
        filename = Feat[index][0]
        shutil.copy(filename, './random_choose/')
    return

if __name__ == '__main__':
    main()