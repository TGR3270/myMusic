import numpy as np
import matplotlib.pyplot as plt
from dtw import dtw
import matplotlib.cm as cm
x = np.array([0, 0, 1, 1, 2, 4, 2, 1, 2, 0]).reshape(-1, 1)
y = np.array([1, 1, 1, 2, 2, 2, 2, 3, 2, 0]).reshape(-1, 1)
plt.plot(x)
plt.plot(y)
plt.legend()
plt.show()
dist, cost, acc, path = dtw(
    x, y, dist=lambda x, y: np.linalg.norm(x - y, ord=1))
print('Minimum distance found:', dist)
plt.imshow(acc.T, origin='lower', cmap=cm.gray, interpolation='nearest')
plt.plot(path[0], path[1], 'w')
plt.xlim((-0.5, acc.shape[0]-0.5))
plt.ylim((-0.5, acc.shape[1]-0.5))
plt.show()
