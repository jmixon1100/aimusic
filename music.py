import glob
import os
import pdb
import numpy as np
from matplotlib import pyplot as plt
from lxml import etree
import argparse

ROOT = os.path.dirname(os.path.abspath(__file__))
parser = argparse.ArgumentParser(
    description="Get note data from musicXML files")
parser.add_argument('-x', '--data',
                    help='path to data folder, defaults to ROOT/scores/*.musicxml',
                    default=os.path.join(ROOT, './scores','*.musicxml'))


def main(args):
    datafile = os.path.expanduser(args.data)

    files = glob.glob(os.path.join(datafile))

    labels, notes = read_data(files)

    pdb.set_trace()


def read_data(files):

    #initialize empty arrays for labels and notes
    notes = np.zeros((len(files), 22))
    labels = []

    for i, file_path in enumerate(files):
        temp_notes = []

        temp_accidentals = []

        #current xml document being read
        xml_str = etree.parse(file_path)

        # get key(labels)
        for key in xml_str.xpath('//key'):
            labels.append(int(key.xpath(".//fifths/text()")[0]))
        # get note values
        for pitch in xml_str.xpath('//pitch'):
            temp_notes.append(pitch.xpath(".//step/text()")[0])
            temp_accidentals.append(int(pitch.xpath(".//alter/text()")
                                    [0]) if pitch.xpath(".//alter/text()") != [] else 0)

        # convert notes to their int equivalents 
        temp_notes = np.asarray(encode_notes(temp_notes))

        # add the accidental values to get the actual pitch of the notes
        temp_notes += temp_accidentals

        #returns note index, and number of occurances of each note
        note_value, note_counts = np.unique(temp_notes, return_counts=1)

        #update the note counts
        for j in range(len(note_value)):
            notes[i, note_value[j]] += note_counts[j]

    return labels, notes


def encode_notes(notes):
    tones = {'A': 1, 'B': 4, 'C': 7, 'D': 10, 'E': 13, 'F': 16, 'G': 19}
    new_notes = []
    for i in range(len(notes)):
        new_notes.append(tones[notes[i]])
    return new_notes

#will get used later for displaying data
def encode_labels():
    keys = {-7: 'Cb', -6: 'Gb', -5: 'Db', -4: 'Ab', -3: 'Eb', -2: 'Bb', -
            1: 'F', 0: 'C', 1: 'G', 2: 'D', 3: 'A', 4: 'E', 5: 'B', 6: 'F#', 7: 'C#'}


if __name__ == '__main__':
    main(parser.parse_args())
