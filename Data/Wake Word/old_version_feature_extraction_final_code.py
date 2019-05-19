import pyaudio
import wave
import numpy as np
import os
from speechpy.feature import mfcc
import json

# CONSTANTS
RATE = 16000 # sample rate
WINDOW = 0.1 # size of window
STRIDE = 0.05 # time between each window
MFCC = 13 # number of desired MFCCs
FILTER_BANKS = 20 # number of filter banks to compute
FFT_NUM = 512 # length of fast fourier transform window
CURR_PATH = os.getcwd() + "\\" # current path

def Convert_To_MFCC(fileName, path):
        return mfcc(Read_Audio_Data(path + fileName),RATE,WINDOW,STRIDE,MFCC,FILTER_BANKS,FFT_NUM,0,None,True).tolist()

def Read_Audio_Data(fileName):
        #open the wave file
        wf = wave.open(fileName, 'rb')

        #get the packed bytes
        raw_sig = wf.readframes(wf.getnframes())

        #convert the packed bytes into integers
        audio_sig = np.fromstring(raw_sig, 'Int16')

        # close the file
        wf.close()

        return audio_sig

def Obtain_Audio_Data(data_inp):

        # desired dir for data extraction
        audio_dir = CURR_PATH + data_inp + "\\"

        # obtain files within the dir
        audio_list = os.listdir(audio_dir)

        # name of the json file based on user input
        json_type = data_inp.replace(" ","_") + "_data.json"

        # data dictionary
        curr_data = {}

        # if the file is not within the directory
        if not(os.path.isfile(json_type)):

                # create the file
                inp_file = open(json_type,'w')
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
                        curr_data[sample.replace(".wav","")] = Convert_To_MFCC(sample,audio_dir)

        # place contents into the json 
        with open(json_type, 'w') as outfile:
                json.dump(curr_data, outfile)

        print("<<" + json_type + ">> has been stored in the directory: " + str(os.getcwd()))

if __name__ == '__main__':
        data_inp = 0

        while not((data_inp == "Wake Word") or (data_inp == "Not Wake Word")):
                data_inp = input("Enter Desired Data to Process (Wake Word or Not Wake Word): ")

        Obtain_Audio_Data(data_inp)