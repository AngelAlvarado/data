#!/usr/bin/env bash

# I'll execute my programs, with the input directory paymo_input and output the files in the directory paymo_output
# This file cleans batch data and executes main script file to detect fraudulent payments.
# Cleaning data before even create Network
# Input must be txt separated by commas
# arg string $1 input bach data (it does not have to contain  except for the extension of the file)
echo $#
if [[ $# != 5 ]] ; then
    echo 'Using following output and input files: '
    echo "./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt"
    batch="./paymo_input/batch_payment.txt"
    stream="./paymo_input/stream_payment.txt"
    output1="./paymo_output/output1.txt"
    output2="./paymo_output/output2.txt"
    output3="./paymo_output/output3.txt"
else
    batch=$1
    stream=$2
    output1=$3
    output2=$4
    output3=$5
fi

echo "Cleaning batch data..."
echo "[$(date)] Starting cleaning batch data.." >> ./results.txt
batch_dataset_cleaned_filename=$(echo $batch | sed -e 's/.txt//g')_cleaned.txt
echo "New dataset name:"
echo $batch_dataset_cleaned_filename
echo "Using only columns with data important to me (id1 and id2)..."
echo "id1,id2" > $batch_dataset_cleaned_filename
awk 'BEGIN {FS=","} NR >= 2 {  gsub (" ", "", $2); gsub (" ", "", $3); print $2","$3}' $batch >> $batch_dataset_cleaned_filename

echo "Finish cleaning batch data..."
echo "[$(date)] Finished cleaning batch data.." >> ./results.txt

echo $5
echo "Generating Network and Setting up application to process new payments"
#@todo pass correct arguments
/Users/Angel/anaconda/bin/python ./src/antifraud.py $batch $stream $output1 $output2 $output3

