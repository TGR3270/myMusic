import librosa
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import librosa.display
from dtw import dtw
from numpy.linalg import norm
import os

y1, sr1 = librosa.load(
    'C:\PythonFile\kenkyu_sotsuron\phrase\\testDemo1.wav')
y2, sr2 = librosa.load(
    'C:\PythonFile\kenkyu_sotsuron\phrase\\test1.wav'
)
mfcc1 = librosa.feature.mfcc(y1, sr1)
mfcc2 = librosa.feature.mfcc(y2, sr2)

plt.subplot(1, 2, 1)
mfcc1 = librosa.feature.mfcc(y1, sr1)
librosa.display.specshow(mfcc1)

plt.subplot(1, 2, 2)
mfcc2 = librosa.feature.mfcc(y2, sr2)
librosa.display.specshow(mfcc2)

plt.show()

dist, cost, acc_cost, path = dtw(
    mfcc1.T, mfcc2.T, dist=lambda x, y: norm(x - y, ord=1))
print('distance between the two sounds:', dist)

plt.imshow(cost.T, origin='lower', cmap=cm.gray, interpolation='nearest')
plt.plot(path[0], path[1], 'w')
plt.xlim((-0.5, cost.shape[0]-0.5))
plt.ylim((-0.5, cost.shape[1]-0.5))
plt.show()
'''
files = os.listdir("C:\PythonFile\kenkyu_sotsuron\phrase")
for file in files:
    print(file)
    y1, sr1 = librosa.load(
        'C:\PythonFile\kenkyu_sotsuron\phrase\Ex-01_a_Main.wav')
    file = 'C:\PythonFile\kenkyu_sotsuron\phrase\\' + file
    y2, sr2 = librosa.load(file)
    mfcc1 = librosa.feature.mfcc(y1, sr1)
    mfcc2 = librosa.feature.mfcc(y2, sr2)
    dist, cost, acc_cost, path = dtw(
        mfcc1.T, mfcc2.T, dist=lambda x, y: norm(x - y, ord=1))
    print(file, ' ', 'Normalized distance between the two sounds:', dist)



plt.subplot(1, 2, 1)
mfcc1 = librosa.feature.mfcc(y1, sr1)
librosa.display.specshow(mfcc1)

plt.subplot(1, 2, 2)
mfcc2 = librosa.feature.mfcc(y2, sr2)
librosa.display.specshow(mfcc2)

plt.show()


dist, cost, acc_cost, path = dtw(
    mfcc1.T, mfcc2.T, dist=lambda x, y: norm(x - y, ord=1))
print('Normalized distance between the two sounds:', dist)

plt.imshow(cost.T, origin='lower', cmap=cm.gray, interpolation='nearest')
plt.plot(path[0], path[1], 'w')
plt.xlim((-0.5, cost.shape[0]-0.5))
plt.ylim((-0.5, cost.shape[1]-0.5))
plt.show()
'''
