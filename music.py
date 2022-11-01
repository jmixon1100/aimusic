import sys
import os
import pdb
import numpy as np
from matplotlib import pyplot as plt
import xml.etree.ElementTree as ET


def main():
    sys.path.append('..')

    fn = os.path.join('Untitled.musicxml')

    with open(fn, 'r') as stream:
        xml_str = stream.read()

    start = xml_str.find('<note')
    end = xml_str[start:].find('</note>') + start + len('</note>')
    print(xml_str[start:end])
    # tree = ET.parse(fn)
    # root = tree.getroot()
    pdb.set_trace()
if __name__ == '__main__':
    main()