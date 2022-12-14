# neuralnetwork_mnist.py
# Handwritten digit recognition on the MNIST dataset using a Keras neural network.
#
# References:
# 1. https://en.wikipedia.org/wiki/MNIST_database
# 2. https://keras.io/api/datasets/mnist/
from sklearn.metrics import confusion_matrix
from keras.callbacks import EarlyStopping
from keras.models import Sequential
from keras.layers import Input, Dense
from keras.optimizers import SGD, Adam, RMSprop, Ftrl
from keras.utils import to_categorical
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np
import os
import pdb
import tensorflow as tf
import argparse

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
    # Uncomment the following line to produce repeatable results

    # Load data
    numsamples, numinputs = xtrain.shape
    numoutputs = len(np.unique(ytrain))
    # convert output to categorical targets
    t_train = to_categorical(ytrain, numoutputs)
    t_test = to_categorical(ytest, numoutputs)

    # Create neural network

    model = load_model('presmodel.h5')  # loading model

    # model = Sequential(name="key_recognition")
    # model.add(Input(shape=(numinputs,)))
    # model.add(Dense(units=200, activation='tanh', name='hidden1'))
    # model.add(Dense(units=200, activation='tanh', name='hidden2'))
    # # model.add(Dense(units=800, activation='tanh', name='hidden3'))
    # model.add(Dense(units=numoutputs, activation='softmax', name='output'))

    model.summary()
    input("Press <Enter> to continue")

    model.compile(
        loss=tf.keras.losses.SquaredHinge(),
        optimizer=SGD(learning_rate=0.01),
        metrics=['accuracy'])

    # Add optional callbacks
    callback = EarlyStopping(
        monitor='loss',
        min_delta=1e-5,
        patience=10,
        verbose=1)

    # Train the network
    history = model.fit(xtrain, t_train,
                        epochs=100,
                        batch_size=5,
                        validation_data=(xtest, t_test),
                        callbacks=[callback],
                        verbose=1)

    # Compute the accuracy
    metrics_train = model.evaluate(xtrain, t_train, verbose=0)
    print("=================================")
    print(f"Training loss = {metrics_train[0]:0.4f}")
    print(f"Training accuracy = {metrics_train[1]:0.4f}")

    metrics_test = model.evaluate(xtest, t_test, verbose=0)
    print(f"Testing loss = {metrics_test[0]:0.4f}")
    print(f"Testing accuracy = {metrics_test[1]:0.4f}")

    # Show the confusion matrix for test data
    pred = np.argmax(model.predict(xtest, verbose=0), axis=-1)
    cm = confusion_matrix(ytest, pred)
    print("Confusion matrix:")
    print('\n'.join([''.join(['{:6}'.format(item)
          for item in row]) for row in cm]))

    # Plot the performance over time
    # fig, ax = plt.subplots()
    p1, = plt.plot(ytest,'bo')
    p2, = plt.plot(pred,'ro')
    
    plt.show()

    # Show misclassifications

    # Save model to file
    model.save(os.path.expanduser(os.path.join(ROOT, 'mnist_model.h5')))

    # pdb.set_trace()


if __name__ == "__main__":
    main(parser.parse_args())
