import pandas as pd
import sys
import csv
import time


def verify_all_features(df,feature_one,feature_two,feature_three):
    for x in df.values:
        feature_one.write('unverified\n')
        feature_two.write('unverified\n')
        feature_three.write('trusted\n')

def main():
    """
    Reads sanitized batch file into a dataframe
    The general idea is generate a big matrix and the analyze from it each new record
    *re-compute matrix when there are new users.*
    args ./paymo_input/batch_payment_cleaned.csv ./paymo_input/stream_payment.csv ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt
    """
    feature_one = open(sys.argv[3], 'w')
    feature_two = open(sys.argv[4], 'w')
    feature_three = open(sys.argv[5], 'w')
    # preparing network-matrices

    # Initialize matrix size
    dataframeunique = pd.read_csv(sys.argv[1], sep=',',
                            header=0, skipinitialspace=True, error_bad_lines=False, index_col=0)
    w = dataframeunique.groupby(dataframeunique.index).first().count()
    Matrix = [[0 for x in range(w)] for y in range(w)]

    # Maybe not needed and same dataframe can be used
    dataframe = pd.read_csv(sys.argv[1], sep=',',
                            header=0, skipinitialspace=True, error_bad_lines=False, index_col=0)

    # @todo generate matrix before start processing
    new_payments_file = open(sys.argv[2], 'rt')

    try:
        reader = csv.reader(new_payments_file)
        next(reader, None)
        for payment in reader:
            return
            ## below code will be deleted and Matrix will be use to calculate generation
            first_generation = str(
                dataframe.ix[int(payment[1].replace(" ", ""))].query('id2==' + payment[2].replace(" ", "")).size > 0)
            if first_generation:
                feature_one.write('trusted\n')
                # Next payment request.
            else:
                feature_one.write('unverified\n')
                # testing second generation
            #time.sleep(5)
    finally:
        new_payments_file.close()


if __name__ == '__main__':
    main()