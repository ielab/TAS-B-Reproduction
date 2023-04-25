

a=$1

python3 generate_validation_input_from_candidate_set.py \
--out-file /scratch/itee/uqswan37/balance_training/dataset/msmarco/queries.dev_49k_input_sampled$a.tsv \
--candidate-file "/scratch/itee/uqswan37/balance_training/TAS-query-original/2023-01-10_1013_baseline_for_query/<msmarco>-output.txt" \
--collection-file /scratch/itee/uqswan37/balance_training/dataset/msmarco/collection.tsv \
--query-file /scratch/itee/uqswan37/balance_training/dataset/msmarco/queries.dev_49k_sampled$a.tsv \
--top 100