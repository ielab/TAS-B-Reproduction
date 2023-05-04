# This is the reproduce code for the paper "Balanced Topic Aware Sampling for Effective Dense Retriever: A Reproducibility Study" by Shuai Wang and Guido Zuccon.


In our project, there are two datasets that's been used: [MS_MARCO_passage_ranking](https://microsoft.github.io/msmarco/Datasets.html) and [Amazon_shopping_queries](https://github.com/amazon-science/esci-data)

## To reproduce for MS_MARCO_passage_ranking

### Data preparation
1. Download the dataset from [MS_MARCO_passage_ranking](https://microsoft.github.io/msmarco/Datasets.html) and put it in the folder `dataset/msmarco/`. (You need: collection.tsv, all queries.tsv, all qrels.tsv, train_triples_qid_pid)
2. Download the pre-computed training scores from [ensemble scores](https://zenodo.org/record/4068216) and put it in the folder `dataset/msmarco/`.


### Run BM25 Baseline

1. Set-up [pyserini](https://github.com/castorini/pyserini)
2. Follow the instructions on [get bm25 score of MS marco passage ranking in pyserini](https://github.com/castorini/pyserini/blob/master/docs/experiments-msmarco-passage.md)
3. Put the output of top-100 BM25 results in the folder `dataset/msmarco/` and name it as `bm25-top-100-49k.tsv`.
4. Put the output of top-1000 BM25 results in the folder `dataset/msmarco/` and name it as `bm25-top-1000-49k.tsv`

### Train Baseline DR model

To train baseline DR model, do the following:
````
cd matchmaker
python3 matchmaker/train.py \
    --config-file config/train/defaults.yaml config/train/data/example-minial-dataset.yaml config/train/models/bert_dot.yaml \
    --run-name msmarco-baseline-model
````

## Inference Baseline DR model

To inference the baseline DR model, do the following:
````

python3 matchmaker/dense_retrieval.py encode+index+search \
   --run-name baseline_dr \
   --config config/dense_retrieval/base_setting.yaml config/dense_retrieval/dataset/msmarco_dev.yaml config/dense_retrieval/model/base.yaml
````
Remember to change model path in config/dense_retrieval/model/base.yaml to the trained model from above step.


## Early Stopping Generation

To seperate training file, run the following
````
cd matchmaker
python3 generate_smart_earlystopping_retrieval.py 
    --output-file ../dataset/msmarco/sampled_queries.tsv \
    --candidate-metric ../dataset/msmarco/baseline.metrics.tsv\
    --candidate-file ../dataset/msmarco/bm25-top-100-49k.tsv\
    --qrel ../dataset/msmarco/qrels.dev.small.tsv \
    --collection-file ../dataset/msmarco/collection.tsv \
    --query-file ../dataset/msmarco/queries.dev.small.tsv

````

## Query Clustering


### To train the distilled model
For model_choice: please see all available yaml files in config/train/modes/exp/
````
cd matchmaker
python3 matchmaker/train.py \
    --config-file config/train/defaults.yaml config/train/data/msmarco.yaml config/train/models/bert_dot.yaml config/train/modes/exp/{model_choice}.yaml \
    --run-name msmarco-${model_choice}
````

### To inference

Note: please specify the path of trained models in config/dense_retrieval/model/example.yaml
````
python3 matchmaker/dense_retrieval.py encode+index+search --run-name {cmodel_choice} \
        --config config/dense_rertrieval/base_setting.yaml config/dense_rertrieval/dataset/msmarco_dev.yaml config/dense_retrieval/model/example.yaml

````


## To reproduce for Amazon_shopping_queries

### Data preparation







# Train a Dense Retriever (BERT_DOT) with TAS-Balanced & Dual-Supervision

This guide builds up on: [dense_retrieval_train.md](dense_retrieval_train.md)

We again use a BERT_DOT with shared encoder: **bert_dot**

## TAS-Balanced

For the dataset config, see the *config/train/data/example-minimal-tasb-dataset.yaml*.

The config for TAS-Balanced input files:
````yaml
dynamic_query_file: "/path/to/train/queries.train.tsv"
dynamic_collection_file: "/path/to/train/collection.tsv"
dynamic_pairs_with_teacher_scores: "/path/to/train/T2-train-ids.tsv" # output of matchmaker/distillation/teacher_textscore_to_ids.py (from single model pairwise scores or the ensemble)
dynamic_query_cluster_file: "/path/to/train/train_clusters.tsv"      # generate it with matchmaker/distillation/query_clusterer.py (and a baseline dense retrieval model)
````

Example train command (cd in ir-project-matchmaker):
````
python matchmaker/train.py --config-file config/train/defaults.yaml config/train/data/<your dataset here>.yaml config/train/models/bert_dot.yaml config/train/modes/tas_balanced.yaml --run-name your_experiment_name
````

The dynamic_teacher will run on the same GPU as the main training (if you only have 1 GPU available) if you have more than 1 GPU available, the dynamic teacher will exclusively take the last GPU and the training the rest.


If you want to know more about the needed workflow to set up teacher scores & models: [distillation_workflow_dual-supervision.md](distillation_workflow_dual-supervision.md)

## Indexing & FAISS Vector Retrieval

If you want to know more about the evaluation options see: [dense_retrieval_evaluate.md](dense_retrieval_evaluate.md)