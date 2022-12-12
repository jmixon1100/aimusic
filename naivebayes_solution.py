# naivebayes.py
"""Perform document classification using a Naive Bayes model."""

import argparse
import os
import pdb
import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import ComplementNB

ROOT = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(
    description="Use a Naive Bayes model to classify text documents.")
parser.add_argument('-x', '--training_data',
                    help='path to training data file, defaults to ROOT/trainingdata.txt',
                    default=os.path.join(ROOT, 'trainingdata.txt'))
parser.add_argument('-y', '--training_labels',
                    help='path to training labels file, defaults to ROOT/traininglabels.txt',
                    default=os.path.join(ROOT, 'traininglabels.txt'))
parser.add_argument('-xt', '--testing_data',
                    help='path to testing data file, defaults to ROOT/testdata.txt',
                    default=os.path.join(ROOT, 'testdata.txt'))
parser.add_argument('-yt', '--testing_labels',
                    help='path to testing labels file, defaults to ROOT/testlabels.txt',
                    default=os.path.join(ROOT, 'testlabels.txt'))
parser.add_argument('-k', '--keys',
                    help='path to newsgroups file, defaults to ROOT/keys.txt',
                    default=os.path.join(ROOT, 'keys.txt'))
parser.add_argument('-n', '--notes',
                    help='path to vocabulary file, defaults to ROOT/notes.txt',
                    default=os.path.join(ROOT, 'notes.txt'))


def main(args):
    print("Document Classification using Naïve Bayes Classifiers")
    print("=======================")
    print("PRE-PROCESSING")
    print("=======================")

    # Parse input arguments
    training_data_path = os.path.expanduser(args.training_data)
    training_labels_path = os.path.expanduser(args.training_labels)
    testing_data_path = os.path.expanduser(args.testing_data)
    testing_labels_path = os.path.expanduser(args.testing_labels)
    key_sig_path = os.path.expanduser(args.keys)
    notes_path = os.path.expanduser(args.notes)

    # Load data from relevant files
    print("Loading training data...")
    xtrain = np.loadtxt(training_data_path, dtype=int, delimiter=',')
    print("Loading training labels...")
    ytrain = np.loadtxt(training_labels_path, dtype=int, delimiter=',')
    print("Loading testing data...")
    xtest = np.loadtxt(testing_data_path, dtype=int, delimiter=',')
    print("Loading testing labels...")
    ytest = np.loadtxt(testing_labels_path, dtype=int, delimiter=',')
    print("Loading keys...")
    key_sigs = np.loadtxt(key_sig_path, dtype=int, delimiter=',')
    print("Loading notes...")
    notes = np.loadtxt(notes_path, dtype=int, delimiter=',')

    # Change indexing to 0
    # xtrain[:, 0:2] -= 1
    # ytrain += 7
    # xtest[:, 0:2] -= 1
    # ytest += 7

    # Extract useful parameters
    num_training_documents = len(ytrain)
    num_testing_documents = len(ytest)
    num_words = len(notes)
    num_newsgroups = len(key_sigs)

    clf = GaussianNB()
    clf.fit(xtrain, ytrain)
    pred = clf.predict(xtest)

    # Compare training and test accuracy
    print("train accuracy =", np.mean(ytrain == clf.predict(xtrain)))
    print("test accuracy =", np.mean(ytest == pred))

if __name__ == '__main__':
    main(parser.parse_args())
