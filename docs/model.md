# model.py Documentation

This documentation provides an overview of the functions implemented in the `model.py` module of the `tdmchops` project.

## analyserfile2datetime64(file)

Convert an analyser file name to a `numpy.datetime64` object.

### Parameters:

- `file` : str
  The file name to convert.

### Returns:

`numpy.datetime64`
  The corresponding `numpy.datetime64` object.

## kicker_times(filename, channel=4, fs=999.99)

Extract kicker times from a TDMS file.

### Parameters:

- `filename` : str
  The TDMS file name.

- `channel` : int, optional (default=4)
  The channel number containing the kicker data.

- `fs` : float, optional (default=999.99)
  The sampling frequency in Hz.

### Returns:

`list`
  A list of kicker times as `numpy.datetime64` objects.

## convert_date_to_filename(date)

Convert a `numpy.datetime64` object to a formatted file name.

### Parameters:

- `date` : `numpy.datetime64`
  The date to convert.

### Returns:

`str`
  The formatted file name corresponding to the input date.

## datetime642analyserfile(datetime64, head='')

Convert a `numpy.datetime64` object to an analyser file name.

### Parameters:

- `datetime64` : `numpy.datetime64`
  The date to convert.

- `head` : str, optional (default='')
  The additional head (prefix) to be added to the file name.

### Returns:

`str`
  The analyser file name corresponding to the input date.

## get_analyser_files(head, termination)

Get a sorted list of analyser files in the specified directory.

### Parameters:

- `head` : str
  The directory containing the analyser files.

- `termination` : str
  The file extension or termination of the analyser files.

### Returns:

`numpy.ndarray`
  A sorted array of analyser file names.

## get_time_delta_between_files(analyser_files)

Calculate the time differences between consecutive analyser files.

### Parameters:

- `analyser_files` : `numpy.ndarray`
  A sorted array of analyser file names.

### Returns:

`numpy.ndarray`
  An array of time differences in seconds between consecutive analyser files.

## plot_in_subsets(arrayx, arrayy, n_subsets)

Plot data in subsets.

### Parameters:

- `arrayx` : `numpy.ndarray`
  The x-axis data array.

- `arrayy` : `numpy.ndarray`
  The y-axis data array.

- `n_subsets` : int
  The number of subsets to plot.

### Returns:

None

## find_key_in_range(dictionary, value)

Find a key in a dictionary based on a value within a range.

### Parameters:

- `dictionary` : dict
  The dictionary to search in.

- `value` : `numpy.datetime64`
  The value to find within the ranges of the dictionary values.

### Returns:

object or None
  The key corresponding to the matching value, or None if no match is found.

## create_dictionary(filenames, values1, values2)

Create a dictionary using the given arrays as keys and values.

### Parameters:

- `filenames` : `numpy.ndarray`
  The keys for the dictionary.

- `values1` : `numpy.ndarray`
  The first values for the dictionary.

- `values2` : `numpy.ndarray`
  The second values for the dictionary.

### Returns:

`dict`
  The created dictionary.

## initial_final_timestamps(file, reference=np.datetime64('2021-06-30T23:27:34.000000'), correction=np.timedelta64(1280157120, 'ns'))

Get the initial and final timestamps of a TDMS file.

### Parameters:

- `file` : str
  The TDMS file name.

- `reference` : `numpy.datetime64`, optional (default=np.datetime64('2021-06-30T23:27:34.000000'))
  The reference timestamp for corrections.

- `correction` : `numpy.timedelta64`, optional (default=np.timedelta64(1280157120, 'ns'))
  The correction value in nanoseconds.

### Returns:

`tuple`
  A tuple containing the initial and final timestamps as `numpy.datetime64` objects.

## get_sc_files(head='/lustre/ap/litv-exp/2021-07-03_E143_TwoPhotonDecay_ssanjari/ntcap/sc/SC_2021-06-30_23-27-45/')

Get a list of SC files.

### Parameters:

- `head` : str, optional (default='/lustre/ap/litv-exp/2021-07-03_E143_TwoPhotonDecay_ssanjari/ntcap/sc/SC_2021-06-30_23-27-45/')
  The directory containing the SC files.

### Returns:

`list`
  A list of SC file names.

## get_iq_files(head='/lustre/ap/litv-exp/2021-07-03_E143_TwoPhotonDecay_ssanjari/ntcap/iq/IQ_2021-06-30_23-27-34_part3/')

Get a list of IQ files.

### Parameters:

- `head` : str, optional (default='/lustre/ap/litv-exp/2021-07-03_E143_TwoPhotonDecay_ssanjari/ntcap/iq/IQ_2021-06-30_23-27-34_part3/')
  The directory containing the IQ files.

### Returns:

`list`
  A list of IQ file names.

## get_kick_time(sc_files)

Get kicker times from a list of SC files.

### Parameters:

- `sc_files` : list
  A list of SC file names.

### Returns:

`numpy.ndarray`
  An array of kicker times as `numpy.datetime64` objects.

## get_absolute_time_file_ranges(iq_files)

Get absolute time ranges for IQ files.

### Parameters:

- `iq_files` : list
  A list of IQ file names.

### Returns:

`dict`
  A dictionary containing IQ file names as keys and their corresponding time ranges (start, finish) as values (`numpy.datetime64` objects).

## chop_and_stack(lframes=2**21, time=1, fs=20000000, offset_in_seconds_from_injection=10, kick_time=None, file_ranges=None)

Chop and stack IQ data based on injection times.

### Parameters:

- `lframes` : int, optional (default=2**21)
  Number of frequency bins (lframes) used during the analysis.

- `time` : float, optional (default=1)
  The duration in seconds of data to analyze, starting from an offset in time (skip).

- `fs` : int, optional (default=20000000)
  The sampling frequency in Hz.

- `offset_in_seconds_from_injection` : float, optional (default=10)
  The starting point in time of the analysis, measured in seconds from the injection time.

- `kick_time` : `numpy.ndarray`, optional (default=None)
  An array of kicker times as `numpy.datetime64` objects.

- `file_ranges` : `dict`, optional (default=None)
  A dictionary containing IQ file names as keys and their corresponding time ranges (start, finish) as values (`numpy.datetime64` objects).

### Returns:

`numpy.ndarray`
  A 2D array containing the chopped and stacked data (`zz_sum`).
