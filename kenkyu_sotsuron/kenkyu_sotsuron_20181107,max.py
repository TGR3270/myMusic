import os
import csv
import time

start = time.time()  # プログラム実行時間を測る

suisen = {}  # 推薦フレーズの辞書型

csvlistA = list()  # 分析対象のリスト

filesB = os.listdir("C:\PythonFile\kenkyu_sotsuron\\db")  # フォルダをスキャン
suisenAlls = os.listdir("C:\PythonFile\kenkyu_sotsuron\\db")  # フォルダをスキャン

# 初めの読み込み
with open('kaiseki.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        csvlistB = list()
        csvlistB.append(row[0])
        csvlistB.append(row[1])
        csvlistB.append(row[2])
        csvlistA.append(csvlistB)
# 推薦順を決定
for suisenAll in suisenAlls:
    mydict = {}
    # DB側のまとまりごとに類似度が一番高いものを算出
    for fileB in filesB:
        if not(fileB in suisen.keys()):
            minValue = 500
            minKey = 0
            for row in csvlistA:
                if fileB == row[1]:
                    # print(row)
                    if float(minValue) > float(row[2]):
                        minValue = row[2]
                        minKey = row[0]
            mydict[fileB, minKey] = minValue
    # まとまりのなかで一番類似度が低いものを推薦
    start = True
    for k, v in sorted(mydict.items(), key=lambda x: x[1], reverse=True):
        # print(k, v)
        if start:
            suisen[k[0]] = v
            start = False
    print(suisen)
    if len(suisen) >= 32:
        break
    # 推薦されたフレーズのDB側を除去
    for row in csvlistA:
        if row[1] in suisen.keys():
            csvlistA.remove(row)

    # 推薦されたフレーズを入力側に追加
    with open('DB.csv') as f:
        readerDB = csv.reader(f)
        for rowDB in readerDB:
            if rowDB[0] in suisen.keys() or rowDB[1] in suisen.keys():
                csvlistB = list()
                if rowDB[0] in suisen.keys():
                    csvlistB.append(rowDB[0])
                    csvlistB.append(rowDB[1])
                else:
                    csvlistB.append(rowDB[1])
                    csvlistB.append(rowDB[0])
                csvlistB.append(rowDB[2])
                csvlistA.append(csvlistB)

print(suisen)
mod_suisen = list()
for key, val in suisen.items():
    mod_suisen.append(key)

with open('C:\\Users\\Ryo Taguchi\\Desktop\\processing_suisen\\data\\suisen.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)  # writerオブジェクトの生成
    writer.writerow(mod_suisen)  # 複数行に書き込み
csv_file.close()

process_time = time.time() - start
print(process_time)
