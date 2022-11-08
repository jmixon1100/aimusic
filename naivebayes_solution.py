# naivebayes.py
"""Perform document classification using a Naive Bayes model."""

import argparse
import os
import pdb
import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

ROOT = '~/OneDrive - flsouthern.edu/csc3520/assignments/hw1/data'  # change to path where data is stored

parser = argparse.ArgumentParser(description="Use a Naive Bayes model to classify text documents.")
parser.add_argument('-x', '--training_data',
                    help='path to training data file, defaults to ROOT/trainingdata.txt',
                    default=os.path.join(ROOT, 'trainingdata.txt'))
parser.add_argument('-y', '--training_labels',
                    help='path to training labels file, defaults to ROOT/traininglabels.txt',
                    default=os.path.join(ROOT, 'traininglabels.txt'))
parser.add_argument('-xt', '--testing_data',
                    help='path to testing data file, defaults to ROOT/testingdata.txt',
                    default=os.path.join(ROOT, 'testingdata.txt'))
parser.add_argument('-yt', '--testing_labels',
                    help='path to testing labels file, defaults to ROOT/testinglabels.txt',
                    default=os.path.join(ROOT, 'testinglabels.txt'))
parser.add_argument('-n', '--newsgroups',
                    help='path to newsgroups file, defaults to ROOT/newsgroups.txt',
                    default=os.path.join(ROOT, 'newsgroups.txt'))
parser.add_argument('-v', '--vocabulary',
                    help='path to vocabulary file, defaults to ROOT/vocabulary.txt',
                    default=os.path.join(ROOT, 'vocabulary.txt'))


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
    newsgroups_path = os.path.expanduser(args.newsgroups)
    vocabulary_path = os.path.expanduser(args.vocabulary)

    # Load data from relevant files
    print("Loading training data...")
    xtrain = np.loadtxt(training_data_path, dtype=int)
    print("Loading training labels...")
    ytrain = np.loadtxt(training_labels_path, dtype=int)
    print("Loading testing data...")
    xtest = np.loadtxt(testing_data_path, dtype=int)
    print("Loading testing labels...")
    ytest = np.loadtxt(testing_labels_path, dtype=int)
    print("Loading newsgroups...")
    newsgroups = np.loadtxt(newsgroups_path, dtype=str)
    print("Loading vocabulary...")
    vocabulary = np.loadtxt(vocabulary_path, dtype=str)

    # Change 1-indexing to 0
    xtrain[:, 0:2] -= 1
    ytrain -= 1
    xtest[:, 0:2] -= 1
    ytest -= 1

    # Extract useful parameters
    num_training_documents = len(ytrain)
    num_testing_documents = len(ytest)
    num_words = len(vocabulary)
    num_newsgroups = len(newsgroups)

    print("\n=======================")
    print("TRAINING")
    print("=======================")

    # Estimate the prior probabilities
    print("Estimating prior probabilities via MLE...")
    priors = np.bincount(ytrain) / num_training_documents

    # Estimate the class conditional probabilities
    print("Estimating class conditional probabilities via MAP...")
    class_conditionals = np.zeros((num_words, num_newsgroups))
    rows = xtrain[:, 1].tolist()
    cols = ytrain[xtrain[:, 0]].tolist()
    np.add.at(class_conditionals, (rows, cols), xtrain[:, 2])
    alpha = (1 / num_words)
    class_conditionals += alpha
    class_conditionals /= np.sum(class_conditionals, 0)
    # pdb.set_trace()
    print("\n=======================")
    print("TESTING")
    print("=======================")

    # Test the Naive Bayes classifier
    print("Applying natural log to prevent underflow...")
    log_priors = np.log(priors)
    log_class_conditionals = np.log(class_conditionals)

    print("Counting words in each document...")
    counts = np.zeros((num_testing_documents, num_words))
    rows = xtest[:, 0].tolist()
    cols = xtest[:, 1].tolist()
    np.add.at(counts, (rows, cols), xtest[:, 2])

    print("Computing posterior probabilities...")
    log_posterior = np.matmul(counts, log_class_conditionals)
    log_posterior += log_priors

    print("Assigning predictions via argmax...")
    pred = np.argmax(log_posterior, 1)

    print("\n=======================")
    print("PERFORMANCE METRICS")
    print("=======================")

    # Compute performance metrics
    accuracy = np.mean(ytest == pred)
    print("Accuracy: {0:d}/{1:d} ({2:0.1f}%)".format(sum(ytest == pred), num_testing_documents, accuracy * 100))
    cm = confusion_matrix(ytest, pred)
    print("Confusion matrix:")
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in cm]))

    # pdb.set_trace()


if __name__ == '__main__':
    main(parser.parse_args())
