import pyaudio
import wave
import numpy as np
import os
from speechpy.feature import mfcc
import json
import random

# CONSTANTS
RATE = 16000  # Sample rate
WINDOW = 0.1  # Size of window
STRIDE = 0.05  # Time between each window
MFCC = 13  # Number of desired MFCCs
FILTER_BANKS = 20  # Number of filter banks to compute
FFT_NUM = 512  # Length of fast fourier transform window
CURR_PATH = os.getcwd() + "\\"  # Current path
PERCENT_TRAIN = 80  # Percent of sample to designate for training


def Convert_To_MFCC(wf):
        return mfcc(Read_Audio_Data(wf), RATE, WINDOW, STRIDE, MFCC,
                    FILTER_BANKS, FFT_NUM, 0, None, True).tolist()


def Read_Audio_Data(wf):
        # Get the packed bytes
        raw_sig = wf.readframes(wf.getnframes())

        # Convert the packed bytes into integers
        audio_sig = np.fromstring(raw_sig, 'Int16')

        # Close the file
        wf.close()

        return audio_sig


def Obtain_Audio_Data(data_inp):
        # Desired dir for data extraction
        audio_dir = CURR_PATH + data_inp + "\\"
        print(audio_dir)

        # Obtain files within the dir
        audio_list = os.listdir(audio_dir)

        # Names of the json files based on user input
        json_type_train = data_inp.replace(" ", "_") + "_" + "Train_data.json"
        json_type_test = data_inp.replace(" ", "_") + "_" + "Test_data.json"

        # Data dictionaries
        curr_data_train = {}
        curr_data_test = {}

        # Create the files and add dictionary to each json
        inp_file = open(json_type_train, 'w')
        inp_file.close()
        with open(json_type_train, 'a') as outfile:
                json.dump(curr_data_train, outfile)

        # Repeat for test data
        inp_file = open(json_type_test, 'w')
        inp_file.close()
        with open(json_type_test, 'a') as outfile:
            json.dump(curr_data_test, outfile)

        # Load the contents of each data json
        with open(json_type_train) as f_in_train:
            curr_data_train = json.load(f_in_train)
        with open(json_type_test) as f_in_test:
            curr_data_test = json.load(f_in_test)

        # Obtain each audio sample from the desired dir
        for sample in audio_list:
            wf = wave.open(audio_dir + sample, 'rb')

            # Randomly put data into test/training dictionaries
            if (wf.getnchannels() == 1 and wf.getsampwidth() == 2 and
                    wf.getframerate() == RATE):
                rand = random.randint(1, 101)
                if (rand <= PERCENT_TRAIN):
                    curr_data_train[sample.replace(".wav", "")] = \
                        Convert_To_MFCC(wf)
                else:
                    curr_data_test[sample.replace(".wav", "")] = \
                        Convert_To_MFCC(wf)
            else:
                print("<<" + sample + ">> is of invalid format.")

        # Place contents into the json
        with open(json_type_train, 'w') as outfile:
            json.dump(curr_data_train, outfile)
        with open(json_type_test, 'w') as outfile:
            json.dump(curr_data_test, outfile)
        print("Files have been stored in the directory: " + str(os.getcwd()))

if __name__ == '__main__':
        data_inp = 0
        type_inp = 0

        while not((data_inp.lower() == "ww") or (data_inp.lower() == "nww")):
                data_inp = input("Enter Desired Data to Process (ww or nww): ")

        Obtain_Audio_Data(data_inp)
