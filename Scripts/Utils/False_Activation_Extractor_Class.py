"""
Title: False Activation Extractor
Author: Chidi Ewenike
Date: 07/15/2019
Organization: Cal Poly CSAI
Description: Class which detects and stores false activations predicted
             by a model

"""


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

with open(os.getcwd() + "%sUtils%sPATH.json" %
          (delim, delim), "r") as path_json:
    REPO_PATH = json.load(path_json)["PATH"]

# Constants
# =============================================================================
LAST_NAME = "ewenike"

NWW_PATH = REPO_PATH + "%sData%sWakeWord%sAudio%sNot_Wake_Word%s" % \
           (delim, delim, delim, delim, delim)

CONFIDENCE = 0.6  # prediction confidence
ACTIVATIONS = 4  # number of activations for confident activation

FALSE_COUNT = 4

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

WINDOW = 0.128  # size of window
STRIDE = 0.064  # time between each window
MFCC = 13  # number of desired MFCCs
FILTER_BANKS = 20  # number of filter banks to compute
FFT_NUM = 512  # length of fast fourier transform window


class False_Activation:

    def __init__(self, location, print_pred, description, randomize,
                 input_model=None,
                 false_count=FALSE_COUNT, retrain=False, last_name=LAST_NAME,
                 nww_path=NWW_PATH, confidence=CONFIDENCE,
                 activations=ACTIVATIONS, chunk=CHUNK, format=FORMAT,
                 channels=CHANNELS, rate=RATE, window=WINDOW, stride=STRIDE,
                 mfcc=MFCC, filter_banks=FILTER_BANKS, fft_num=FFT_NUM):

        self.input_model = input_model
        self.location = location
        self.description = description
        self.false_count = false_count
        self.last_name = last_name
        self.nww_path = nww_path
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
        self.retrain = retrain
        self.randomize = randomize

        self.model = self.ww_model.load(self.input_model)

        self.ext_feat = Feature_Extraction()

        self.stream = None
        self.frames = []
        self.false_files = []
        self.act_count = 0
        self.false_count = FALSE_COUNT
        self.false_counts = 0

    def Run_Extraction(self):
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

                        self.False_Activation()

                        self.frames = self.frames[18:]

                    if (self.false_counts >= self.false_count):
                        self.Retrain_Model()

                # if prediction falls below the confidence level
                else:

                    # reset the activation count
                    act_count = 0

                    if not(self.print_pred):
                        # output nothing to the stream
                        print("-", end="", flush=True)

                # window the data stream
                self.frames = self.frames[1:]

    def Retrain_Model(self):
        """
        Retrains a Model object model with the new false wake word data

        Args:
            None

        Returns:
            None

        """

        self.stream.close()

        random.shuffle(self.false_files)

        Path_To = REPO_PATH + "%sData%sWakeWord%sAudio%sNot_Wake_Word%s" % \
            (delim, delim, delim, delim, delim)

        for files in self.false_files[:self.false_count - 1]:
            os.rename(Path_To + files, "%s%sTrain_Data%s%s" %
                      (Path_To, delim, delim, files))

        os.rename(Path_To + self.false_files[self.false_count - 1],
                  "%s%sTest_Data%s%s" %
                  (Path_To, delim, delim,
                   self.false_files[self.false_count - 1]))

        self.false_counts = 0
        self.false_files = []
        self.ext_feat.Obtain_WW_Audio_Data()

        if not(self.retrain):
            self.ww_model = Model()
            self.ww_model.build_model()

        if not(self.randomize):
            self.ww_model.preprocess()

        else:
            self.ww_model.randomized_preprocess()

        self.ww_model.train_model()

        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate, input=True,
                                  frames_per_buffer=self.chunk)

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

    def False_Activation(self):
        """
        Saves the input byte buffer as a wav file

        Args:
            None

        Returns:
            None

        """
        # if false activation occurs in false activation mode
        self.false_counts += 1

        # store the wav
        file_name = "notww_%s-false_%s_%s_%s.wav" \
                    % (self.description,
                       self.location,
                       datetime.now().strftime("%m%d%y%H%M%S_"),
                       self.last_name)

        wf = wave.open(self.nww_path + file_name, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames[:19]))
        wf.close()
        print("\n<<" + file_name + ">> has been saved\n")

        self.false_files.append(file_name)
