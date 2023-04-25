import math
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import seaborn as sns
import scipy.stats


file = "../correlation_margin_msmarco"

val_l = []
test_ms_l = []
test_2019_l = []
test_2020_l = []

with open(file) as f:
    for line in f:
        margin, val, test_ms, test_2019, test_2020 = line.strip().split()
        val_l.append(float(val))
        test_ms_l.append(float(test_ms))
        test_2019_l.append(float(test_2019))
        test_2020_l.append(float(test_2020))


plt.figure()
plt.scatter(val_l, test_ms_l)

c_m = scipy.stats.pearsonr(val_l, test_ms_l)

plt.plot(np.unique(val_l),
         np.poly1d(np.polyfit(val_l, test_ms_l, 1))
         (np.unique(val_l)), color='red')
plt.xlabel('ndcg@10 validation', size=16)
plt.ylabel('ndcg@10 MS MARCO dev', size=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

cor = "{:10.4f}".format(c_m[0])

plt.text(0.47, 0.385,f"coefficient={cor}", fontsize=15)
plt.tight_layout()
plt.savefig("msmarco_dev_correlation.pdf")
plt.close()

plt.figure()

plt.scatter(val_l, test_2019_l)
plt.plot(np.unique(val_l),
         np.poly1d(np.polyfit(val_l, test_2019_l, 1))
         (np.unique(val_l)), color='red')
c_2019 = scipy.stats.pearsonr(val_l, test_2019_l)
cor = "{:10.4f}".format(c_2019[0])

plt.text(0.465, 0.665 ,f"coefficient={cor}", fontsize=15)
plt.xlabel('ndcg@10 validation', size=16)
plt.ylabel('ndcg@10 TREC DL 2019',size=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.tight_layout()
#plt.show()
plt.savefig("dl2019_correlation.pdf")
plt.close()


plt.figure()
plt.scatter(val_l, test_2020_l)
plt.plot(np.unique(val_l),
         np.poly1d(np.polyfit(val_l, test_2020_l, 1))
         (np.unique(val_l)), color='red')
c_2020 = scipy.stats.pearsonr(val_l, test_2020_l)

plt.xlabel('ndcg@10 validation', size=16)
plt.ylabel('ndcg@10 TREC DL 2020', size=16)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
cor = "{:10.4f}".format(c_2020[0])
plt.text(0.47, 0.66 ,f"coefficient={cor}", fontsize=15)
plt.tight_layout()
plt.savefig("dl2020_correlation.pdf")
plt.close()
