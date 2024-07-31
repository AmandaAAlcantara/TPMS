#developed with the data taken from the TPMS sensor project 

from gnuradio import gr, blocks, analog
from gnuradio import uhd
import numpy as np
import time

# Import custom blocks
from my_custom_blocks.manchester_encoder import ManchesterEncoder
from my_custom_blocks.hex_string_source import HexStringSource

class FSKTransmitter(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        sample_rate = 2e6  
        center_freq = 433.92e6  
        gain = 20  
        symbol_rate = 1e3 
        freq_deviation = 10e3 
        
        self.hex_source = HexStringSource()
        self.manchester_encoder = ManchesterEncoder()
        self.float_to_complex = blocks.float_to_complex(1)
        self.fsk_mod = analog.frequency_modulator_fc(2 * np.pi * freq_deviation / sample_rate)
        self.throttle = blocks.throttle(gr.sizeof_gr_complex * 1, sample_rate, True)
        self.usrp_sink = uhd.usrp_sink(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                channels=range(1),
            ),
        )

    
        self.connect(self.hex_source, self.manchester_encoder, self.float_to_complex, self.fsk_mod, self.throttle, self.usrp_sink)
        
     
        self.usrp_sink.set_samp_rate(sample_rate)
        self.usrp_sink.set_center_freq(center_freq, 0)
        self.usrp_sink.set_gain(gain, 0)

# Instantiate and run the flowgraph
if __name__ == '__main__':
    tb = FSKTransmitter()
    tb.start()
    print("Transmitting for 15 seconds...")
    time.sleep(15) 
    tb.stop()
    tb.wait()
    print("Transmission stopped.")
