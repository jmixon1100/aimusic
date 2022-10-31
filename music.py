import sys
import os
import pdb
import numpy as np
from matplotlib import pyplot as plt



def main():
    sys.path.append('..')

    fn = os.path.join('FMP_C1_F15_Eflat.xml')

    with open(fn, 'r') as stream:
        xml_str = stream.read()

    start = xml_str.find('<note')
    end = xml_str[start:].find('</note>') + start + len('</note>')
    print(xml_str[start:end])
    pdb.set_trace()
if __name__ == '__main__':
    main()