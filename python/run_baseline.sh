#!/bin/bash

N_QUERY=2000
WEIGHTED_UPDATE=0
QUERY_STRATEGY=0
N_RUNS=10
STARTING=0
QUEUE="doppa"
N_PT=1

if [ "$QUERY_STRATEGY" -eq 0 ]; then
   query_strategy="us_qs"
elif [ "$QUERY_STRATEGY" -eq 1 ]; then
   query_strategy="grd_qs"
elif [ "$QUERY_STRATEGY" -eq 2 ]; then
   query_strategy="dvrs_qs"
elif [ "$QUERY_STRATEGY" -eq 3 ]; then
    query_strategy="es_qs"
fi


prefix="$query_strategy-pt-$N_PT-fbcount-$N_QUERY-base-RF-starting-$STARTING-weighted_update-$WEIGHTED_UPDATE-nruns-$N_RUNS"
echo $prefix
DIRECTORY="/home/mislam1/icse/ad_examples/python"
OUTFILE="$DIRECTORY/$prefix-out.txt"
ERRORFILE="$DIRECTORY/$prefix-error.txt"
qsub -N "$prefix" -q $QUEUE -l walltime=48:00:00,mem=4gb,nodes=1:doppa:ppn=4 -o $OUTFILE -e $ERRORFILE -j oe -k oe -M mdrakibul.islam@wsu.edu -m bae -v QUERY_STRATEGY=${QUERY_STRATEGY},N_QUERY=${N_QUERY},N_RUNS=${N_RUNS},WEIGHTED_UPDATE=${WEIGHTED_UPDATE},STARTING=${STARTING},DIRECTORY=${DIRECTORY},N_PT=${N_PT} experiment.sh