import argparse
from tqdm import tqdm
parser = argparse.ArgumentParser()
parser.add_argument('--queries_file', type=str, required=True)
parser.add_argument('--output', type=str, required=True)


args = parser.parse_args()
qid_set = set()
did_list = []
with open(args.output, 'w') as fw:
    with open(args.queries_file) as f:
        for line in tqdm(f):
            qid,did,rank,score = line.strip().split()
            if qid not in qid_set:
                qid_set.add(qid)
                did_list = []
            if did not in did_list:
                fw.write(f'{qid} Q0 {did} {rank} {score} rank\n')
                did_list.append(did)


