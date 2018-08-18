#!/bin/bash

cd $directory
module load python/3.5.1
source ~/py35_venv/bin/activate

echo
echo "Starting the experiments"
echo
python -m baseline.malware.baseline_experiments --filedir "" --datafile "/data/doppa/users/mislam1/datasets/anomaly/malware-complete/fullsamples/malware-complete_1.csv" --query_strategy $QUERY_STRATEGY --n_query $N_QUERY --n_runs $N_RUNS --weighted_update $WEIGHTED_UPDATE --starting $STARTING

echo
echo "Job completed ..."
echo