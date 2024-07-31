import numpy as np
from gnuradio import gr

class ManchesterEncoder(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
            name="ManchesterEncoder",
            in_sig=[np.uint8],
            out_sig=[np.float32])
        
    def manchester_encode(self, byte):
        manchester_dict = {
            '0': '01',
            '1': '10'
        }
        binary_data = format(byte, '08b')
        encoded = ''.join(manchester_dict[bit] for bit in binary_data)
        return np.array([int(b) for b in encoded], dtype=np.float32)
    
    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        out[:] = np.concatenate([self.manchester_encode(byte) for byte in in0])
        return len(out)


