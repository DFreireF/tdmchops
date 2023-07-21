# TDMSchopper Script Documentation

This documentation provides an overview of the TDMSchopper script functionality.

The TDMSchopper script processes input arguments from the command line to specify the duration of the analysis, the starting point of the analysis, and the number of frequency bins. It then calls the `controller()` function, which coordinates the chopping and stacking process. The `controller()` function uses methods from the `TDMSchopper.model` module to retrieve necessary data files, analyze the data, and save the chopped and stacked data in a NumPy file called `zz_cutted_and_stacked.npz`.

## main()

Main entry point of the TDMSchopper script.

This function parses command-line arguments, performs the chopping and stacking of data, and saves the result in a NumPy file.

### Command-line Arguments:

- `-t`, `--time` : float, optional (default=1)
  The duration in seconds of data to analyze, starting from an offset in time (skip).

- `-s`, `--skip` : float, optional (default=10)
  The starting point in time of the analysis, measured in seconds from the injection time.

- `-b`, `--binning` : int, optional (default=2**21)
  The number of frequency bins (lframes) used during the analysis.

### Returns:

None

## controller(lframes, time, skip)

Controller function responsible for orchestrating the data chopping and stacking process.

This function retrieves relevant data files, analyzes data based on provided time and skip parameters, and saves the resulting chopped and stacked data in a NumPy file.

### Parameters:

- `lframes` : int
  Number of frequency bins (lframes) used during the analysis.

- `time` : float
  The duration in seconds of data to analyze, starting from an offset in time (skip).

- `skip` : float
  The starting point in time of the analysis, measured in seconds from the injection time.

### Returns:

None
