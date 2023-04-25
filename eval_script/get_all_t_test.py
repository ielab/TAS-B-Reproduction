import glob
import os
import argparse
import time
from scipy import stats
from tqdm import tqdm
parser = argparse.ArgumentParser()

parser.add_argument('--input_folder', type=str, required=True)
parser.add_argument('--target', type=str, required=True)

args = parser.parse_args()

measures = {"ndcg": "ndcg_cut_10",
            "mrr": "recip_rank ",
            "recall": "recall_1000"
            }
parent_folder = args.input_folder + '/*'
child_folders = glob.glob(parent_folder)

result_file = ""
target_result = {}
all_other_result = {}

for child_folder in child_folders:
    result_dict = {}
    for m in measures:
        m_w = measures[m]
        rel_file = os.path.join(child_folder, m + '.trec')
        with open(rel_file) as f:
            for line in f:
                _, qid, result = line.strip().split()
                if qid =="all":
                    continue
                if m not in result_dict:
                    result_dict[m] = {}
                if qid not in result_dict[m]:
                    result_dict[m][qid] = float(result)

    if args.target in child_folder:
        target_result = result_dict
    else:
        all_other_result[child_folder] = result_dict


qid_list = list(target_result["ndcg"].keys())
target_final = {}
target_report_list = []
for m in measures:
    tem = []
    for qid in qid_list:
        tem.append(target_result[m][qid])
    target_report_list.append("{0:.3f}".format(sum(tem)/len(tem)))
    target_final[m] = tem
print(f'{args.target} & {" & ".join(target_report_list)}')


for child_folder in all_other_result:
    #print(child_folder)
    line = child_folder
    #final_report_list = []
    for m in measures:
        tem = []
        for qid in qid_list:
            tem.append(all_other_result[child_folder][m][qid])
        _, p = stats.ttest_ind(tem, target_final[m])
        if p<0.05:
          line += "&"  + "{0:.3f}".format(sum(tem)/len(tem)) + "$^{*}$"
        else:
            line += "& " + "{0:.3f}".format(sum(tem) / len(tem))
    print(line)




