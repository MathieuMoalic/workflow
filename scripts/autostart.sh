#!/bin/bash
for file in *.mx3; do 
    echo $file
    port=$(( $RANDOM % 10000 + 40000 ))
    sbatch --job-name="${file/.mx3/}_port:$port" --output="${file/.mx3/}.logs" $HOME/scripts/mumax_job.sh $file $port
done