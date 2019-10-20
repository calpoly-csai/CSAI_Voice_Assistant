'''
Name: Run Wake Word Class
Author: Chidi Ewenike
Date: 10/10/2019
Organization: Cal Poly CSAI
Description: Class for detecting the wake word of live audio stream
'''

# Imports
# =============================================================================
import argparse
import json
import os
import pyaudio
import random
import wave

import numpy as np
import tensorflow as tf

from datetime import datetime
from speechpy.feature import mfcc
from tensorflow.keras import models, layers
from Utils.Feature_Extraction_Class import Feature_Extraction
from Utils.OS_Find import Path_OS_Assist
from Utils.WW_Model_Class import Model

delim = Path_OS_Assist()

with open(os.getcwd() + "%sUtils%sPATH.json" % (delim, delim), "r") \
        as path_json:
    REPO_PATH = json.load(path_json)["PATH"]

# Constants
# =============================================================================
CONFIDENCE = 0.6  # prediction confidence
ACTIVATIONS = 4  # number of activations for confident activation

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

WINDOW = 0.128  # size of window
STRIDE = 0.064  # time between each window
MFCC = 13  # number of desired MFCCs
FILTER_BANKS = 20  # number of filter banks to compute
FFT_NUM = 512  # length of fast fourier transform window


class Run_Wake_Word:

    def __init__(self, print_pred, input_model=None, confidence=CONFIDENCE,
                 activations=ACTIVATIONS, chunk=CHUNK,
                 format=FORMAT, channels=CHANNELS, rate=RATE, window=WINDOW,
                 stride=STRIDE, mfcc=MFCC, filter_banks=FILTER_BANKS,
                 fft_num=FFT_NUM):

        self.input_model = input_model
        self.confidence = confidence
        self.activations = activations
        self.chunk = chunk
        self.format = format
        self.channels = channels
        self.rate = rate
        self.window = window
        self.stride = stride
        self.mfcc = mfcc
        self.filter_banks = filter_banks
        self.fft_num = fft_num
        self.print_pred = print_pred
        self.p = pyaudio.PyAudio()
        self.ww_model = Model()

        self.model = self.ww_model.load(self.input_model)

        self.ext_feat = Feature_Extraction()

        self.stream = None
        self.frames = []
        self.act_count = 0

    def Run_Detection(self):
        """
        Runs the false extraction on the input stream

        Args:
            None

        Returns:
            None

        """

        # print the summary of the model
        print(self.ww_model.model.summary(), end="\n\n", flush=True)
        # open an audio data stream
        self.stream = self.p.open(format=self.format, channels=self.channels,
                                  rate=self.rate, input=True,
                                  frames_per_buffer=self.chunk)

        act_count = 0

        while True:

            # reads chunk of audio
            data = self.stream.read(self.chunk)

            # appends chunk to frame list
            self.frames.append(data)

            # begins making predictions after the first
            # 2.5 seconds of audio is read
            if (len(self.frames) > 19):

                prediction = self.Prediction()

                # if the predictions is larger than the defined confidence
                if (prediction > self.confidence):

                    # increment the activation counter
                    act_count += 1

                    # if the number of consecutive activations
                    # exceeds the activation value
                    if(act_count >= self.activations):

                        # print out "nimbus"
                        print(" << nimbus >> ", end=" ", flush=True)

                        # reset activation count
                        act_count = 0

                        self.frames = self.frames[18:]

                # if prediction falls below the confidence level
                else:

                    # reset the activation count
                    act_count = 0

                    if not(self.print_pred):
                        # output nothing to the stream
                        print(".", end="", flush=True)

                # window the data stream
                self.frames = self.frames[1:]

    def Prediction(self):
        """
        Makes a prediction based on the input audio frames
        transformed into MFCCs

        Args:
            None

        Returns:
            None

        """
        # converts first 19 chunks of audio bytes into 16 bit int values
        in_data = np.fromstring(np.array(self.frames[:19]), 'Int16')

        # extract MFCCs from the 19 chunks of audio
        audio_sig = np.array([mfcc(in_data, self.rate, self.window,
                                   self.stride, self.mfcc, self.filter_banks,
                                   self.fft_num, 0, None, True)])

        # makes predictions
        prediction = self.ww_model.model.predict(audio_sig)

        if(self.print_pred):
            print(prediction)

        return prediction
