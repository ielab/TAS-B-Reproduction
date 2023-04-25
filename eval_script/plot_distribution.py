import math

import matplotlib.pyplot as plt
from tqdm import tqdm
import seaborn as sns

file2 = "esci-data-main/shopping_queries_dataset/teacher_dynamic_scores.tsv"
#file1 = "esci-data-main/shopping_queries_dataset/teacher_dynamic_scores.tsv"
file1 = "/Users/shuaiwang/workspace/2023s1PHD/extra/Balance_training/Data_Sophia/bert_cat_ensemble_msmarcopassage_train_scores_ids.tsv"

file_dict = {file1:"MS MARCO",
             file2: "Amazon Shopping Queries"}

out = "esci-data-main/shopping_queries_dataset/a.pdf"
files = [file1, file2]

#data_margins = {}
plt.figure(figsize=(10, 6), dpi=80)

for file in files:

    data_margins = []
    with open(file) as f:
        for line in tqdm(f):
            ps, ns, qid, didp, didn = line.strip().split()
            if file == file2:
                margin = (float(ps) - float(ns))/3
            else:

                margin = float(ps)-float(ns)

            #if margin not in data_margins:
               # data_margins[margin] = 0
            data_margins.append(margin)

    #sorted_keys = sorted(data_margins.keys())

    sns.distplot(data_margins, hist=False, kde=True,
                 kde_kws={'fill': True, 'linewidth': 3},
                 label=file_dict[file])

    #plt.hist(data_margins, bins=math.ceil((max(data_margins)-min(data_margins))))
plt.legend(prop={'size': 16})
plt.xlabel('Margin Score', size=16)
plt.ylabel('Density', size=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig(out)


print(max(data_margins), min(data_margins))


