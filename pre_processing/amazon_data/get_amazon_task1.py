import pandas as pd
from tqdm import tqdm
import random
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--folder', type=str,help='folder', default="")
args = parser.parse_args()

input_folder = args.folder
random.seed(1)


df_examples = pd.read_parquet(os.path.join(input_folder, 'shopping_queries_dataset_examples.parquet'))
df_products = pd.read_parquet(os.path.join(input_folder, 'shopping_queries_dataset_products.parquet'))


df_examples = df_examples[df_examples["small_version"] == 1]

df_products_us = df_products[df_products["product_locale"]=="us"]
df_examples_us = df_examples[df_examples["product_locale"]=="us"]
df_examples_train_valid = df_examples_us[df_examples_us["split"]=="train"]
df_examples_test = df_examples_us[df_examples_us["split"]=="test"]


collection_file = os.path.join(input_folder, "collection_amazon.tsv")
#

with open(collection_file, 'w') as f:
    for index, row in tqdm(df_products_us.iterrows()):
        f.write(f'{row["product_id"]}\t{row["product_title"]}\n')


queries_train_file = os.path.join(input_folder, "queries_train_amazon.tsv")
qrel_train_file = os.path.join(input_folder, "qrels.train_amazon.tsv")
queries_validation = os.path.join(input_folder, "queries_valid_amazon.tsv")
qrel_valid_file = os.path.join(input_folder, "qrels.valid_amazon.tsv")
queries_test = os.path.join(input_folder, "queries_test_amazon.tsv")
qrel_test_file = os.path.join(input_folder, "qrels.test_amazon.tsv")


w1 = open(queries_train_file, 'w')
w2 = open(queries_validation, 'w')
w3 = open(qrel_train_file, 'w')
w4 = open(qrel_valid_file, 'w')

w5 = open(queries_test, 'w')
w6 = open(qrel_test_file, 'w')

esci_label2gain = {
    'E': 1.0,
    'S': 0.1,
    'C': 0.01,
}

qid_train_valid = set()
title_dict = {}
did_dict = {}
for index, row in df_examples_train_valid.iterrows():
    qid = row["query_id"]
    qid_train_valid.add(qid)
    title_dict[qid] = row["query"]
    if row["esci_label"] in esci_label2gain:
        label = 1
    else:
        label = 0
    product_id = row["product_id"]

    if qid not in did_dict:
        did_dict[qid] = {}
    did_dict[qid][product_id] = label


qid_valid = random.sample(list(qid_train_valid), k=3200)
print(len(set(qid_valid)))
#
for qid in tqdm(qid_train_valid):
    if qid not in qid_valid:
        w1.write(f'{qid}\t{title_dict[qid]}\n')
        did_current = did_dict[qid]
        for did in did_current:
            w3.write(f'{qid}\t0\t{did}\t{did_current[did]}\n')
    else:
        w2.write(f'{qid}\t{title_dict[qid]}\n')
        did_current = did_dict[qid]
        for did in did_current:
            w4.write(f'{qid}\t0\t{did}\t{did_current[did]}\n')
#
#


test_ids = set()
title_dict_test = {}
did_dict_test = {}

for index, row in df_examples_test.iterrows():
    qid = row["query_id"]

    test_ids.add(qid)
    title_dict_test[qid] = row["query"]
    if row["esci_label"] in esci_label2gain:
        label = 1
    else:
        label = 0
    product_id = row["product_id"]

    if qid not in did_dict_test:
        did_dict_test[qid] = {}
    did_dict_test[qid][product_id] = label

for qid in tqdm(test_ids):
    w5.write(f'{qid}\t{title_dict_test[qid]}\n')
    did_current = did_dict_test[qid]
    for did in did_current:
        w6.write(f'{qid}\t0\t{did}\t{did_current[did]}\n')

