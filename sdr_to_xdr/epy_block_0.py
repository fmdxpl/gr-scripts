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

    def __init__(self, bandwidth = 5, low = 3,  high = 5, boost = 1.0, reduce = 1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.bandwidth = bandwidth

        self.low = low
        self.high = high

        self.boost = boost
        self.reduce = reduce
        
        
    def work(self, input_items, output_items):
        #for i in range(0, len(output_items[0])):
        for i in range(0, 1):
            if(input_items[0][i] > self.high):
                self.bandwidth = max(self.bandwidth - self.reduce, 0)
                output_items[0][i]=self.bandwidth
            elif(input_items[0][i] < self.low):
                self.bandwidth = min(self.bandwidth + self.boost, 13)
                output_items[0][i]=self.bandwidth

        #return(len(output_items[0]))
        return(1)
