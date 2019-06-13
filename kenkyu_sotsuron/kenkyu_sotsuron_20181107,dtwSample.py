import pylab as plt
import seaborn as sns
# 日本語ファイル名NG
# BD内のフレーズどうしの類似度を求め，データとして保存
import csv
import librosa
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import librosa.display
from dtw import dtw
from numpy.linalg import norm
import os

import time

start = time.time()

δ = lambda a,b: (a - b)**2
first = lambda x: x[0]
second = lambda x: x[1]

def minVal(v1, v2, v3):
    if first(v1) <= min(first(v2), first(v3)):
        return v1, 0
    elif first(v2) <= first(v3):
        return v2, 1
    else:
        return v3, 2 

def calc_dtw(A, B):
    S = len(A)
    T = len(B)

    m = [[0 for j in range(T)] for i in range(S)]
    m[0][0] = (δ(A[0],B[0]), (-1,-1))
    for i in range(1,S):
        m[i][0] = (m[i-1][0][0] + δ(A[i], B[0]), (i-1,0))
    for j in range(1,T):
        m[0][j] = (m[0][j-1][0] + δ(A[0], B[j]), (0,j-1))

    for i in range(1,S):
        for j in range(1,T):
            minimum, index = minVal(m[i-1][j], m[i][j-1], m[i-1][j-1])
            indexes = [(i-1,j), (i,j-1), (i-1,j-1)]
            m[i][j] = (first(minimum)+δ(A[i], B[j]), indexes[index])
    return m

csvlistA = list()

mylist = list()  # 計算がだぶらないために履歴を格納

files = os.listdir("C:\PythonFile\kenkyu_sotsuron\\dbTest")  # フォルダをスキャン
for fileA in files:
    for fileB in files:
        A = "C:\PythonFile\kenkyu_sotsuron\\dbTest\\" + fileA
        B = "C:\PythonFile\kenkyu_sotsuron\\dbTest\\" + fileB
        fileC = fileA + fileB
        fileD = fileB + fileA
        if (not (fileC in mylist)) and (not (fileD in mylist)):  # 履歴になければ計算！
            mylist.append(fileC)
            if A != B:
                y1, sr1 = librosa.load(A)
                y2, sr2 = librosa.load(B)
                mfcc1 = np.reshape(librosa.feature.mfcc(y1, sr1),(1,-1))
                mfcc2 = np.reshape(
                    librosa.feature.mfcc(y2, sr2), (1, -1))  # mfcc処理
                dist=calc_dtw(mfcc1, mfcc2)
                # DTW計算結果
                print("between", fileA, "and", fileB, ' ',
                      'Normalized distance between the two sounds:', dist)
                # データをリストに保持
                csvlistB = list()
                csvlistB.append(fileA)
                csvlistB.append(fileB)
                csvlistB.append(dist)
                csvlistA.append(csvlistB)
with open('outputDB.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)  # writerオブジェクトの生成
    writer.writerows(csvlistA)  # 複数行に書き込み
csv_file.close()

process_time = time.time() - start

print(process_time)
