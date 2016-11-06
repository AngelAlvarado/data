#!/usr/bin/env bash

# I'll execute my programs, with the input directory paymo_input and output the files in the directory paymo_output
# This file cleans batch data and executes main script file to detect fraudulent payments.
# Cleaning data before even create Network
# Input must be CSV
# arg string $1 input bach data (it does not have to contain  except for the extension of the file)
if [[ $# -eq 0 ]] ; then
    echo 'Using following output and input files: '
    echo "./paymo_input/batch_payment.csv ./paymo_input/stream_payment.csv ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt"
    $1="./paymo_input/batch_payment.csv"
    $2="./paymo_input/stream_payment.csv"
    $3="./paymo_output/output1.txt"
    $4="./paymo_output/output2.txt"
    $5="./paymo_output/output3.txt"
fi

echo "Cleaning batch data..."
echo "[$(date)] Starting cleaning batch data.." >> ./results.txt
batch_dataset_cleaned_filename=$(echo $1 | sed -e 's/.csv//g')_cleaned.csv
echo "New dataset name:"
echo $batch_dataset_cleaned_filename
echo "Using only columns with data important to me (id1 and id2)..."
echo "id1,id2" > $batch_dataset_cleaned_filename
awk 'BEGIN {FS=","} NR >= 2 {  gsub (" ", "", $2); gsub (" ", "", $3); print $2","$3}' $1 >> $batch_dataset_cleaned_filename
awk 'BEGIN {FS=","} NR >= 2 {  gsub (" ", "", $2); print $2}' $1 >> $batch_dataset_cleaned_filename.customers

echo "Finish cleaning batch data..."
echo "[$(date)] Finished cleaning batch data.." >> ./results.txt

echo "Generating Network and Setting up application to process new payments"
#@todo pass correct arguments
/Users/Angel/anaconda/bin/python ./src/antifraud.py $1 $2 $3 $4 $5

