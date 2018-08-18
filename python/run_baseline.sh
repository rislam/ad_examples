#!/bin/bash

N_QUERY=2000
WEIGHTED_UPDATE=0
QUERY_STRATEGY=0
N_RUNS=10
STARTING=0
QUEUE="doppa"

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
OUTFILE="$directory/$prefix-out.txt"
ERRORFILE="$directory/$prefix-error.txt"
qsub -N "$prefix" -q $QUEUE -l walltime=48:00:00,mem=4gb,nodes=1:doppa:ppn=4 -o $OUTFILE -e $ERRORFILE -j oe -k oe -M mdrakibul.islam@wsu.edu -m bae -v QUERY_STRATEGY=${QUERY_STRATEGY},N_QUERY=${N_QUERY},N_RUNS=${N_RUNS},WEIGHTED_UPDATE=${WEIGHTED_UPDATE},STARTING=${STARTING} experiment.sh