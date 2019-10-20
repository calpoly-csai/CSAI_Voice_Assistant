'''
Title: Feature Extraction Class
Author: Chidi Ewenike
Date: 04/19/2019
Organization: Cal Poly CSAI
Description: Class that extracts and saves MFCCs

'''

import json
import os
import pyaudio
import sys
import wave

import numpy as np

from speechpy.feature import mfcc
from Utils.OS_Find import Path_OS_Assist

# CONSTANTS
RATE = 16000  # sample rate
WINDOW = 0.128  # size of window
STRIDE = 0.064  # time between each window
MFCC = 13  # number of desired MFCCs
FILTER_BANKS = 20  # number of filter banks to compute
FFT_NUM = 512  # length of fast fourier transform window

delim = Path_OS_Assist()

with open(os.getcwd() + "%sUtils%sPATH.json" % (delim, delim), "r") \
        as PATH_JSON:
    REPO_PATH = json.load(PATH_JSON)["PATH"]

AUDIO_PATH = "%sData%sWakeWord%sAudio" % (delim, delim, delim)


class Feature_Extraction:
    def __init__(self):
        self.words = {}

    def Convert_To_MFCC(self, wf):
        '''
        Converts audio byte streams to MFCCs

        Args:
            wf - wave object

        Return:
            MFCCs - list of float lists
        '''

        return mfcc(self.Read_Audio_Data(wf), RATE, WINDOW, STRIDE, MFCC,
                    FILTER_BANKS, FFT_NUM, 0, None, True).tolist()

    def Read_Audio_Data(self, wf):
        '''
        Reads in the wav file and stores the bytes as a 16-bit integer

        Args:
            wf - wave object

        Return
            audio_sig - list of integers

        '''
        # get the packed bytes
        raw_sig = wf.readframes(wf.getnframes())

        # convert the packed bytes into integers
        audio_sig = np.fromstring(raw_sig, 'Int16')

        # close the file
        wf.close()

        return audio_sig

    def Obtain_WW_Audio_Data(self):
        '''
        Reads all the audio files, extracts the MFCCs, and
        stores them in JSON files

        Args:
            None


        Return:
            None
        '''
        data_dirs = ['Not_Wake_Word%sTrain_Data' % delim,
                     'Not_Wake_Word%sTest_Data' % delim,
                     'Wake_Word%sTrain_Data' % delim,
                     'Wake_Word%sTest_Data' % delim]

        ww_data = {}
        nww_data = {}

        for data_inp in data_dirs:
            # desired dir for data extraction
            audio_dir = REPO_PATH + AUDIO_PATH + delim + data_inp + delim

            # obtain files within the dir
            audio_list = os.listdir(audio_dir)

            word = data_inp.split(delim)[0]

            type_of_data = data_inp.split(delim)[1]

            # name of the json file based on user input
            json_type = word + "_" + type_of_data + ".json"

            # data dictionary
            curr_data = {}

            # if the file is not within the directory
            if not(os.path.isfile(json_type)):

                # create the file
                inp_file = open(json_type, 'w')
                inp_file.close()

                # add the dict to the json
                with open(json_type, 'a') as outfile:
                    json.dump(curr_data, outfile)

            # load the contents of the data json
            with open(json_type) as f_in:
                curr_data = json.load(f_in)

            # obtain each audio sample from the desired dir
            for sample in audio_list:

                # process the sample if it is not processed yet
                if (sample not in curr_data):
                    wf = wave.open(audio_dir + sample, 'rb')

                    if (wf.getnchannels() == 1 and wf.getsampwidth() == 2 and
                            wf.getframerate() == 16000):

                        mfcc = self.Convert_To_MFCC(wf)
                        curr_data[sample.replace(".wav", "")] = mfcc

            if "Not Wake Word" in data_inp:
                nww_data.update(curr_data)

            else:
                ww_data.update(curr_data)

            # place contents into the json
            with open(REPO_PATH + "%sData%sWakeWord%sMFCC%s%s" %
                      (delim, delim, delim, delim, json_type), "w") as outfile:
                json.dump(curr_data, outfile)

            print("<<" + json_type + ">> has been stored in"
                  "the directory: " + str(os.getcwd()))

        with open(REPO_PATH + "%sData%sWakeWord%sMFCC%sww_data.json" %
                  (delim, delim, delim, delim), "w") as outfile:
            json.dump(ww_data, outfile)

        print("<<ww_data.json>> has been stored")

        with open(REPO_PATH + "%sData%sWakeWord%sMFCC%snww_data.json" %
                  (delim, delim, delim, delim), "w") as outfile:
            json.dump(nww_data, outfile)

        print("<<nww_data.json>> has been stored.")
