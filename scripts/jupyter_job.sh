#!/bin/bash -l
#SBATCH --nodes=1
#SBATCH --ntasks-per-core=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=24G
#SBATCH --time=15:00:00
#SBATCH --partition=standard

jupyter lab --port=$1  