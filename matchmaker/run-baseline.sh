#!/bin/bash
#SBATCH -N 1
#SBATCH --job-name=balance_training
#SBATCH --mem-per-cpu=20G
#SBATCH -o logs/print_2018.txt
#SBATCH -e logs/error_2018.txt
#SBATCH --partition=gpu
#SBATCH --gres=gpu:tesla-smx2:3
#SBATCH --cpus-per-task=10


module load anaconda/3.6
module load cuda/10.2.89.440
#
source activate /scratch/itee/uqswan37/balance_training/envs/
#


CUDA_VISIBLE_DEVICES=0,1,2 python3 matchmaker/dense_retrieval.py encode+index+search --run-name baseline_for_query --config /scratch/itee/uqswan37/balance_training/matchmaker/config/dense_retrieval/dense.yaml