import argparse
from tqdm import tqdm
parser = argparse.ArgumentParser()
parser.add_argument('--queries_file', type=str, required=True)
parser.add_argument('--qrel_file', type=str, required=True)
parser.add_argument('--collection', type=str, required=True)
parser.add_argument('--output', type=str, required=True)

args = parser.parse_args()

rel_dict = {}
with open(args.qrel_file) as f:
    for line in tqdm(f):
        qid,_,did,rel = line.split()
        if int(rel)>=1:
            if qid not in rel_dict:
                rel_dict[qid] = []
            rel_dict[qid].append(did)
collection_dict = {}
with open(args.collection) as f:
    for line in tqdm(f):
        did, text = line.split('\t', 1)
        collection_dict[did] = text

with open(args.output,'w') as fw:
    with open(args.queries_file) as f:
        for line in tqdm(f):
            qid, text = line.split('\t')
            if qid in rel_dict:
                rel_list = rel_dict[qid]
                new_text = collection_dict[rel_list[0]].strip()
                fw.write(qid + '\t' + new_text+'\n')


