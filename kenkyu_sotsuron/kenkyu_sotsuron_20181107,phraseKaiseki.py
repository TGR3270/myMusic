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
import socket
import pandas as pd

start = time.time()  # プログラム実行時間を測る

csvlistA = list()

mylist = list()  # 計算がだぶらないために履歴を格納

append = str()  # データを格納する場所

csvDB = list()

filesA = os.listdir("C:\PythonFile\kenkyu_sotsuron\\input")  # フォルダをスキャン
filesB = os.listdir("C:\PythonFile\kenkyu_sotsuron\\db")  # フォルダをスキャン

phraseDict = {}

# mfcc処理
for fileA in filesA:
    y1, sr1 = librosa.load("C:\PythonFile\kenkyu_sotsuron\\input\\" + fileA)
    mfcc1 = librosa.feature.mfcc(y1, sr1)
    phraseDict[fileA] = mfcc1

for fileB in filesB:
    mfcc1 = np.load("dbnpy\\"+fileB+".npy ")
    phraseDict[fileB] = mfcc1

for fileA in filesA:
    for fileB in filesB:
        A = "C:\PythonFile\kenkyu_sotsuron\\input\\" + fileA
        B = "C:\PythonFile\kenkyu_sotsuron\\db\\" + fileB
        fileC = fileA + fileB
        fileD = fileB + fileA
        if (not (fileD in mylist)):  # 履歴になければ計算！
            mylist.append(fileC)
            if A != B:
                dist, cost, acc_cost, path = dtw(
                    phraseDict[fileA].T, phraseDict[fileB].T, dist=lambda x, y: norm(x - y, ord=1))
                csvrow = fileA, fileB, dist
                csvDB.append(csvrow)

with open('kaiseki.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)  # writerオブジェクトの生成
    writer.writerows(csvDB)  # 複数行に書き込み
csv_file.close()


process_time = time.time() - start
print(process_time)
