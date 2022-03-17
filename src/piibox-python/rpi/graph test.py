import numpy as np
import matplotlib.pyplot as plt

xData = np.arange(0, 10, 1)
yData1 = xData.__pow__(2.0)
yData2 = np.arange(15, 61, 5)
plt.figure(num=1, figsize=(8, 6))
plt.title('Plot 1', size=14)
plt.xlabel('x-axis', size=14)
plt.ylabel('y-axis', size=14)
plt.plot(xData, yData1, color='b', linestyle='--', marker='o', label='y1 data')
plt.plot(xData, yData2, color='r', linestyle='-', label='y2 data')
plt.legend(loc='upper left')
plt.show()
plt.savefig('static/img/plot1.png')

#from matplotlib import pyplot as plt
# x = [3, 6, 9]
# y = [2, 4, 6]
# plt.plot(x, y)
# plt.show()
# plt.savefig('timmytest.png')