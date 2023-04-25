#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=100G
#SBATCH --job-name=balance_train
#SBATCH --partition=ai
#SBATCH --account=a_ielab
#SBATCH --gres=gpu:a100:1
#SBATCH --time=99:00:00
#SBATCH -o print.txt
#SBATCH -e error.txt


module load anaconda3/2022.05
module load cuda/11.7.0
source activate balance_train

name=$1

CUDA_VISIBLE_DEVICES=0 python3 matchmaker/eval.py --config-file config/train/defaults.yaml config/data/amazon_data.yaml config/train/models/$name.yaml --run-name $name


