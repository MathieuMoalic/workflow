#!/bin/bash
file=$1
port=$(( $RANDOM % 10000 + 40000 ))
sbatch --job-name="${file/.mx3/}_port:$port" --output="${file/.mx3/}.logs" $HOME/scripts/mumax_job.sh $file $port