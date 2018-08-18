#!/bin/bash

N_QUERY=2000
WEIGHTED_UPDATE=0
QUERY_STRATEGY=0
N_RUNS=10
STARTING=0

if [ "$QUERY_STRATEGY" -eq 0 ]; then
   query_strategy="uncertainty_sampling"
elif [ "$QUERY_STRATEGY" -eq 1 ]; then
   query_strategy="greedy_query_strategy"
elif [ "$QUERY_STRATEGY" -eq 2 ]; then
   query_strategy="diverse_query_strategy"
elif [ "$QUERY_STRATEGY" -eq 3 ]; then
    query_strategy="entropy_sampling"
fi


prefix="$query_strategy-fbcount-$N_QUERY-base-RF-starting-$STARTING-weighted_update-$WEIGHTED_UPDATE-nruns-$N_RUNS"
echo $prefix
directory="~/icse/ad_examples/python"

#PBS -V
#PBS -N $prefix
#PBS -l nodes=1:doppa:ppn=4,walltime=48:00:00
#PBS -e "$directory/$prefix-error.txt"
#PBS -o "$directory/$prefix-out.txt"
#PBS -M mislam1@eecs.wsu.edu
#PBS -m abe
#PBS -q doppa
#PBS -l mem=4gb

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