import glob
import os
import pdb
import numpy as np
from matplotlib import pyplot as plt
from lxml import etree
import argparse
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
parser = argparse.ArgumentParser(
    description="Get note data from musicXML files")
parser.add_argument('-x', '--traindata',
                    help='path to data folder, defaults to ROOT/scores/*.musicxml',
                    default=os.path.join(ROOT, './scores', '*.musicxml'))

parser.add_argument('-y', '--testdata',
                    help='path to data folder, defaults to ROOT/test_scores/*.musicxml',
                    default=os.path.join(ROOT, './test_scores', '*.musicxml'))


def main(args):
    training_data_file = os.path.expanduser(args.traindata)
    testing_data_file = os.path.expanduser(args.testdata)

    training_files = glob.glob(os.path.join(training_data_file))
    testing_files = glob.glob(os.path.join(testing_data_file))

    print("Number of training scores being loaded: {:d}".format(len(training_files)))
    train_labels, train_notes = read_data(training_files)
    np.savetxt("trainingdata.txt", train_notes, fmt='%d', delimiter=',')
    np.savetxt("traininglabels.txt", train_labels, fmt='%d')

    print("Current Key Statistics For Training Data")
    keys, counts = get_num_of_keys(train_labels)
    counts -= 1

    np.set_printoptions(formatter={'int': '|{:3d}|'.format},
                        linewidth=sys.maxsize, threshold=sys.maxsize)
    print(''.center(89, '='))
    print(str(keys).lstrip('[').rstrip(']'))
    print(str(counts).lstrip('[').rstrip(']'))
    print(''.center(89, '='))

    print(''.center(30, '='))
    print("GENERATING TEST DATA")
    print(''.center(30, '='))

    test_labels, test_notes = read_data(testing_files)

    print("\nCurrent Key Statistics For Test Data")
    keys, counts = get_num_of_keys(test_labels)
    counts -= 1

    np.set_printoptions(formatter={'int': '|{:3d}|'.format},
                        linewidth=sys.maxsize, threshold=sys.maxsize)
    print(''.center(89, '='))
    print(str(keys).lstrip('[').rstrip(']'))
    print(str(counts).lstrip('[').rstrip(']'))
    print(''.center(89, '='))

    

    np.savetxt("testdata.txt", test_notes, fmt='%d', delimiter=',')
    np.savetxt("testlabels.txt", test_labels, fmt='%d')
# method to help with selecting data to add to data set


def get_num_of_keys(labels):
    total_labels = np.arange(-7, 8)
    temp_labels = np.concatenate((total_labels, labels), axis=None)
    return np.unique(temp_labels, return_counts=1)


def read_data(files):

    # initialize empty arrays for labels and notes
    notes = np.zeros((len(files), 21))
    labels = []

    for i, file_path in enumerate(files):
        temp_notes = []

        temp_accidentals = []

        # current xml document being read
        xml_str = etree.parse(file_path)

        last_key = 0
        oof = False
        # get key(labels)
        for k,key in enumerate(xml_str.xpath('//key')):
            temp_key = int(key.xpath(".//fifths/text()")[0])
            if k == 0 :
                last_key = temp_key
                labels.append(temp_key)
            else:
                print("ERROR: TOO MANY KEYS @ " + file_path)
                oof = True
                # del labels[-(1):]
                
                break
        # get note values
        
        if(not oof):
            for pitch in xml_str.xpath('//pitch'):
                temp_notes.append(pitch.xpath(".//step/text()")[0])
                temp_accidentals.append(int(pitch.xpath(".//alter/text()")
                                        [0]) if pitch.xpath(".//alter/text()") != [] else 0)

        # convert notes to their int equivalents
            temp_notes = np.asarray(encode_notes(temp_notes))

            # add the accidental values to get the actual pitch of the notes
            temp_notes += temp_accidentals

            # returns note index, and number of occurances of each note
            note_value, note_counts = np.unique(temp_notes, return_counts=1)

            # update the note counts
            for j in range(len(note_value)):

                #accounting for double sharps and flats
                if note_value[j] > 20:
                    temp_value = 1
                elif note_value[j] < 0:
                    temp_value = 19
                else :    
                    temp_value = note_value[j]

                
                    notes[i, temp_value] += note_counts[j]
        
    # notes = np.delete(notes,np.where(~notes.any(axis=1))[0],0)
   

    return labels, notes


def encode_notes(notes):
    tones = {'A': 1, 'B': 4, 'C': 7, 'D': 10, 'E': 13, 'F': 16, 'G': 19}
    new_notes = []
    for i in range(len(notes)):
        new_notes.append(tones[notes[i]])
    return new_notes

def convert_labels(keys_nums):
    temp_arr = keys_nums
    for i,key in enumerate(keys_nums):
        temp_arr[i] += abs(key)
    return temp_arr

# will get used later for displaying data
def encode_labels(keys_nums):
    keys = {-7: 'Cb', -6: 'Gb', -5: 'Db', -4: 'Ab', -3: 'Eb', -2: 'Bb', -
            1: 'F', 0: 'C', 1: 'G', 2: 'D', 3: 'A', 4: 'E', 5: 'B', 6: 'F#', 7: 'C#'}
    new_keys = []
    for i in range(len(keys_nums)):
        new_keys.append(keys[keys_nums[i]])
    return new_keys


if __name__ == '__main__':
    main(parser.parse_args())
