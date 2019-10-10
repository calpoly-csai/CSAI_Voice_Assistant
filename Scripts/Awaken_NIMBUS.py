'''
Name: Awaken NIMBUS
Author: Chidi Ewenike
Date: 10/10/2019
Organization: Cal Poly CSAI
Description: Detects the wake word of live audio stream
'''

from Utils.Wake_Word_Run_Class import Run_Wake_Word
import argparse
import os
import pyaudio
import json

with open(os.getcwd() + "\\Utils\\PATH.json", "r") as path_json:
    REPO_PATH = json.load(path_json)["PATH"]

parser = argparse.ArgumentParser()
parser.add_argument('-i',
                    action="store",
                    required=True,
                    help="Input Model to Detect Wake Word")
parser.add_argument('-p',
                    action="store_true",
                    required=False,
                    help="Print Out Prediction Scores")
parser.add_argument('-a',
                    action="store",
                    required=False,
                    default=4,
                    help="Number of predictions for an activation")

args = parser.parse_args()

CONFIDENCE = 0.6  # prediction confidence
ACTIVATIONS = args.a  # number of activations for confident activation
CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
WINDOW = 0.128  # size of window
STRIDE = 0.064  # time between each window
MFCC = 13  # number of desired MFCCs
FILTER_BANKS = 20  # number of filter banks to compute
FFT_NUM = 512  # length of fast fourier transform window


def main():
    detection = Run_Wake_Word(input_model=args.i,
                              print_pred=args.p,
                              activations=args.a)

    detection.Run_Detection()


if __name__ == "__main__":
    main()
