
for VARIABLE in 1 2 3 4 5 6
do
   python3 preprocessing/generate_validation_input_from_candidate_set.py --out-file /scratch/itee/uqswan37/balance_training/dataset/msmarco/queries.dev_49k_input_sampled$VARIABLE.tsv --candidate-file /scratch/itee/uqswan37/balance_training/dataset/msmarco/qrels.dev.tsv --collection-file /scratch/itee/uqswan37/balance_training/dataset/msmarco/collection.tsv --query-file /scratch/itee/uqswan37/balance_training/dataset/msmarco/queries.dev_49k_sampled$VARIABLE.tsv --top-N 100
done
