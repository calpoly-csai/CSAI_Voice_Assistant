"""
Title: False Activation Data Extraction
Author: Viet Nguyen
Date: 07/14/2019
Organization: Cal Poly CSAI
Description: This script take audio file(s) that do not contain the wake word
             ("Nimbus"), perform prediction on them, and dump the frames that
             activate the model.
"""

from pydub import AudioSegment
import numpy as np
from speechpy.feature import mfcc
import wave
import sys
import os
from datetime import datetime
try:
    from keras import models
except ImportError:
    from tensorflow.keras import models

# Globals for audio specs
CHUNK_SIZE = 2048
FORMAT = 'int16'
SAMPLE_WIDTH = 2
NUM_CHANNELS = 1
SAMPLE_RATE = 16000
DURATION = 2.5
NUM_CHUNKS = int(DURATION * SAMPLE_RATE // CHUNK_SIZE)
BYTES_PER_CHUNK = CHUNK_SIZE * SAMPLE_WIDTH * NUM_CHANNELS

# Globals for MFCC specs
WINDOW = .1
STRIDE = .05
MFCC = 13
FILTER_BANKS = 20
FFT_NUM = 512

# Other globals
NUM_BITS_IN_BYTE = 8
PREDICTION_THRESHOLD = .6
NAME = "Smith"


class FalsePosDetect:
    def __init__(self, raw_bytes, model, target_dir, path='rawaudio'):
        self.raw_bytes = raw_bytes
        # Number of intervals
        self.n_intervals = len(self.raw_bytes) // BYTES_PER_CHUNK - \
            NUM_CHUNKS + 1
        if self.n_intervals <= 0:
            raise Exception("%s is too short" % (path))
        self.model = model
        self.target_dir = target_dir
        self.path = path
        self.n_false_pos = 0

    def from_path(path, model, target_dir):
        """Return a FalsePosDetect object given path name, None if invalid."""
        try:
            audio = AudioSegment.from_file(path, sample_width=SAMPLE_WIDTH,
                                           channels=NUM_CHANNELS,
                                           frame_rate=SAMPLE_RATE)
        except:
            print("Not a valid audio file: %s" % (path))
            return
        # Validate audio file, return FPD object if valid.
        if FalsePosDetect.validate(audio, path):
            return FalsePosDetect(audio.raw_data, model, target_dir,
                                  os.path.basename(path))

    def validate(audio, path):
        """Check if an AudioSegment object is of the audio standards."""
        valid = True
        if audio.sample_width != SAMPLE_WIDTH:
            print("Invalid sample width, require %d-bit audio but "
                  "encounter %d-bit audio"
                  % (SAMPLE_WIDTH * NUM_BITS_IN_BYTE, audio.sample_width))
            valid = False
        if audio.frame_rate != SAMPLE_RATE:
            print("Invalid sample rate, require %d-kHz audio but encounter"
                  " %d-kHz audio" % (SAMPLE_RATE, audio.frame_rate))
            valid = False
        if audio.channels != NUM_CHANNELS:
            print("Invalid number of channels, require %d-channel audio "
                  "but encounter %d-channel audio"
                  % (NUM_CHANNELS, audio.channels))
            valid = False
        if not valid:
            print('\t%s' % (path))
        return valid

    def run_detection(self):
        """Run prediction on every possible interval."""
        for i in range(self.n_intervals):
            self.run_interval(i * BYTES_PER_CHUNK,
                              (i + NUM_CHUNKS) * BYTES_PER_CHUNK)

    def print_stats(self):
        """Print the prediction statistics after running run_detection."""
        print(self.path)
        print("\t%d false activations detected out of %d intervals (%.2f%%)"
              % (self.n_false_pos, self.n_intervals,
                 100 * self.n_false_pos / self.n_intervals))

    def run_interval(self, start, end):
        """Do fpd on interval of appropriate size."""
        # Extract MFCC values.
        sample = np.array(mfcc(np.frombuffer(self.raw_bytes[start:end],
                          FORMAT), SAMPLE_RATE, WINDOW, STRIDE, MFCC,
                          FILTER_BANKS, FFT_NUM, 0, None, True))
        # If positively predicted, write interval to wav file.
        if self.model.predict(np.reshape(sample, (1, 46, 13))) >= \
                PREDICTION_THRESHOLD:
            self.write(start, end)
            self.n_false_pos += 1

    def write(self, start, end):
        """Write the raw audio bytes to a wav file in target_dir."""
        with wave.open(
            os.path.join(self.target_dir, "notww_false-act-%s_%s_%s.wav" %
                         (self.path, datetime.now().strftime("%m%d%Y%H%M%S%f"),
                          NAME)),
                'wb') as wave_obj:
            wave_obj.setparams((NUM_CHANNELS, SAMPLE_WIDTH, SAMPLE_RATE,
                               CHUNK_SIZE * NUM_CHUNKS, 'NONE',
                               'not compressed'))
            wave_obj.writeframesraw(self.raw_bytes[start:end])


def driver(path, model, target_dir):
    """Driver to run fpd conveniently."""
    # Construct FPD object from path
    fpd = FalsePosDetect.from_path(path, model, target_dir)
    if fpd is not None:  # If file is of valid format, run detection.
        fpd.run_detection()
        fpd.print_stats()


def main(args):
    if len(args) not in (4, 5):
        print("usage: python %s model source target_dir [name]" % (args[0]))
        return
    model = models.load_model(args[1])
    source = args[2]
    target_dir = args[3]
    if len(args) == 5:  # If name is passed in, change default name.
        global NAME
        NAME = args[4]
    # If source is directory, recursively go through every file in the dir.
    if os.path.isdir(source):
        for dirpath, dirnames, fnames in os.walk(source):
            for fname in fnames:
                print()
                driver(os.path.join(dirpath, fname), model, target_dir)
    else:
        driver(source, model, target_dir)


if __name__ == '__main__':
    main(sys.argv)
