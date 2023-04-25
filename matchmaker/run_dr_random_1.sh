#!/bin/bash
#SBATCH -N 1
#SBATCH --job-name=balance_training
#SBATCH --mem-per-cpu=10G
#SBATCH -o logs/print_2018.txt
#SBATCH -e logs/error_2018.txt
#SBATCH --partition=gpu
#SBATCH --gres=gpu:tesla-smx2:1
#SBATCH --cpus-per-task=10


module load anaconda/3.6
module load cuda/10.2.89.440
#
source activate /scratch/itee/uqswan37/balance_training/envs/
#


name=$1

python matchmaker/dense_retrieval.py encode+index+search --run-name $name-dr-1 --config config/dense_retrieval/uniform_1/$name.yaml