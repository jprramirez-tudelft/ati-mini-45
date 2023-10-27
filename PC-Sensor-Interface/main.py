import ft_interface as fif
import preprocessing as pre


# Notes: Baud rate 115200 very unstable: often returns incorrect samples, etc.

file_name = 'test'  # filename that data and plots get saved as.

# Force sensor interface
instrument = fif.instrument_setup('COM5', 1250000)  # select USB port and baudrate (19200=100Hz / 115200=500Hz / 1250000=7000Hz)
calib = fif.calibration(instrument)
data, t = fif.acquire_data(instrument, 10)  # select timespan of data capture
fif.save_data(calib, data, t, file_name)  # saved as file_name.pickle

# Preprocessing
calib, preprocessed_data, t = pre.load(file_name)
values = pre.get_values(preprocessed_data, calib)
pre.save_preprocessed_data(values, t, file_name)  # saved as file_name_preprocessed.pickle
pre.plot_initial_data(values, t, calib, file_name)  # saved as file_name-initial_plot.png
