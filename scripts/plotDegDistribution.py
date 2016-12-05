import pickle
from collections import defaultdict
import matplotlib
import matplotlib.pyplot as plt

outdist = pickle.load(open('../datastructures/outDegDist.p'))
indist = pickle.load(open('../datastructures/inDegDist.p'))

outdist_sorted = []
for key in outdist:
    outdist_sorted.append((key,outdist[key]))

indist_sorted = []
for key in indist:
    indist_sorted.append((key,indist[key]))


outdist_sorted.sort(key=lambda tup: tup[0])
indist_sorted.sort(key=lambda tup: tup[0])

x_out = []
y_out = []
for deg,dist in outdist_sorted:
    x_out.append(deg)
    y_out.append(dist)

x_in = []
y_in = []
for deg,dist in indist_sorted:
    x_in.append(deg)
    y_in.append(dist)


# font = {'size'   : 24}
# matplotlib.rc('font', **font)

plt.loglog(x_out,y_out,label="Out Degree Distribution",color='red')
plt.loglog(x_in,y_in,label="In Degree Distribution",color='blue')
plt.legend()
plt.savefig('degdist.png')
