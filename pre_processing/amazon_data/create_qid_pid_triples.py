from tqdm import tqdm
import argparse


parser = argparse.ArgumentParser()

parser.add_argument('--input_file', type=str, default="/Users/shuaiwang/workspace/2023s1PHD/extra/Balance_training/esci-data-main/shopping_queries_dataset/triples_input_for_scoring.csv")
parser.add_argument('--output_triples_with_scores', type=str, default="/Users/shuaiwang/workspace/2023s1PHD/extra/Balance_training/esci-data-main/shopping_queries_dataset/train")

args = parser.parse_args()

rel_dict_positive = {}
rel_dict_negative = {}

qrel_file = "/esci-data-main/shopping_queries_dataset/qrels.train_amazon.tsv"

out_triples = "/Users/shuaiwang/workspace/2023s1PHD/extra/Balance_training/esci-data-main/shopping_queries_dataset/triples_qid.tsv"



with open(qrel_file) as f:
    for line in f:
        qid,_,did,rel = line.strip().split('\t')
        if int(rel) == 1:
            if qid not in rel_dict_positive:
                rel_dict_positive[qid] =[]
            rel_dict_positive[qid].append(did)
        else:
            if qid not in rel_dict_negative:
                rel_dict_negative[qid] = []
            rel_dict_negative[qid].append(did)

with open(out_triples, 'w') as fw:
    for qid in tqdm(rel_dict_positive):
        if qid not in rel_dict_positive:
            continue
        positive_list = rel_dict_positive[qid]
        if qid not in rel_dict_negative:
            continue
        negative_list = rel_dict_negative[qid]
        print(len(positive_list), len(negative_list))
        for did in positive_list:
            for didn in negative_list:
                fw.write(f'{qid}\t{did}\t{didn}\n')


