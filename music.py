import os
import pdb
import numpy as np
from matplotlib import pyplot as plt
from lxml import etree
import argparse

ROOT = os.path.dirname(os.path.abspath(__file__))
parser = argparse.ArgumentParser(
    description="Train a perceptron to classify letters.")
parser.add_argument('-x', '--data',
                    help='path to data file, defaults to ROOT/data.txt',
                    default=os.path.join(ROOT, 'untitled.musicxml'))


def main(args):
    datafile = os.path.expanduser(args.data)
    notes = []
    accidentals = []
    # this section of code took way too long
    xml_str = etree.parse(datafile)
    for pitch in xml_str.xpath('//pitch'):
        notes.append(pitch.xpath(".//step/text()")[0])
        accidentals.append(pitch.xpath(".//alter/text()")
                           [0] if pitch.xpath(".//alter/text()") != [] else '0')
    pdb.set_trace()


def encode_notes():
    tones = {'A': 1, 'B': 4, 'C': 7, 'D': 10, 'E': 13, 'F': 16, 'G': 19}


if __name__ == '__main__':
    main(parser.parse_args())
