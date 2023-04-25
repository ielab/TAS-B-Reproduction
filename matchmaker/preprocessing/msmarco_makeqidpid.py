q,p = {}, {}
queries = ['/scratch/project/neural_ir/dylan/balance_training/esci-data-main/shopping_queries_dataset/queries_train_amazon.tsv','/scratch/project/neural_ir/dylan/balance_training/esci-data-main/shopping_queries_dataset/queries_valid_amazon.tsv','/scratch/project/neural_ir/dylan/balance_training/esci-data-main/shopping_queries_dataset/queries_test_amazon.tsv']
with open('/scratch/project/neural_ir/dylan/balance_training/esci-data-main/shopping_queries_dataset/collection_amazon.tsv','r') as f:
    for l in f:
        l = l.strip()
        p[str(l.split('\t')[1:])[2:-2]] = l.split('\t')[0]
for file in queries:
    with open(file,'r') as f:
        for l in f:
            l = l.strip()
            q[str(l.split('\t')[1:])[2:-2]] = l.split('\t')[0]

with open ('triples.train.small.tsv', 'r') as f:
    with open('qidpidtriples.train.small.tsv','w') as w:
        for l in f:
            l = l.strip().split('\t')
            if l[0] in q and l[1] in p and l[2] in p:
                w.write('{}\t{}\t{}\n'.format(q[l[0]],p[l[1]],p[l[2]]))
