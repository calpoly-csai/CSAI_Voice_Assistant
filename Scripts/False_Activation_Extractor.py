"""
Title: Run False Activation Extraction
Author: Chidi Ewenike
Date: 08/06/2019
Organization: Cal Poly CSAI
Description: Runs false activations on input data

"""

from Utils.False_Activation_Extractor_Class import False_Activation
import argparse
import os
import pyaudio
import json

with open(os.getcwd() + "\\Utils\\PATH.json", "r") as path_json:
    REPO_PATH = json.load(path_json)["PATH"]

parser = argparse.ArgumentParser()
parser.add_argument('-i',
                    action="store",
                    required=False,
                    help="Input Model to Detect False Activations")
parser.add_argument('-r',
                    action="store_true",
                    required=False,
                    help="Continuously Retrain the Same Model")
parser.add_argument('-l',
                    action="store",
                    required=True,
                    help="Location of NWW")
parser.add_argument('-d',
                    action="store",
                    required=True,
                    help="Environment/Conditions Description")
parser.add_argument('-p',
                    action="store_true",
                    required=False,
                    help="Print Out Prediction Scores")

args = parser.parse_args()

LAST_NAME = "ewenike"

NWW_PATH = REPO_PATH + "\\Data\\WakeWord\\Audio\\Not Wake Word\\"

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


def main():
    false_activation = False_Activation(input_model=args.i,
                                        retrain=args.r,
                                        location=args.l,
                                        description=args.d,
                                        print_pred=args.p)

    false_activation.Run_Extraction()


if __name__ == "__main__":
    main()
