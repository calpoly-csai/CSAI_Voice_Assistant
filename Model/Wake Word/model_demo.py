import json
import os
import pyaudio
from speechpy.feature import mfcc
import wave
import numpy as np
# ============
# Demo Part 1
# Remove 
# ============
CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

WINDOW = 0.1 # size of window
STRIDE = 0.05 # time between each window
MFCC = 13 # number of desired MFCCs
FILTER_BANKS = 20 # number of filter banks to compute
FFT_NUM = 512 # length of fast fourier transform window

def build_model():
    # ============
    # Demo Part 6
    # Remove 
    # ============

p = pyaudio.PyAudio()

ww_test_data = {}
ww_test_data_keys = []

ww_train_data = {}
ww_train_data_keys = []

nww_test_data = {}
nww_test_data_keys = []

nww_train_data = {}
nww_train_data_keys = []

train_data = []
train_labels = []

test_data = []
test_labels = []

read = 0

while not(read == "y" or read == "n"):
    read = input("Train new model? (y or n) ")

if read == "y":
    with open(os.path.join(JSON_PATH,"Wake_Word_Train_data.json")) as f_in:
        # ============
        # Demo Part 2
        # Remove 
        # ============

    with open(os.path.join(JSON_PATH,"Not_Wake_Word_Train_data.json")) as f_in:
        # ============
        # Demo Part 3
        # Remove 
        # ============

    with open(os.path.join(JSON_PATH,"Wake_Word_Test_data.json")) as f_in:
        ww_test_data = json.load(f_in)
        ww_test_data_keys = list(ww_test_data.keys())
        random.shuffle(ww_test_data_keys)

    with open(os.path.join(JSON_PATH,"Not_Wake_Word_Test_data.json")) as f_in:
        nww_test_data = json.load(f_in)
        nww_test_data_keys = list(nww_test_data.keys())
        random.shuffle(nww_test_data_keys)

    for i in range(len(ww_train_data_keys)):
        # ============
        # Demo Part 4
        # Remove 
        # ============

    for i in range(len(nww_train_data_keys)):
        # ============
        # Demo Part 5
        # Remove 
        # ============

    for i in range(len(ww_test_data_keys)):
        test_data.append(ww_test_data[ww_test_data_keys[i]])
        test_labels.append(1)

    for i in range(len(nww_test_data_keys)):
        test_data.append(nww_test_data[nww_test_data_keys[i]])
        test_labels.append(0)

    # ============
    # Demo Part 7
    # Remove 
    # ============

else:
    model = 0
    while (model not in os.listdir()):
        # ============
        # Demo Part 8
        # Remove 
        # ============

# ============
# Demo Part 9
# Remove 
# ============
while not(false_act == "y" or false_act == "n"):
    false_act = input("False Activation Collection Mode? (y or n): ")

    if (false_act == "y"):
        noise = 0
        location = input("Location: ")
        description = input("Type of False Activation: ")

        while not(noise == 'q' or noise == 'm' or noise == 'l'):
            noise = input("Noise Level - Quiet (Q) Moderate (M) Loud (L): ").lower()
print()

while True:

    # ============
    # Demo Part 10
    # Remove 
    # ============

        # ============
        # Demo Part 11
        # Remove 
        # ============

            # ============
            # Demo Part 12
            # Remove 
            # ============

                if(false_act == "y"):

                    file_name = "notww_" + description + "-false_"+ location + "_" + noise +"_" + datetime.now().strftime("%m%d%Y%H%M%S%f") + "_ewenike.wav" 
                    wf = wave.open(os.getcwd() + "\\Not Wake Word\\" + file_name, 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(frames[:19]))
                    wf.close()
                    print("\n<<"+file_name+">> has been saved\n")

        else:
            # ============
            # Demo Part 13
            # Remove 
            # ============

        # ============
        # Demo Part 14
        # Remove 
        # ============
