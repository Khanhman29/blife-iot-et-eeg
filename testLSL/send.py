
import sys
import getopt

import time
from random import random as rand

from pylsl import StreamInfo, StreamOutlet, local_clock


def main():
    srate = 1
    name = 'HMIResultData'
    type = 'EEG'
    n_channels = 1
    help_string = 'SendData.py -s <sampling_rate> -n <stream_name> -t <stream_type>'


    # first create a new stream info (here we set the name to BioSemi,
    # the content-type to EEG, 8 channels, 100 Hz, and float-valued data) The
    # last value would be the serial number of the device or some other more or
    # less locally unique identifier for the stream as far as available (you
    # could also omit it but interrupted connections wouldn't auto-recover)
    info = StreamInfo(name, type, n_channels, srate, 'float32', 'myuid34234')

    # next make an outlet
    outlet = StreamOutlet(info)

    print("now sending data...")
    start_time = local_clock()
    sent_samples = 0
    cnt=0
    while True:
        a = 0
        elapsed_time = local_clock() - start_time
        required_samples = int(srate * elapsed_time) - sent_samples
        
        for sample_ix in range(required_samples):
            # make a new random n_channels sample; this is converted into a
            # pylsl.vectorf (the data type that is expected by push_sample)
            cnt+=1
            if(cnt>2):
                cnt =0
                a=1
            mysample = [int(a)]
            # now send it
            outlet.push_sample(mysample)
            print(mysample)
            if (cnt == 0):
                a=0
        
        sent_samples += required_samples
        # now send it and wait for a bit before trying again.
        time.sleep(0.01)


if __name__ == '__main__':
    main()