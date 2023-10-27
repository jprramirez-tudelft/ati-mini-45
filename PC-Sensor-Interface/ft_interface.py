import minimalmodbus
import time
import pickle


def instrument_setup(port, baudrate, check_working=False, session_id=None):
    baudrate_mapping = {19200: 1, 115200: 2, 1250000: 0}

    instrument = minimalmodbus.Instrument(port, 10)
    instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN

    # Find and Set Baudrate
    instrument.serial.baudrate = 1250000
    try:
        instrument.read_register(0x001F)
    except IOError:
        instrument.serial.baudrate = 19200
        try:
            instrument.read_register(0x001F)
        except IOError:
            instrument.serial.baudrate = 115200
    finally:
        instrument.write_register(0x001F, baudrate_mapping[baudrate])
        instrument.serial.baudrate = baudrate

    # Check Working
    check_working and print(instrument.read_register(0x001F))

    # Set Session_id (optional)
    session_id is not None and instrument.write_register(0x000C, session_id)

    return instrument


def calibration(instrument):
    calib = [instrument.read_register(i) for i in range(227, 396)]
    instrument._perform_command(106, b'\xaa')  # unlock
    for i in range(6):
        instrument.write_register(0x0+i, calib[121+i])  # set gage gain
        instrument.write_register(0x6+i, calib[127+i])  # set gage offset
        pass
    instrument._perform_command(106, b'\x18')  # lock
    return calib


def acquire_data(instrument, t, verbose=False):
    data = []

    verbose and print("Starting streaming")
    instrument._perform_command(70, b'U')
    t0 = time.time()
    while time.time() - t0 < t:
        data.append(instrument.serial.read(13))
        pass
    t1 = time.time()
    instrument.serial.write(b'jaaammmmminngg')
    verbose and print("Stopped Streaming")
    time.sleep(1)

    # Status Word
    if instrument.read_register(0x001D):
        raise RuntimeError("Status word nonzero")
    else:
        pass

    return data, t1-t0


def save_data(calib, data, t, name):
    with open(name + '.pickle', 'wb') as f:
        pickle.dump((calib, data, t), f)
        pass
    pass
