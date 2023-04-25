import glob
import os
import argparse
import copy
import scipy.stats
import time
from scipy import stats
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('--input_folder', type=str, required=True)
parser.add_argument('--qrel', type=str, required=True)
parser.add_argument('--l', type=str, default="2")

args = parser.parse_args()

test_2019_l = {}
test_2020_l = {}

file = "correlation_margin_msmarco"

with open(file) as f:
    for line in f:
        margin, val, test_ms, test_2019, test_2020 = line.strip().split()
        #val_l.append(float(val))
        #test_ms_l.append(float(test_ms))
        if margin!="tas":
            test_2019_l[int(margin)] = float(test_2019)
            test_2020_l[int(margin)] = float(test_2020)
        else:
            test_2019_l[margin] = float(test_2019)
            test_2020_l[margin] = float(test_2020)

if "2019" in args.input_folder:
    target_l = test_2019_l
else:
    target_l = test_2020_l

pos_dict = {}
neg_dict = {}



with open(args.qrel) as f:
    for line in f:
        qid, _, did,rel = line.strip().split()
        if qid not in pos_dict:
            pos_dict[qid] = []
            neg_dict[qid] = []
        if int(rel)>= int(args.l):
            pos_dict[qid].append(did)
        else:
            neg_dict[qid].append(did)


parent_folder = args.input_folder + '/*'
child_folders = glob.glob(parent_folder)

final_result_dict = {}
for i in range(1,11):
    final_result_dict[i] = 0
final_result_dict[15] = 0
final_result_dict[20] = 0
final_result_dict['tas'] = 0

sample_p = copy.deepcopy(pos_dict)
sample_dict = copy.deepcopy(neg_dict)

for child_folder in child_folders:
    file_out = os.path.join(child_folder,"<msmarco>-output.trec")
    result_dict = {}
    with open(file_out) as f:
        for line in f:
            qid,_,did,rank,score,_ = line.strip().split()
            if qid not in neg_dict:
                continue
            if qid not in result_dict:
                result_dict[qid] = []
            result_dict[qid].append(did)

    for qid in sample_dict:
        sample_list = sample_dict[qid]
        sample_list_reformed = []
        for did in sample_list:
            if did in result_dict[qid]:
                sample_list_reformed.append(did)
        sample_dict[qid] = sample_list_reformed

    for qid in sample_p:
        sample_list = sample_dict[qid]
        sample_list_reformed = []
        for did in sample_list:
            if did in result_dict[qid]:
                sample_list_reformed.append(did)
        sample_dict[qid] = sample_list_reformed



for child_folder in child_folders:
    file_out = os.path.join(child_folder, "<msmarco>-output.trec")
    result_dict = {}

    with open(file_out) as f:
        for line in f:
            qid,_,did,rank,score,_ = line.strip().split()

            if qid not in neg_dict:
                continue

            if qid not in result_dict:
                result_dict[qid] = {}

            result_dict[qid][did] = float(score)


    score_dist_dict = {}
    for qid in result_dict:
        score_dist = max(result_dict[qid].values()) - min(result_dict[qid].values())
        score_dist_dict[qid] = score_dist


    top_rel_scores = {}
    for qid in result_dict:
        top_rel_scores[qid] = 1

    for qid in result_dict:
        dif = (max(result_dict[qid].values()) - min(result_dict[qid].values()))
        min_value = min(result_dict[qid].values())

        for did in result_dict[qid]:
            result_dict[qid][did] = (result_dict[qid][did]- min_value)/dif
            if (top_rel_scores[qid]==1) and (did in sample_p[qid]):
                top_rel_scores[qid] = result_dict[qid][did]

    margin_list = []

    for qid in result_dict:
        for did in sample_dict[qid]:
            margin_list.append((1-result_dict[qid][did])/score_dist_dict[qid])

    for i in final_result_dict:
        if f"_{i}_" in child_folder:
            final_result_dict[i] = sum(margin_list)/len(margin_list)


for i in final_result_dict:
    print(i, final_result_dict[i])


fig, ax = plt.subplots()
fig.set_size_inches(9, 5)
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]
y = []
for i in x:
    y.append(target_l[i])

ax.set_xlim(1,10)

ax.set_xlabel(r'Hard Margin $M_{max}$', fontsize=14)
ax.set_ylabel(r'ndcg@10', fontsize=14, color='#1f77b4')

ax.tick_params(axis='both', which='major', labelsize=11, color='#1f77b4', labelcolor='#1f77b4')
ax.set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20], color='black')

l1, = ax.plot(x, y, color='#1f77b4')
ax.hlines(y = target_l["tas"], xmin = min(x), xmax= max(x),  color = '#1f77b4', linestyle = '--')

ax2 = ax.twinx()
y2 = []

for i in x:
    y2.append(final_result_dict[i])
l2, = ax2.plot(x, y2, color='red')
ax2.set_ylabel(r'Inference Margin Distance', fontsize=14, color='red')
ax2.tick_params(color='red', labelcolor='red')
ax2.hlines(y = final_result_dict["tas"], xmin = min(x), xmax= max(x),color = 'red', linestyle = '--')

cor = scipy.stats.pearsonr(y, y2)
print(cor)


if "2019" in args.input_folder:
    plt.title("TREC DL 2019", size=18)
    plt.tight_layout()
    plt.savefig("2019_hm.pdf")
else:
    plt.title("TREC DL 2020", size=18)
    plt.tight_layout()
    plt.savefig("2020_hm.pdf")



#plt.show()






#
#

