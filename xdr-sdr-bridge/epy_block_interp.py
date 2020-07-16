"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, from_min=-10.0, from_max=10.0, to_min=0.0, to_max=1.0, div=1):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Interp',   # will show up in GRC
            in_sig=[(np.float32,1024)],
            out_sig=[(np.float32,1024)]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.from_min = from_min
        self.from_max = from_max
        self.to_min = to_min
        self.to_max = to_max
        self.div = div

    def work(self, input_items, output_items):
        a = input_items[0][:].reshape(-1, self.div).mean(1).repeat(self.div).reshape(-1, 1024)

        output_items[0][:] = np.interp(a, [self.from_min, self.from_max], [self.to_min, self.to_max])
        return len(output_items[0])
