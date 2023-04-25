#!/bin/bash
#SBATCH -N 1
#SBATCH --job-name=balance_training
#SBATCH --mem-per-cpu=5G
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
name2=$2
python matchmaker/dense_retrieval.py search --run-name $name-$name2 --config config/dense_retrieval/$name.yaml config/dense_retrieval/dataset/$name2.yaml

