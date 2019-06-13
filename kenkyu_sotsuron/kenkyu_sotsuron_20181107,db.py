# 日本語ファイル名NG
# BD内のフレーズどうしの類似度を求め，データとして保存
import csv
import librosa
import numpy as np
import librosa.display
from numpy.linalg import norm
import os
import time
from numpy import array, zeros, argmin, inf, ndim
from scipy.spatial.distance import cdist
from dtw import dtw
np.set_printoptions(threshold=np.inf)

start = time.time()  # プログラム実行時間を測る

mylist = list()  # 計算がだぶらないために履歴を格納

files = os.listdir("C:\PythonFile\kenkyu_sotsuron\\db")  # フォルダをスキャン

phraseDict = {}

# mfcc処理
for file1 in files:
    y1, sr1 = librosa.load("C:\PythonFile\kenkyu_sotsuron\\db\\" + file1)
    mfcc1=librosa.feature.mfcc(y1, sr1)
    phraseDict[file1] = mfcc1
    np.save("dbnpy\\"+file1+".npy",mfcc1)

append = str()  # データを格納する場所

csvDB = list()

for fileA in files:
    for fileB in files:
        A = "C:\PythonFile\kenkyu_sotsuron\\db\\" + fileA
        B = "C:\PythonFile\kenkyu_sotsuron\\db\\" + fileB
        fileC = fileA + fileB
        fileD = fileB + fileA
        if (not (fileD in mylist)):  # 履歴になければ計算！
            mylist.append(fileC)
            if A != B:
                mfcc1 = phraseDict[fileA]
                mfcc2 = phraseDict[fileB]
                dist, cost, acc_cost, path = dtw(
                    mfcc1.T, mfcc2.T, dist=lambda x, y: norm(x - y, ord=1))
                # DTW計算結果
                print("between", fileA, "and", fileB, ' ',
                      'Normalized distance between the two sounds:', dist)
                # データをリストに保持
                csvrow = fileA, fileB, dist
                csvDB.append(csvrow)

with open('DB.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)  # writerオブジェクトの生成
    writer.writerows(csvDB)  # 複数行に書き込み
csv_file.close()

process_time = time.time() - start
print(process_time)
