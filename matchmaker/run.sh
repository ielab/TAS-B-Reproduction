#!/bin/bash
#SBATCH -N 1
#SBATCH --job-name=balance_training
#SBATCH --mem-per-cpu=10G
#SBATCH -o logs/print_2018.txt
#SBATCH -e logs/error_2018.txt
#SBATCH --partition=gpu
#SBATCH --gres=gpu:tesla-smx2:1
#SBATCH --cpus-per-task=5


module load anaconda/3.6
module load cuda/10.2.89.440
#
source activate /scratch/itee/uqswan37/balance_training/envs/
#
name=$1
sample=$2


python matchmaker/train.py --config-file config/train/defaults.yaml config/train/data/${put_your_dataset_name}.yaml config/train/models/bert_dot.yaml config/train/modes/exp/$name.yaml --run-name $name-${sample}





