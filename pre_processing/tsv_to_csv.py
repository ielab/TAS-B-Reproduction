# Python program to convert .tsv file to .csv file
# importing re library

import argparse
from tqdm import tqdm



parser = argparse.ArgumentParser()
parser.add_argument('--inp', type=str, required=True)
parser.add_argument('--out', type=str, required=True)

args = parser.parse_args()

# reading given tsv file
import pandas as pd

tsv_file = args.inp

# reading given tsv file
csv_table = pd.read_table(tsv_file, sep='\t', names=["id", "text"])

# converting tsv file into csv

csv_table.to_csv(args.out, index=False)

# output
print("Successfully made csv file")
