import json
import os
import pyaudio
from speechpy.feature import mfcc
import wave
import numpy as np
import tensorflow as tf
from tensorflow.keras import models, layers
from datetime import datetime
import random

NWW_PATH = "C:\\Users\\cej17\\Documents\\CSAI\\CSAI_Voice_Assistant\\Data\\Wake Word\\Not Wake Word\\"
JSON_PATH = "C:\\Users\\cej17\\Documents\\Coding_Projects\\rand\\"

WW_TRAIN = "Wake_Word_Train_data.json"
NWW_TRAIN = "Not_Wake_Word_Train_data.json"
WW_TEST = "Wake_Word_Test_data.json"
NWW_TEST = "Not_Wake_Word_Test_data.json"

CONFIDENCE = 0.6
GRU_UNITS = 20
DROPOUT = 0.3
ACTIVATIONS = 4
EPOCHS = 30
BATCH_SIZE = 32

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
    model = models.Sequential()
    model.add(layers.GRU(GRU_UNITS, activation='linear', input_shape=(46,13), dropout=DROPOUT, name='net'))
    model.add(layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model


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
    with open(os.path.join(JSON_PATH, WW_TRAIN)) as f_in:
        ww_train_data = json.load(f_in)
        ww_train_data_keys = list(ww_train_data.keys())
        random.shuffle(ww_train_data_keys)

    with open(os.path.join(JSON_PATH, NWW_TRAIN)) as f_in:
        nww_train_data = json.load(f_in)
        nww_train_data_keys = list(nww_train_data.keys())
        random.shuffle(nww_train_data_keys) 

    with open(os.path.join(JSON_PATH, WW_TEST)) as f_in:
        ww_test_data = json.load(f_in)
        ww_test_data_keys = list(ww_test_data.keys())
        random.shuffle(ww_test_data_keys)

    with open(os.path.join(JSON_PATH, NWW_TEST)) as f_in:
        nww_test_data = json.load(f_in)
        nww_test_data_keys = list(nww_test_data.keys())
        random.shuffle(nww_test_data_keys)

    for i in range(len(ww_train_data_keys)):
        train_data.append(ww_train_data[ww_train_data_keys[i]])
        train_labels.append(1)

    for i in range(len(nww_train_data_keys)):
        train_data.append(nww_train_data[nww_train_data_keys[i]])
        train_labels.append(0)

    for i in range(len(ww_test_data_keys)):
        test_data.append(ww_test_data[ww_test_data_keys[i]])
        test_labels.append(1)

    for i in range(len(nww_test_data_keys)):
        test_data.append(nww_test_data[nww_test_data_keys[i]])
        test_labels.append(0)

    model = build_model()

    test_data = np.array(test_data, dtype=float)
    train_data = np.array(train_data, dtype=float)

    model.fit(train_data, train_labels, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1)

    print(model.evaluate(test_data, test_labels))

    model.save("model_" + datetime.now().strftime("%m%d%Y%H%M%S") + ".h5")

else:
    model = 0

    while (model not in os.listdir()):
        model = input("Input Model Name: ")

    model = models.load_model(model)

print(model.summary())
stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)
frames = []
false_act = 0
act_count = 0

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

    data = stream.read(CHUNK)
    frames.append(data)

    if (len(frames) > 19):

        in_data = np.fromstring(np.array(frames[:19]),'Int16')

        audio_sig = np.array([mfcc(in_data, RATE, WINDOW, STRIDE, MFCC, FILTER_BANKS, FFT_NUM, 0, None, True)])

        prediction = model.predict(audio_sig)

        print(prediction)

        if (prediction > CONFIDENCE):
            act_count+=1

            if (act_count >= ACTIVATIONS):
                print("NIMBUS", end=" ", flush=True)

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
            act_count = 0
            print(" ", end="", flush=True)
 
        frames = frames[1:]
