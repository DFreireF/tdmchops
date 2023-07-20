import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import matplotlib.dates as mdates

def analyserfile2datetime64(file):
    last_part = file.split('/')[-1].split('-')[-1][:-4]
    year = int(last_part[0:4])
    month = int(last_part[5:7])
    day = int(last_part[8:10])
    hour = int(last_part[11:13])
    minute = int(last_part[14:16])
    second = int(last_part[17:19])
    microsecond = int(last_part[20:23]) * 1000  # Convert to microseconds
    
    # Construct the numpy.datetime64 object
    datetime64 = np.datetime64(f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}.{microsecond:06d}")
    return datetime64


def convert_date_to_filename(date):
    date_str = str(date)
    date_str = date_str.replace('-', '.').replace('T', '.').replace(':', '.')[:-3]
    return date_str + '.tiq'
    # Example usage
    #date = np.datetime64('2021-07-02T15:02:34.958000')
    #filename = convert_date_to_filename(date)
    #print(filename) = 2021.07.02.15.02.34.958.tiq

def datetime642analyserfile(datetime64, head = ''):
    analyser_date = convert_date_to_filename(datetime64)
    return head + analyser_date

def get_analyser_files(head, termination):
    analyser_files = np.sort(glob.glob(os.path.join(head, '*' + termination)))
    return analyser_files

def get_time_delta_between_files(analyser_files):
    delta_files = np.diff([analyserfile2datetime64(file) for file in analyser_files[:]])/ np.timedelta64(1, 's')
    return delta_files

def plot_in_subsets(arrayx, arrayy, n_subsets):
    subset_size = len(arrayy) // n_subsets

    for i in range(n_subsets):
        subsety = arrayy[i * subset_size: (i + 1) * subset_size]
        subsetx = arrayx[i * subset_size: (i + 1) * subset_size]
        plt.figure()
        plt.plot(subsetx, subsety)
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        plt.title(f"Subset {i+1}, average delta  {np.average(subsety)}")
        plt.xlabel("Number of deltas")
        plt.ylabel("Delta T (s)")
        plt.ylim(10,35)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def find_key_in_range(dictionary, value):
    values = np.array(list(dictionary.values()))
    value1 = values[:, 0]
    correction_not_taken = np.timedelta64(int(0.013107200007652864*1e9), 'ns')
    value2 = values[:, 1] + correction_not_taken
    matching_indices = np.where((value1 <= value) & (value <= value2))[0]
    
    if len(matching_indices) > 0:
        matching_key = list(dictionary.keys())[matching_indices[0]]
        return matching_key
    else:
        return None
    
def create_dictionary(filenames, values1, values2):
    result = {}
    for filename, value1, value2 in zip(filenames, values1, values2):
        result[filename] = (value1, value2)
    return result

def initial_final_timestamps(file, reference = np.datetime64('2021-06-30T23:27:34.000000'), correction = np.timedelta64(1280157120, 'ns')):
    timestamps = TdmsFile.read(file)['RecordHeader']['absolute timestamp'][:]
    factor = reference - correction
    initial_timestamp = factor + np.timedelta64(int(timestamps[0]*1e9), 'ns')
    final_timestamp = factor + np.timedelta64(int(timestamps[-1]*1e9), 'ns')
    return initial_timestamp, final_timestamp

def get_sc_files(head = '/lustre/ap/litv-exp/2021-07-03_E143_TwoPhotonDecay_ssanjari/ntcap/sc/SC_2021-06-30_23-27-45/'):
    with open(head+'sc_files.txt', encoding='latin1') as f:
        filelist = f.read().split('\n')
    sc_files = [head + f for f in filelist]
    return sc_files
    

def get_iq_files(head = '/lustre/ap/litv-exp/2021-07-03_E143_TwoPhotonDecay_ssanjari/ntcap/iq/IQ_2021-06-30_23-27-34_part3/'):
    with open(head + 'iq_list.txt', encoding='latin1') as f:
        filelist = f.read().split('\n')
    iq_files = [head + f for f in filelist]
    return iq_files

def get_kick_time(sc_files, kicker_times):
    kick_time = np.array([time + np.timedelta64(2,'h')- np.timedelta64(10927123049,'ns') for file in sc_files[-115:-1] for time in kicker_times(file, channel=4, fs = 999.99)])
    return kick_time

def get_absolute_time_file_ranges(iq_files):
    initial_final_timestamps = np.array([initial_final_timestamps(file) for file in iq_files])
    initial_timestamps = initial_final_timestamps[:,0]
    final_timestamps = initial_final_timestamps[:,1]
    file_ranges = create_dictionary(iq_files, initial_timestamps, final_timestamps)

def chop_and_stack(lframes = 2**21, time = 1, fs = 20000000, offset_in_seconds_from_injection = 10, kick_time, file_ranges):
    nframes = int(fs*time/lframes)
    zz_sum  = np.zeros((nframes, lframes))
    
    for injection_time in kick_time[:-1]: 
        nframes = int(fs*time/lframes)
        file_with_injection = find_key_in_range(file_ranges, injection_time)
        print(f'Analysing the injection found at: {file_with_injection}')
        iq = get_iq_object(file_with_injection)
        iq.method = 'fft'
        offset = int((injection_time + offset_from_injection - file_ranges[file_with_injection][0]) / np.timedelta64(1,'s') * fs)
        
        try:
            iq.read_samples(nframes*lframes, offset = offset)
            _,_,zz = iq.get_power_spectrogram(nframes = nframes, lframes = lframes)
            zz_sum = zz_sum + zz
        
        except ValueError:
            nframes = int((iq.nsamples_total - offset) / lframes)
            if nframes != 0:
                iq.read_samples(nframes*lframes, offset = offset)
                _,_,zz = iq.get_power_spectrogram(nframes = nframes, lframes = lframes)
                array1 = np.copy(zz)
            else: 
                array1 = None
            
            #next file and continue
            iq = get_iq_object(file_with_injection.rsplit("/", 1)[0] + "/" + str(int(file_with_injection.split("/")[-1].split(".")[0]) + 1).zfill(7) + ".iq.tdms")
            nframes = int(fs*time/lframes) - int((iq.nsamples_total - offset) / lframes)
            if nframes == 0:
                zz_sum = zz_sum + array1
                continue
            iq.read_samples(nframes*lframes, offset = 0)
            _,_,zz = iq.get_power_spectrogram(nframes = nframes, lframes = lframes)
            if array1 is None:
                zz_sum = zz_sum + zz
            else:
                zz_sum = zz_sum + np.vstack((array1,zz))
            del(array1)
            gc.collect()
        
        del(zz)
        gc.collect()
        
    return zz_sum


