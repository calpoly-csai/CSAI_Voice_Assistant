"""
Title: Run False Activation Extraction
Author: Chidi Ewenike
Date: 08/06/2019
Organization: Cal Poly CSAI
Description: Runs false activations on input data

"""

from Utils.OS_Find import Path_OS_Assist
from Utils.False_Activation_Extractor_Class import False_Activation
import argparse
import os
import pyaudio
import json

delim = Path_OS_Assist()

with open(os.getcwd() + "%sUtils%sPATH.json" % (delim, delim), "r") \
        as path_json:
    REPO_PATH = json.load(path_json)["PATH"]

parser = argparse.ArgumentParser()
parser.add_argument('-i',
                    action="store",
                    required=True,
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
parser.add_argument('-n',
                    action="store",
                    required=False,
                    help="Number of false activations before train",
                    default=4)
parser.add_argument('-a',
                    action="store",
                    required=False,
                    default=4,
                    help="Number of predictions for an activation")
parser.add_argument('--rand',
                    action="store_true",
                    required=False,
                    help="Randomize training and test data")

args = parser.parse_args()

LAST_NAME = "ewenike"

NWW_PATH = REPO_PATH + "%sData%sWakeWord%sAudio%sNot Wake Word%s" % \
           (delim, delim, delim, delim, delim)

CONFIDENCE = 0.6  # prediction confidence
ACTIVATIONS = args.a  # number of activations for confident activation
FALSE_COUNT = args.n
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
                                        print_pred=args.p,
                                        randomize=args.rand
                                        )

    false_activation.Run_Extraction()


if __name__ == "__main__":
    main()
