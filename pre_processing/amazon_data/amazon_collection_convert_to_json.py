import json
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str,help='input collection location', default="collection_amazon.tsv")
parser.add_argument('--output', type=str,help='output collection location', default="../../pyserini/collections/amazon/collection_amazon.jsonl")
args = parser.parse_args()

file_in = args.input


fw = open(args.output, 'w')

with open(file_in) as f:
    for line in tqdm(f):
        id, content = line.strip().split('\t')
        current_dict = {"id": id,
                        "contents": content}
        fw.write(json.dumps(current_dict) + '\n')

