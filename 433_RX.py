import numpy as np
from hackrf import HackRF
import time

# Data to be transmitted
data = 'f24c0b2a4d5b0889fd'

# Manchester Encoding
def manchester_encode(data):
    manchester_dict = {
        '0': '01',
        '1': '10'
    }
    binary_data = ''.join(format(int(byte, 16), '04b') for byte in data)
    manchester_encoded = ''.join(manchester_dict[bit] for bit in binary_data)
    return manchester_encoded

# Function to generate a simple FSK wave
def generate_fsk_wave(encoded_data, base_frequency, sample_rate, symbol_rate):
    symbols = np.array([int(bit) for bit in encoded_data])
    samples_per_symbol = int(sample_rate / symbol_rate)
    t = np.arange(samples_per_symbol) / sample_rate
    
    fsk_wave = np.concatenate([
        0.5 * np.sin(2 * np.pi * (base_frequency + (symbol * 10e3)) * t)
        for symbol in symbols
    ])
    
    return fsk_wave.astype(np.float32)

# Encode the data
encoded_data = manchester_encode(data)

# Initialize HackRF
hackrf = HackRF()

try:
    hackrf.open()
    hackrf.set_tx_freq(433.92e6)  # Set frequency to 433.92 MHz
    hackrf.set_sample_rate(2e6)  # Set sample rate to 2 MHz
    hackrf.set_txvga_gain(20)  # Set TX gain

    # Generate FSK wave
    fsk_wave = generate_fsk_wave(encoded_data, base_frequency=433.92e6, sample_rate=2e6, symbol_rate=1e3)  # 1 kHz symbol rate

    def transmit_callback(samples, num_samples, _):
        samples[:num_samples] = fsk_wave[:num_samples]
        return 0

    # Start transmitting
    hackrf.start_tx(transmit_callback)
    print("Transmitting for 15 seconds...")
    time.sleep(15)  # Transmit for 15 seconds

finally:
    hackrf.stop_tx()
    hackrf.close()
    print("Transmission stopped.")
