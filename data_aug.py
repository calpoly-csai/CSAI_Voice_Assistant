"""
Title: Audio Data Augmentation and Generator
Author: Viet Nguyen
Date: 10/19/2019
Organization: Cal Poly CSAI
Description: This library provide 2 classes: AudioAugmenter and DataGenerator.
"""

import wave
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
import random
import math
import os
import sys

# Globals for audio specs
CHUNK_SIZE = 2048
SAMPLE_WIDTH = 2
FORMAT = 'int%d' % (SAMPLE_WIDTH * 8)
NUM_CHANNELS = 1
SAMPLE_RATE = 16000
DURATION = 4
NUMCHUNKS = int(DURATION * SAMPLE_RATE // CHUNK_SIZE)
BYTES_PER_CHUNK = CHUNK_SIZE * SAMPLE_WIDTH * NUM_CHANNELS
MAX_PITCH_FACTOR = 200
MAX_WN_AMP = 20
MIN_WN_AMP = 0
MAX_SPEED = 2

# set DURATION to be the actual duration that the model takes
DURATION = NUMCHUNKS * CHUNK_SIZE / SAMPLE_RATE


class AudioAugmenter:
    """ A wrapper for raw audio that provides methods to augment the audio

        The purpose is to artificially create new data. Every augmentation
        method returns an AudioAugmenter, which allows for chaining.
    """
    def __init__(self, audio=None, raw_bytes=None, sample_width=SAMPLE_WIDTH,
                 sample_rate=SAMPLE_RATE, num_channels=NUM_CHANNELS):
        if audio is not None:
            self.audio = audio
            self.raw_bytes = audio.raw_data

            self.sample_width = audio.sample_width
            self.sample_rate = audio.frame_rate
            self.num_channels = audio.channels
            self.dtype = 'int%d' % (self.sample_width * 8)
        elif raw_bytes is not None:
            self.raw_bytes = raw_bytes

            self.sample_width = sample_width
            self.sample_rate = sample_rate
            self.num_channels = num_channels
            self.dtype = 'int%d' % (self.sample_width * 8)

            self.audio = AudioSegment(data=self.raw_bytes,
                                      sample_width=self.sample_width,
                                      frame_rate=self.sample_rate,
                                      channels=self.num_channels)
        else:
            raise ValueError("raw_bytes and audio can not both be None")

    def from_file(path, strict=True):
        try:
            audio = AudioSegment.from_file(path)
        # bad practice but necessary because not obvious what exceptions the
        # function may raise
        except:
            print("Not a valid audio file: %s" % (path))
            return
        if strict:
            print("Validating %s" % (path))
            if not AudioAugmenter.validate(audio):
                return
        return AudioAugmenter(audio=audio)

    def validate(audio):
        """Check if an AudioSegment object is of the audio standards"""
        valid = True
        if audio.sample_width != SAMPLE_WIDTH:
            print("\tInvalid sample width, require %d-bit audio but "
                  "encounter %d-bit audio"
                  % (SAMPLE_WIDTH * NUM_BITS_IN_BYTE, audio.sample_width))
            valid = False
        if audio.frame_rate != SAMPLE_RATE:
            print("\tInvalid sample rate, require %d-kHz audio but encounter"
                  " %d-kHz audio" % (SAMPLE_RATE, audio.frame_rate))
            valid = False
        if audio.channels != NUM_CHANNELS:
            print("\tInvalid number of channels, require %d-channel audio "
                  "but encounter %d-channel audio"
                  % (NUM_CHANNELS, audio.channels))
            valid = False
        return valid

    def pad(self, target_duration=DURATION, mode='random'):
        """Pad the audio to a target length"""
        if mode not in ('head', 'tail', 'symmetric', 'random'):
            raise ValueError("Padding mode must be 'head', 'tail', "
                             "'symmetric', or 'random'")

        padding_len = target_duration * 1000 - len(self.audio)
        if padding_len < 0:
            raise ValueError("Input audio is longer than target")

        if mode == 'head':
            head_len = padding_len
        elif mode == 'tail':
            head_len = 0
        elif mode == 'symmetric':
            head_len = padding_len // 2
        else:
            head_len = random.randrange(padding_len + 1)

        new_audio = (AudioSegment.silent(duration=head_len,
                                         frame_rate=self.sample_rate)
                     + self.audio
                     + AudioSegment.silent(duration=padding_len - head_len,
                                           frame_rate=self.sample_rate))
        return AudioAugmenter(audio=new_audio)

    def change_pitch(self, shift_amount=None):
        """Change the audio pitch"""
        if shift_amount is None:
            shift_amount = random.randrange(-300, 300)
        fr = 100
        sz = self.sample_rate // fr
        c = len(self.raw_bytes) // self.sample_width // sz
        shift = shift_amount // fr
        interval = sz * self.sample_width
        aggregator = bytes()
        for num in range(c):
            da = np.frombuffer(self.raw_bytes[num*interval: (num+1)*interval],
                               dtype=np.int16)
            left, right = da[0::2], da[1::2]
            lf, rf = np.fft.rfft(left), np.fft.rfft(right)
            lf, rf = np.roll(lf, shift), np.roll(rf, shift)
            if shift_amount >= 0:
                lf[0:shift], rf[0:shift] = 0, 0
            else:
                lf[shift:], rf[shift:] = 0, 0
            nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
            ns = np.column_stack((nl, nr)).ravel().astype(np.int16)
            aggregator += ns.tobytes()
        return AudioAugmenter(raw_bytes=aggregator,
                              sample_width=self.sample_width,
                              sample_rate=self.sample_rate,
                              num_channels=self.num_channels)

    def add_noise(self, amplitude=None):
        """Add random noise"""
        if amplitude is None:
            amplitude = np.random.randint(0, 1000)
        np_data = np.frombuffer(self.raw_bytes, dtype=self.dtype)
        noise = np.random.randint(0, amplitude, size=np_data.shape,
                                  dtype=self.dtype)
        return AudioAugmenter(raw_bytes=(np_data + noise).tobytes(),
                              sample_width=self.sample_width,
                              sample_rate=self.sample_rate,
                              num_channels=self.num_channels)

    def speed_up(self, factor=None):
        """Speed up the audio by a factor"""
        if factor is None or factor < 1:
            factor = random.uniform(1, MAX_SPEED)
        return AudioAugmenter(audio=self.audio.speedup(playback_speed=factor))


class DataGenerator:
    """ A generator for audio data, can be fed into TensorFlow's train function

        A generator-like object that randomly applies augmentation methods from
        AudioAugmenter.
    """
    def __init__(self, augs):
        self.original_augs = augs

    def from_file(path):
        augs = []
        if os.path.isdir(path):
            for dirpath, dirnames, fnames in os.walk(source):
                for fname in fnames:
                    aug = AudioAugmenter.from_file(os.path.join(dirpath,
                                                                fname))
                    if aug is not None:
                        augs.append(aug)
        else:
            aug = AudioAugmenter.from_file(path)
            if aug is not None:
                augs.append(aug)
        return DataGenerator(augs)

    def from_bytes(raw_bytes_list):
        return DataGenerator([AudioAugmenter(raw_bytes=raw_bytes)
                              for raw_bytes in raw_bytes_list])

    def __next__(self):
        aug = (random.choice(self.original_augs).speed_up().change_pitch()
               .add_noise().pad())
        return aug.raw_bytes
        sample = (
            np.array(mfcc(np.frombuffer(aug.raw_bytes, dtype='int%d'
                                        % (self.sample_width * 8)),
                          SAMPLE_RATE, WINDOW, STRIDE, MFCC, FILTER_BANKS,
                          FFT_NUM, 0, None, True)).reshape((1, -1)))
        return shape

    def __iter__(self):
        return self


def test():
    generator = DataGenerator.from_file(sys.argv[1])
    while True:
        play(AudioSegment(next(generator), sample_width=SAMPLE_WIDTH,
                          frame_rate=SAMPLE_RATE, channels=NUM_CHANNELS))


if __name__ == '__main__':
    test()
