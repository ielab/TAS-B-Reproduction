from tqdm import tqdm

collection_file = "/scratch/project/neural_ir/dylan/balance_training/esci-data-main/shopping_queries_dataset/collection_amazon.tsv"
query_file = "/scratch/project/neural_ir/dylan/balance_training/esci-data-main/shopping_queries_dataset/queries_train_amazon.tsv"
ensemble_file = "/scratch/project/neural_ir/dylan/balance_training/esci-data-main/shopping_queries_dataset/teacher_dynamic_scores.tsv"
out_train_tsv = open("/scratch/project/neural_ir/dylan/balance_training/esci-data-main/shopping_queries_dataset/triples_for_random.tsv", 'w')


query_dict = {}
with open(query_file) as f:
    for line in tqdm(f):
        qid, text = line.strip().split('\t')
        query_dict[qid] = text

collection_dict = {}
with open(collection_file) as f:
    for line in tqdm(f):
        qid, text = line.strip().split('\t')
        collection_dict[qid] = text

with open(ensemble_file) as f:
    for line in tqdm(f):
        pos, neg, qid, pid, nid = line.strip().split('\t')
        query = query_dict[qid]
        pp = collection_dict[pid]
        pn = collection_dict[nid]
        out_train_tsv.write(f'{pos}\t{neg}\t{query}\t{pp}\t{pn}\n')
