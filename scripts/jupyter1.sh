#!/bin/bash
port=$(( $RANDOM % 10000 + 40000 ))
sbatch --job-name="jupyter_port:$port" --output="$HOME/trash/jupyter.logs" $HOME/scripts/jupyter_job.sh $port