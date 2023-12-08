import numpy as np
import argparse

from .model import get_iq_files, get_sc_files, get_absolute_time_file_ranges, get_kick_time, chop_and_stack

def main():
    """
    Main entry point of the TDMchopS script.

    This function parses command-line arguments, performs the chopping and stacking of data,
    and saves the result in a NumPy file.

    Command-line Arguments:
    -t, --time : float, optional (default=1)
        The duration in seconds of data to analyze, starting from an offset in time (skip).
    -s, --skip : float, optional (default=10)
        The starting point in time of the analysis, measured in seconds from the injection time.
    -b, --binning : int, optional (default=2**21)
        The number of frequency bins (lframes) used during the analysis.

    Returns:
    None
    """
    scriptname = 'TDMSchopper' 
    parser = argparse.ArgumentParser()

    # Main Arguments
    parser.add_argument('-t', '--time', type = float, default = 1, help = 'For how long in time to analyse (from an introduced offset in time (skip)).')
    parser.add_argument('-s', '--skip', type = float, default = 10, help = 'Starting point in time of the analysis (from injection).')
    parser.add_argument('-b', '--binning', type = int, default = 2**21, help = 'Number of frecuency bins (lframes).')

    args = parser.parse_args()

    controller(int(args.binning), args.time, args.skip)
    
def controller(lframes, time, skip):
    """
    Controller function responsible for orchestrating the data chopping and stacking process.

    This function retrieves relevant data files, analyzes data based on provided time and skip parameters,
    and saves the resulting chopped and stacked data in a NumPy file.

    Parameters:
    lframes : int
        Number of frequency bins (lframes) used during the analysis.
    time : float
        The duration in seconds of data to analyze, starting from an offset in time (skip).
    skip : float
        The starting point in time of the analysis, measured in seconds from the injection time.

    Returns:
    None
    """
    #Get the files containing the scalar and iq signal information recorded by the NTCAP
    sc_files = get_sc_files()
    iq_files = get_iq_files()
    #Get the kicker time, corrected to injection time by correcting the time with a reference
    kick_time = get_kick_time(sc_files)
    #Get from where in absolute time to where it finish every iq file and created a dictionary for every file (key) with the two time values (start, finish)
    file_ranges = get_absolute_time_file_ranges(iq_files)
    #for every absolute injection time find in which file is it information stored and from there, analyses 'time' seconds of data from and offset of 'skip' seconds from injection.
    #keep the power[time][frequency] (zz) for every chunk stacked into zz_sum
    zz_cutted_and_stacked = chop_and_stack(lframes = lframes, time = time, fs = 20000000, offset_in_seconds_from_injection = skip, kick_time = kick_time, file_ranges = file_ranges)
    #save the chopped and stacked zz_sum of every injection time
    np.savez('zz_cutted_and_stacked', zz = zz_cutted_and_stacked)

if __name__ == '__main__':
    main()
