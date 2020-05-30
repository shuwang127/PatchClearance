import os
import time
import shutil
import random
import numpy as np
import pandas as pd

rootPath = '../'
githubPath = rootPath + '/github_commit/'
randomPath = rootPath + '/random_commit/'

githubList = [file for root, ds, fs in os.walk(githubPath) for file in fs]

listLen = len(githubList)
listNum = list(range(listLen)) # [0, 1, 2, 3, ...]
random.shuffle(listNum)

cnt = 0
folder = 2
for i in range(listLen):
    index = listNum[i]
    filename = githubList[index]
    src = os.path.join(githubPath, filename)
    fdst = os.path.join(randomPath, 'commit' + str(folder).zfill(2))
    if not os.path.exists(fdst):
        os.mkdir(fdst)
    dst = os.path.join(fdst, filename)

    shutil.move(src, dst)
    print(dst)
    cnt += 1
    if cnt == 100000:
        cnt = 0
        folder += 1
