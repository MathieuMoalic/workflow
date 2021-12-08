#!/bin/bash -l
#SBATCH --nodes=1
#SBATCH --mem=4G
#SBATCH --time=15:00:00
#SBATCH --partition=tesla 
#SBATCH --gres=gpu:1
#SBATCH --exclude=gpu09

module load cuda/10.2.89_440.33.01
TMPDIR="/mnt/storage_2/scratch/grant_398/mumax_kernels/"
file=$1
$HOME/go/bin/amumax -http=":$2" -cache="/mnt/storage_2/scratch/grant_398/mumax_kernels/" $file
mv "${file/.mx3/}.logs" "${file/.mx3/.out}/slurm.logs"
# this bit removes the port at the end of the name of the 
from=$file
re='(.+)_port[0-9]'
while [[ $hello =~ $re ]]; do
  hello=${BASH_REMATCH[1]}
done