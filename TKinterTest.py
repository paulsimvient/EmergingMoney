import matplotlib.pyplot as plt
import numpy as np

length=np.random.random(10)
length.sort()
time=np.random.random(10)
time.sort()
slope,intercept=np.polyfit(np.log(length),np.log(time),1)
print(slope)
plt.plot(length,time,'--')
plt.show()