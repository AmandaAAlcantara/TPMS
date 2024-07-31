#developed with the data taken from the TPMS sensor project 
# @https://www.rtl-sdr.com/using-a-hackrf-to-transmit-to-a-local-repeater/

import numpy as np
from hackrf import HackRF
import time

# Data to be transmitted - pressure = 0
data = 'f24c0b2a4d000853fb'

# Manchester Encoding
def manchester_encode(data):
    manchester_dict = {
        '0': '01',
        '1': '10'
    }
    binary_data = ''.join(format(int(byte, 16), '04b') for byte in data)
    manchester_encoded = ''.join(manchester_dict[bit] for bit in binary_data)
    return manchester_encoded

# Function to generate wave
def generate_fsk_wave(encoded_data, base_frequency, sample_rate, symbol_rate):
    symbols = np.array([int(bit) for bit in encoded_data])
    samples_per_symbol = int(sample_rate / symbol_rate)
    t = np.arange(samples_per_symbol) / sample_rate
    
    fsk_wave = np.concatenate([
        0.5 * np.sin(2 * np.pi * (base_frequency + (symbol * 10e3)) * t)
        for symbol in symbols
    ])
    
    return fsk_wave.astype(np.float32)

# data encoder
encoded_data = manchester_encode(data)


hackrf = HackRF()

try:
    hackrf.open()
    hackrf.set_tx_freq(433.92e6) 
    hackrf.set_sample_rate(2e6) 
    hackrf.set_txvga_gain(20)  
    #wave
    fsk_wave = generate_fsk_wave(encoded_data, base_frequency=433.92e6, sample_rate=2e6, symbol_rate=1e3)  

    def transmit_callback(samples, num_samples, _):
        samples[:num_samples] = fsk_wave[:num_samples]
        return 0

    #transmit
    hackrf.start_tx(transmit_callback)
    print("Transmitting for 15 seconds...")
    time.sleep(15)  

finally:
    hackrf.stop_tx()
    hackrf.close()
    print("TX stopped")
