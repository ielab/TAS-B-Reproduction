
import glob
import os
import argparse
import time
from tqdm import tqdm
parser = argparse.ArgumentParser()

parser.add_argument('--input_folder', type=str, required=True)
parser.add_argument('--qrel', type=str, required=True)
parser.add_argument('--trec_eval', type=str, required=True)
parser.add_argument('--l', type=str, default="2")

args = parser.parse_args()

input_folder = args.input_folder

# for input_folder in tqdm(input_folders):
#     file_name = os.path.join(input_folder,"test_top1000orSomeOtherName-output.txt")
#     file_out = os.path.join(input_folder,"<msmarco>-output.trec")
#     qid_set = set()
#     did_list = []
#     if os.path.exists(file_out):
#           continue
#     if os.path.exists(file_name):
#         fw = open(file_out, 'w')
#         with open(file_name) as f:
#             for line in f:
#                 qid, did, rank, score = line.strip().split()
#                 if qid not in qid_set:
#                     qid_set.add(qid)
#                     did_list = []
#                 if did not in did_list:
#                     fw.write(f'{qid} 0 {did} {rank} {score} result\n')
#                     did_list.append(did)
# time.sleep(10)

measures = {"ndcg": "ndcg_cut.10",
            "mrr": "recip_rank -M 10",
            "recall": "recall.1000"
            }

for measure in measures:
    measure_w = measures[measure]
    file_name = os.path.join(input_folder,"<msmarco>-output.trec")
    qrel_name = args.qrel
    trec_eval = args.trec_eval
    l = args.l
    out_file = os.path.join(input_folder,measure + ".trec")
    command = f'{trec_eval} -q -l {l} -m {measure_w} "{qrel_name}" "{file_name}" > {out_file}'
    print(command)
    os.system(command)










