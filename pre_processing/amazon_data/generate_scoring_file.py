import argparse
import pandas as pd
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--queries_file', type=str, default="/scratch/project/neural_ir/dylan/balance_training/esci-data-main/shopping_queries_dataset/queries_train_amazon.tsv")
parser.add_argument('--collection_file', type=str,  default="/scratch/project/neural_ir/dylan/balance_training/esci-data-main/shopping_queries_dataset/collection_amazon.tsv")
parser.add_argument('--triple_file', type=str, default="/scratch/project/neural_ir/dylan/balance_training/esci-data-main/shopping_queries_dataset/triples_qid.tsv")
parser.add_argument('--out_file', type=str, default="/scratch/project/neural_ir/dylan/balance_training/esci-data-main/shopping_queries_dataset/triples_input_for_scoring.csv")
args = parser.parse_args()

query_dict ={}
with open(args.queries_file) as f:
    for line in tqdm(f):
        qid, text = line.strip().split('\t')
        query_dict[qid] = text

collection_dict = {}
with open(args.collection_file) as f:
    for line in tqdm(f):
        qid, text = line.strip().split('\t')
        collection_dict[qid] = text

triple_set = set()


with open(args.triple_file) as f:
    for line in tqdm(f):
        qid, did_p, did_n = line.strip().split('\t')
        triple_set.add(f'{qid}_{did_p}')
        triple_set.add(f'{qid}_{did_n}')

header = ['id', 'text']
data = []
for triple in tqdm(triple_set):
    qid, did = triple.split('_')
    data.append([triple, f'{query_dict[qid]}[SEP]{collection_dict[did]}'])
print(data[0])

data = pd.DataFrame(data, columns=header)
data.to_csv(args.out_file, index=False)
