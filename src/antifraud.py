import pandas as pd
import sys
import csv
import numpy as np
import time


def verify_all_features(df,feature_one,feature_two,feature_three):
    for x in df.values:
        feature_one.write('unverified\n')
        feature_two.write('unverified\n')
        feature_three.write('trusted\n')

def main():
    """
    Reads sanitized batch file into a dataframe
    The general idea is generate analyze each relationship from the incoming payment then create a matrix
        which will generate a matrix of size MxM to look up relationships even faster.
    *re-compute matrix when there are new users.*
    args ./paymo_input/batch_payment_cleaned.csv ./paymo_input/stream_payment.csv ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt
    """
    feature_one = open(sys.argv[3], 'w')
    feature_two = open(sys.argv[4], 'w')
    feature_three = open(sys.argv[5], 'w')
    # Reads initial file
    dataframe = pd.read_csv(sys.argv[1], sep=',',
                            header=0, skipinitialspace=True, error_bad_lines=False, index_col=0)

    # @todo generate matrix of size of size MxM before incoming payments.
    # @todo do not calculate 2nd, 3rd and 4th generations using a for loop. It won't work.
    #    An optimal solution will be to use an adjacency Matrix theorem: https://people.math.osu.edu/husen.1/teaching/sp2003/571/graphs.pdf.
    #    Theorem: If A is the adjacency matrix of a graph or digraph G with vertices {v1, . . . vn}, then the i, j entry of Ak is the number of paths of length k from vi to vj .
    new_payments_file = open(sys.argv[2], 'rt')
    # Analyze relationships of incoming payments against data in the system.
    try:
        reader = csv.reader(new_payments_file)
        next(reader, None)
        for payment in reader:
            first_generation_around = False
            first_generation = False
            index_payment = int(payment[1].replace(" ", ""))
            try:
                first_generation = str(
                    dataframe.ix[index_payment].query(
                        'id2==' + payment[2].replace(" ", "")).size > 0)
            except KeyError:
                try:
                    first_generation_around = int(payment[2].replace(" ", "")) in (
                        dataframe['id2'] == index_payment)
                except KeyError:
                    # @todo add new relationship to matrix.
                    print("Check next generation")

            if first_generation or first_generation_around:
                feature_one.write('trusted\n')
                feature_two.write('trusted\n')
                feature_three.write('trusted\n')
                # Next payment request.
            else:
                # Gather friends of friends (second generation)
                test = dataframe.ix[index_payment]
                # At this point it seems not the best idea to keep iterating. I'd be really slow for large datasets.
                # For example: Using the 3.8 M records CSV file and trying to create a matrix out of it kills
    finally:
        new_payments_file.close()


if __name__ == '__main__':
    main()