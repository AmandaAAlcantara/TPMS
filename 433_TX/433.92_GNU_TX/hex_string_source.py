import numpy as np
from gnuradio import gr

class HexStringSource(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
            name="HexStringSource",
            in_sig=None,
            out_sig=[np.uint8])
        self.data = bytes.fromhex('f24c0b2a4d000853fb')
        self.index = 0

    def work(self, input_items, output_items):
        out = output_items[0]
        num_samples = len(out)
        out[:] = np.frombuffer(self.data[self.index:self.index+num_samples], dtype=np.uint8)
        self.index += num_samples
        if self.index >= len(self.data):
            self.index = 0
        return len(out)
