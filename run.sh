#!/usr/bin/env bash

# example of the run script for running the fraud detection algorithm with a python file,
# but could be replaced with similar files from any major language

# I'll execute my programs, with the input directory paymo_input and output the files in the directory paymo_output
# @todo trigger expection if not valid arguments
# Cleaning data before even create Network
# Input must be CSV
# arg string $1 input bach data (it does not have to contain . except for the extension of the file)
if [[ $# -eq 0 ]] ; then
    echo 'Please use the following arguments: '
    echo "./paymo_input/batch_payment.csv ./paymo_input/stream_payment.csv ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt"
    exit 0
fi

echo "Cleaning batch data..."
echo "[$(date)] Starting cleaning batch data.." >> ./results.txt
batch_dataset_cleaned_filename=$(echo $1 | sed -e 's/.csv//g')_cleaned.csv
echo $batch_dataset_cleaned_filename
echo "id1,id2" > $batch_dataset_cleaned_filename
awk 'BEGIN {FS=","} NR >= 2 {  gsub (" ", "", $2);gsub (" ", "", $3); print $2","$3}' $1 >> $batch_dataset_cleaned_filename
awk 'BEGIN {FS=","} NR >= 2 {  gsub (" ", "", $2); print $2}' $1 >> $batch_dataset_cleaned_filename.customers

echo "Finish cleaning batch data..."
echo "[$(date)] Finished cleaning batch data.." >> ./results.txt

echo "Generating Network "
#@todo pass correct arguments
#python3 ./src/antifraud.py ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt

