# =============================================================================
# Title: Audio Recording
# Author: Chidi Ewenike
# Date: 04/19/2019
# Organization: Cal Poly CSAI
# Description: Records audio and labels the recording
# =============================================================================

import json
import os
import pyaudio
import time
import wave
import winsound

from Utils.OS_Find import Path_OS_Assist

delim = Path_OS_Assist()

with open(os.getcwd() + "%sUtils%sPATH.json" %
          (delim, delim), "r") as path_json:
    REPO_PATH = json.load(path_json)["PATH"]

USER_NAME = "ewenike"

CHUNK = 2048  # Buffer size
FORMAT = pyaudio.paInt16  # Sample Size
CHANNELS = 1  # Sample Depth
RATE = 16000  # Sample Rate
RECORD_SECONDS = 2.5  # Recording Time
quit_inp = 0  # var for quitting out of program

# program loop
while (quit_inp != 'q'):
    feat_type = 0  # wake or not wake work label
    gender = 0  # gender label
    end_desc_sess = 0  # ends the current description session

    # ensures proper input of either ww or notww
    while not(feat_type == "ww" or feat_type == "notww"):
        feat_type = input("WW or NotWW: ").lower()

    if (feat_type == "ww"):

        target_dir = "Wake Word"  # used for setting the correct directory
        ww_noise = 0
        first_name = input("First Name: ").lower()  # used for labeling file
        last_name = input("Last Name: ").lower()

        # ensures proper input
        while not (gender == "m" or gender == "f"):
            gender = input("Male (m) or Female (f): ").lower()

        # labeling brief description
        ww_descr = (input("Enter the description: ").lower()).replace(" ", "-")

        # labeling the recording location
        ww_loc = (input("Location: ").lower()).replace(" ", "-")

        while not(ww_noise == 'q' or ww_noise == 'm' or ww_noise == 'l'):
            ww_noise = input("Noise Level - Quiet (Q) "
                             "Moderate (M) Loud (L): ").lower()

    else:
        target_dir = "Not Wake Word"
        nww_noise = 0
        nww_descr = ((input("Enter description: ")).lower()).replace(" ", "-")
        nww_loc = (input("Location: ").lower()).replace(" ", "-")

        while not(nww_noise == 'q' or nww_noise == 'm' or nww_noise == 'l'):
            nww_noise = input("Noise Level - Quiet (Q) Moderate (M) "
                              "Loud (L): ").lower()

    while (end_desc_sess != 'e'):

        # PyAudio instantiation
        p = pyaudio.PyAudio()

        # Audio data byte list
        frames = []

        # Count down
        print("Recording in\n3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
        print("**RECORDING**")

        # Starts the audio stream
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                        input=True, output=True, frames_per_buffer=CHUNK)

        # Reads the audio data buffer and adds it to the "frames" list
        for i in range(0, int(RATE/CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("**RECORDING ENDED**")

        # Audio playback
        while(input("Play Audio (p): ").lower() == 'p'):
            for values in frames:
                stream.write(values)

        # Stop and close the audio stream
        stream.stop_stream()
        stream.close()

        # Destruct the PyAudio instantiation
        p.terminate()

        # Skip the audio save if "d"
        if (input("To delete, type (d): ").lower() == 'd'):
            pass
        else:
            # Get the current time
            curr_time = time.strftime("%m%d%Y%H%M%S", time.localtime())

            # Save the file name
            if (feat_type == "ww"):
                file_name = "ww_" + gender + "_" + ww_descr + "_" + \
                             ww_loc + "_" + ww_noise + "_" + last_name + \
                             "_" + first_name + "_" + curr_time + "_" + \
                             USER_NAME + ".wav"

            else:
                file_name = "notww_" + nww_descr + "_" + nww_loc + "_" + \
                            nww_noise + "_" + curr_time + "_" + USER_NAME + \
                            ".wav"

            print(file_name + " has been saved.")

            # Store the audio in the "Data/Target directory"
            # <<FOR LINUX OR MAC OS, REPLACE \\ with />>
            wf = wave.open("%s%sData%sWakeWord%sAudio%s%s%s%s" %
                           (REPO_PATH, delim, delim, delim, delim,
                            target_dir, delim, file_name), 'wb')

            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

        end_desc_sess = input("If finished with description session,"
                              "type (e); otherwise, type anything else:"
                              ).lower()

    quit_inp = input("If finished recording, type (q). Otherwise, "
                     "type anything else: ").lower()
