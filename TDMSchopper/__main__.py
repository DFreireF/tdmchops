import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import matplotlib.dates as mdates
import argparse

from TDMSchopper.TDMSchopper.model import get_iq_files, get_sc_files, get_absolute_time_file_ranges

def main():
    
    scriptname = 'TDMSchopper' 
    parser = argparse.ArgumentParser()

    # Main Arguments
    parser.add_argument('odsin', type = str, nargs = '+', help = 'Name of the ods.')
    parser.add_argument('-t','--texout', type = str, nargs = '?', help = 'Name of the tex.')

    args = parser.parse_args()

    controller(args.odsin[0],  args.texout)
    print(f'{scriptname} converted {args.odsin[0]} to tex succesfully.')
    
def controller():
    sc_files = get_sc_files()
    iq_files = get_iq_files()
    file_ranges = get_absolute_time_file_ranges()

if __name__ == '__main__':
    main()
