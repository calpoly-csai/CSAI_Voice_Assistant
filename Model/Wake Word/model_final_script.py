import tensorflow as tf
from tensorflow.keras import models, layers
import json
import numpy as np
import os
import pyaudio
from speechpy.feature import mfcc
from datetime import datetime
import wave
import random
from pydub import AudioSegment
from pydub.playback import play

song = AudioSegment.from_wav("tessa_hello.wav")
NWW_PATH = "C:\\Users\\Jason Ku\\Downloads\\CSAI_Voice_Assistant\\Data\\Wake Word\\Not Wake Word\\"
JSON_PATH = "C:\\Users\\Jason Ku\\Downloads\\CSAI_Voice_Assistant\\Data\\Wake Word\\"

# NWW_PATH = 'C:\\Users\\username\\Documents\\CSAI\\CSAI_Voice_Assistant\\Data\\Wake Word\\Not Wake Word'
# JSON_PATH = "C:\\Users\\username\Documents\\CSAI\\CSAI_Voice_Assistant\\Data\\Wake Word

# Name of json data files
WW_TRAIN = "Wake_Word_Train_data.json"
NWW_TRAIN = "Not_Wake_Word_Train_data.json"
WW_TEST = "Wake_Word_Test_data.json"
NWW_TEST = "Not_Wake_Word_Test_data.json"

CONFIDENCE = 0.6  # Prediction confidence
GRU_UNITS = 20  # GRU unit size
DROPOUT = 0.3  # Dropout size
ACTIVATIONS = 5  # Number of activations for confident activation
EPOCHS = 30  # Number of fwd and bckwd props
BATCH_SIZE = 32  # Batch size

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

WINDOW = 0.1  # Size of window
STRIDE = 0.05  # Time between each window
MFCC = 13  # Number of desired MFCCs
FILTER_BANKS = 20  # Number of filter banks to compute
FFT_NUM = 512  # Length of fast fourier transform window


def build_model():

    # Define a model as a sequence of layers
    model = models.Sequential()

    # Add first layer which is the GRU
    model.add(layers.GRU(GRU_UNITS, activation='linear', input_shape=(46, 13), dropout=DROPOUT, name='net'))

    # Add second layer which is a output for binary classification
    model.add(layers.Dense(1, activation='sigmoid'))

    # Define loss and optimzer fns
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

p = pyaudio.PyAudio()

# Wake word train & test data with shuffled list of keys
ww_test_data = {}
ww_test_data_keys = []
ww_train_data = {}
ww_train_data_keys = []

# Not wake word train & test data with shuffled list of keys
nww_test_data = {}
nww_test_data_keys = []
nww_train_data = {}
nww_train_data_keys = []

# Input list of training & test data and labels
train_data = []
train_labels = []
test_data = []
test_labels = []

read = 0

while not(read == "y" or read == "n"):
    read = input("Train New Model? (y or n) ")

if read == "y":

    # Open the JSON from the path containing the data JSON
    with open(os.path.join(JSON_PATH, WW_TRAIN)) as f_in:
        # Load the data from the json into a dict
        ww_train_data = json.load(f_in)
        # Obtain list of keys
        ww_train_data_keys = list(ww_train_data.keys())
        # Shuffle the list
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

    # Iterate through the list of ww train keys
    for i in range(len(ww_train_data_keys)):
        # Hash into the dict and store it in the input list
        train_data.append(ww_train_data[ww_train_data_keys[i]])
        # Label the corresponding data
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

    # Call the build_model fn which returns the model
    model = build_model()

    # Convert the data lists to np arrays of type float
    test_data = np.array(test_data, dtype=float)
    train_data = np.array(train_data, dtype=float)

    # Train the model
    model.fit(train_data, train_labels, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1)

    # Evaluate the model with the test data
    print(model.evaluate(test_data, test_labels))

    # Save the model
    model.save("model_" + datetime.now().strftime("%m%d%Y%H%M%S%f") + ".h5")

else:
    model = 0

    # If the model is in not the current directory
    while (model not in os.listdir(os.getcwd())):
        # Input the name of the model
        model = input("Input Model Name: ")

    # Load the desired model
    model = models.load_model(model)

# Print the summary of the model
print(model.summary())

# Open an audio data stream
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Contains the chunks of streamed data
frames = []

# False activation mode indicator
false_act = 0

# Counts for confident activations
act_count = 0

# False activation mode
while not(false_act == "y" or false_act == "n"):
    false_act = input("False Activation Collection Mode? (y or n): ").lower()

    if (false_act == "y"):
        noise = 0
        location = input("Location: ")
        description = input("Type of False Activation: ")

        while not(noise == 'q' or noise == 'm' or noise == 'l'):
            noise = input("Noise Level - Quiet (Q) Moderate (M) Loud (L): ").lower()
print()

while True:
    # Reads chunk of audio
    data = stream.read(CHUNK)

    # Appends chunk to frame list
    frames.append(data)
    print("("+str(act_count)+")", end="", flush=True)

    # Begins making predictions after the first 2.5 seconds of audio is read
    if (len(frames) > 19):

        # Converts first 19 chunks of audio bytes into 16 bit int values
        in_data = np.fromstring(np.array(frames[:19]), 'Int16')

        # Extract MFCCs from the 19 chunks of audio
        audio_sig = np.array([mfcc(in_data, RATE, WINDOW, STRIDE, MFCC, FILTER_BANKS, FFT_NUM, 0, None, True)])

        # Makes predictions
        prediction = model.predict(audio_sig)

        # Print(prediction)

        # If the predictions is larger than the defined confidence
        if (prediction > CONFIDENCE):

            # Increment the activation counter
            act_count += 1

            # If the number of consecutive activations exceeds the activation value
            if(act_count >= ACTIVATIONS):
                play(song)
                # Print out "NIMBUS"
                print("NIMBUS", end=" ", flush=True)

                # Reset activation count
                act_count = 0

                # If false activation occurs in false activation mode
                if(false_act == "y"):

                    # Store the wav
                    file_name = "notww_" + description + "-false_" + location + "_" + noise + "_" + datetime.now().strftime("%m%d%Y%H%M%S%f") + "_ku.wav"
                    wf = wave.open(os.path.join(NWW_PATH, file_name), 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(frames[:19]))
                    wf.close()
                    print("\n<<" + file_name + ">> has been saved\n")
                test = input("paused")

        # If prediction falls below the confidence level
        else:
            # Reset the activation count
            act_count = 0

            # Output nothing to the stream
            print(".", end="", flush=True)

        # Window the data stream
        frames = frames[1:]
