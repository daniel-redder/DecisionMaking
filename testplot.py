#Daniel R
#This code is to make a test plot for our project proposal

import seaborn as sns
import matplotlib.pyplot as plt

data = [69940, 5256, 2974, 19786, 88858, 11057, 58189, 42356, 17286, 56191, 15607, 21576, 6066, 80136, 95398, 36087, 22799
    , 42797, 22182, 58190, 60962, 22913, 37930, 57766, 86946, 0]

data = [x/10000 for x in data]

names = [f'{x}_AI' for x in range(len(data))]


print(len(data),len(names))
plt.xlabel("model name")
plt.ylabel("# of times model proposed a trade on average (across 10,000 games)")
plt.scatter(names,data)

plt.show()