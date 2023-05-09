import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from datasets import load_dataset
import argparse
from tqdm import tqdm
from torch.utils.data import Dataset
import datasets
import torch
from transformers import DataCollatorWithPadding
from torch.utils.data import DataLoader

parser = argparse.ArgumentParser()
parser.add_argument('--input_file', type=str, default="/scratch/project/neural_ir/dylan/balance_training/esci-data-main/shopping_queries_dataset/triples_input_for_scoring.csv")
parser.add_argument('--output_triples_with_scores', type=str, default="/scratch/project/neural_ir/dylan/balance_training/esci-data-main/shopping_queries_dataset/train")
parser.add_argument('--model', type=str, required=True)
parser.add_argument('--batch_size', type=int, required=True)
args = parser.parse_args()

class Processor:
    def __init__(self, tokenizer, max_length=32):
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __call__(self, example):
        docid = example['id']
        text = example['text']
        tokenized = self.tokenizer(text, return_tensors="pt", truncation=True, max_length =self.max_length)
        return {'id': docid,
                'input_ids': tokenized["input_ids"][0],
                'attention_mask': tokenized["attention_mask"][0]}
#
class EncodeDataset(Dataset):
    def __init__(self, dataset: datasets.Dataset, max_len=128):
        self.dataset = dataset
        self.max_len = max_len

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, item):
        docid = self.dataset[item]['id']
        input_ids = self.dataset[item]['input_ids']
        attention_mask = self.dataset[item]['attention_mask']
        return docid, {'input_ids': input_ids, "attention_mask": attention_mask}
#
#
class EncodeCollator(DataCollatorWithPadding):
    def __call__(self, features):
        docids = [x[0] for x in features]
        text_features = [x[1] for x in features]
        collated_features = super().__call__(text_features)
        return docids, collated_features

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
tokenizer = AutoTokenizer.from_pretrained(args.model, cache_dir = "cache")
pretrained_model = AutoModelForSequenceClassification.from_pretrained(args.model).to(device)


dataset = load_dataset('csv', data_files=args.input_file, split='train', cache_dir='cache')

dataset = dataset.map(Processor(tokenizer, 32), remove_columns=dataset.column_names, num_proc=4)

encode_dataset = EncodeDataset(dataset)

encode_loader = DataLoader(
        encode_dataset,
        batch_size=args.batch_size,
        collate_fn=EncodeCollator(
            tokenizer,
            max_length=128,
            padding='max_length'
        ),
        shuffle=False,
        drop_last=False,
        num_workers=10
)


#out = []
#lookup_indices = []

with open(args.output_triples_with_scores + args.model.replace("/", "_") + '.tsv', 'w') as fw:
    with torch.no_grad():
        for docids, batch_inputs in tqdm(encode_loader):
            #lookup_indices.extend(docids)
            batch_inputs = batch_inputs.to(device)
            batch_logits = pretrained_model(**batch_inputs).logits
            scores = torch.nn.functional.softmax(batch_logits, dim=1)[:,-1]
            for docid, score in zip(docids, scores):
                fw.write(f'{docid}\t{float(score)}\n')

            #out.extend(indexs)


# for cls, id in zip(out, lookup_indices):
#     if cls not in out_classes:
#         out_classes[cls] = []
#     out_classes[cls].append(str(id))
#
#
# with open(args.output_clusters, 'w') as fw:
#     for cls in range(0, len(out_classes)):
#         fw.write('\t'.join(out_classes[cls]) + '\n')