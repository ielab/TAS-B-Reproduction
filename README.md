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

### Inference Baseline DR model

To inference the baseline DR model for msmarco_dev 49k, do the following:
````
python3 matchmaker/dense_retrieval.py encode+index+search \
   --run-name baseline_dr_49k \
   --config config/dense_retrieval/base_setting.yaml config/dense_retrieval/dataset/msmarco_dev_49k.yaml config/dense_retrieval/model/base.yaml
````
Remember to change model path in config/dense_retrieval/model/base.yaml to the trained model from above step.

Then generate evaluation using the following: 

````
cd ..
python3 pre_processing/all_result_to_trec_n_evaluate.py \
    --input_folder TAS-query-original/baseline_dr_49k #Please Specify the inferenced folder adress from the last step \
    --qrel dataset/msmarco/qrel.dev.tsv \
    --trec_eval trec_eval/trec_eval  #Please Do specify the location of your trec_eval in your system
````

### Early Stopping Generation
To seperate training file, run the following
````
cd matchmaker
python3 generate_smart_earlystopping_retrieval.py 
    --output-file ../dataset/msmarco/sampled_queries.tsv \
    --candidate-metric ../TAS-query-original/baseline_dr_49k/ndcg.trec \
    --candidate-file ../dataset/msmarco/bm25-top-100-49k.tsv\
    --qrel ../dataset/msmarco/qrels.dev.small.tsv \
    --collection-file ../dataset/msmarco/collection.tsv \
    --query-file ../dataset/msmarco/queries.dev.small.tsv
````

### Query Clustering
Run the following code for query clustering preprocessing
````
python3 matchmaker/distillation/query_clusterer.py 
    --run-name msmarco_query_clustered \
    --config-file config/train/defaults.yaml config/train/cluster_model.yaml
````
The expected outcome includes two files: cluster-assignment-ids.tsv and cluster-assignment-text.tsv.


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
On the other hand, creating your own yaml file is also possible. Please refer to the example.yaml for the format.
````
python3 matchmaker/dense_retrieval.py encode+index+search --run-name {cmodel_choice} \
        --config config/dense_rertrieval/base_setting.yaml config/dense_rertrieval/dataset/msmarco_dev.yaml config/dense_retrieval/model/example.yaml
````

Note, you can also change the dataset by changing the msmarco_dev.yaml to trec_dl_2019.yaml or trec_dl_2020.yaml


## To reproduce for Amazon_shopping_queries

### Data preparation

Download data from [Amazon_shopping_queries](https://github.com/amazon-science/esci-data)

````
git clone https://github.com/amazon-science/esci-data.git
mv esci-data/shopping_queries_dataset/* dataset/amazon/
````

First pre-process the data by running the following code:

````
python3 pre_processing/amazon_data/get_amazon_task1.py --folder dataset/amazon/
````

Then for documents, further process using the following code

````
python3 pre_processing/amazon_data/amazon_collection_convert_to_json.py \
    --input dataset/amazon/collection_amazon.tsv \
    --output dataset/amazon/collection_amazon.json
````

### Query Clustering
Run the following code for query clustering preprocessing
````
python3 matchmaker/distillation/query_clusterer.py 
    --run-name amazon_query_clustered \
    --config-file config/train/defaults.yaml config/train/cluster_model_amazon.yaml
````


### Train the baseline DR model

Start to train the baseline DR model by running the following code:

````
cd matchmaker
python3 matchmaker/train.py \
    --config-file config/train/defaults.yaml config/train/data/amazon_data.yaml config/train/models/bert_dot.yaml \
    --run-name amazon_baseline_model
````



### Inference the baseline DR model

````
python3 matchmaker/dense_retrieval.py encode+index+search \
   --run-name baseline_dr_amazon \
   --config config/dense_retrieval/base_setting.yaml config/dense_retrieval/dataset/amazon_train.yaml config/dense_retrieval/model/base.yaml
````


### Get teacher emsembled scores

To get teacher emsembled scores, first, you need to get scores of training queries using BERT, ALBERT, and BERT-LARGE

First, preprocess the data by running the following code:

````
python3 pre_processing/amazon_data/create_qid_pid_triples.py 
    --input_qrel dataset/amazon/qrels.train_amazon.tsv \
    --output_triples_with_scores dataset/amazon/triples_train.tsv

python3 pre_processing/amazon_data/generate_scoring_file.py 
    --queries_file dataset/amazon/queries_train_amazon.tsv\
    --collection_file dataset/qrel.train_amazon.tsv \
    --input_triples dataset/amazon/triples_train.tsv \
    --output_scoring_file dataset/amazon/scoring_file.tsv
````
change train to valid/test to preprocess the data for validation/test set

Then, run the following code to get scores of training queries using BERT, ALBERT, and BERT-LARGE

````
python3 pre_processing/amazon_data/run_teacher_scores.py 

python3 pre_processing/amazon_data/fusing_teacher_scorings.py
````

### Train the distilled model
For model_choice: please see all available yaml files in config/train/modes/exp/
````
cd matchmaker
python3 matchmaker/train.py \
    --config-file config/train/defaults.yaml config/train/data/amazon_data.yaml config/train/models/bert_dot.yaml config/train/modes/exp/{model_choice}.yaml \
    --run-name amazon-${model_choice}
````

### To inference

Note: please specify the path of trained models in config/dense_retrieval/model/example.yaml
On the other hand, creating your own yaml file is also possible. Please refer to the example.yaml for the format.
````
python3 matchmaker/dense_retrieval.py encode+index+search --run-name {model_choice} \
        --config config/dense_rertrieval/base_setting.yaml config/dense_rertrieval/dataset/amazon_data.yaml config/dense_retrieval/model/example.yaml
````



# Below is the code instruction from original paper that you may find helpful

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
