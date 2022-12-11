# decisiontree.py
"""Predict Parkinson's disease based on dysphonia measurements using a decision tree."""

import matplotlib.pyplot as plt
import numpy as np
import os
import pdb
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import confusion_matrix
import argparse
ROOT = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description="Use a Naive Bayes model to classify text documents.")

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
    xtrain = np.loadtxt(training_data_path, dtype=int,delimiter=',')
    print("Loading training labels...")
    ytrain = np.loadtxt(training_labels_path, dtype=int,delimiter=',')
    print("Loading testing data...")
    xtest = np.loadtxt(testing_data_path, dtype=int,delimiter=',')
    print("Loading testing labels...")
    ytest = np.loadtxt(testing_labels_path, dtype=int,delimiter=',')
    print("Loading keys...")
    key_sigs = np.loadtxt(key_sig_path, dtype=int,delimiter=',')
    print("Loading notes...")
    notes = np.loadtxt(notes_path, dtype=int,delimiter=',')

    # Train a decision tree via information gain on the training data
    clf = DecisionTreeClassifier(
        criterion="entropy",
        splitter="best",
        max_depth=None,
        random_state=0)
    clf.fit(xtrain, ytrain)

    # Test the decision tree
    pred = clf.predict(xtest)

    # Compare training and test accuracy
    print("train accuracy =", np.mean(ytrain == clf.predict(xtrain)))
    print("test accuracy =", np.mean(ytest == pred))

    # Show the confusion matrix for test data
    cm = confusion_matrix(ytest, pred)
    print("Confusion matrix:")
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in cm]))
    key_sigs = encode_labels(key_sigs)
    # Visualize the tree using matplotlib and plot_tree
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(11, 5), dpi=150)
    plot_tree(clf,class_names=key_sigs, filled=True, rounded=True, fontsize=6)
    plt.show()

def encode_labels(keys_nums):
    keys = {-7: 'Cb', -6: 'Gb', -5: 'Db', -4: 'Ab', -3: 'Eb', -2: 'Bb', -
            1: 'F', 0: 'C', 1: 'G', 2: 'D', 3: 'A', 4: 'E', 5: 'B', 6: 'F#', 7: 'C#'}
    new_keys = []
    for i in range(len(keys_nums)):
        new_keys.append(keys[keys_nums[i]])
    return new_keys

if __name__ == '__main__':
    main(parser.parse_args())
