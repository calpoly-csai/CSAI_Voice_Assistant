import os
import pyaudio
import sys
import time
import wave

CHANNELS = 1
CHUNK = 2048
RATE = 16000
FORMAT = pyaudio.paInt16
TIME = 2.5
p = pyaudio.PyAudio()
in_device = p.get_default_input_device_info()
out_device = p.get_default_output_device_info()
quit_inp = 0 # var for quitting out of program


# program loop
while (quit_inp != 'q'):    
        feat_type = 0 # wake or not wake work label
        gender = 0 # gender label
        end_desc_sess = 0 # ends the current description session

        # ensures proper input of either ww or notww
        while not(feat_type == "ww" or feat_type == "notww"): 
                feat_type = input("WW or NotWW: ").lower()
        filename = None
        if (feat_type == "ww"):
                target_dir = "Wake Word" # used for setting the correct directory
                ww_noise = 0
                first_name = input("First Name: ").lower() # used for labeling file
                last_name = input("Last Name: ").lower() # ''

                # ensures proper input
                while not (gender == "m" or gender == "f"):
                        gender = input("Male (m) or Female (f): ").lower()

                ww_descr = (input("Enter the description: ").lower()).replace(" ","_") # labeling brief description
                ww_loc = (input("Location: ").lower()).replace(" ","-") # labeling the recording location

                while not(ww_noise == 'q' or ww_noise == 'm' or ww_noise == 'l'):
                        ww_noise = input("Noise Level - Quiet (Q) Moderate (M) Loud (L): ").lower()
                filename = target_dir +\
                                 "/ww_" +\
                                 gender + "_" +\
                                 ww_descr + "_" +\
                                 ww_loc + "_" +\
                                 last_name + "_" +\
                                 first_name + "_" +\
                                 time.strftime("%m%d%Y%H%M%S",time.localtime()) + "_" +\
                                 "aikens.wav"
        else:
                target_dir = "Not Wake Word"
                nww_noise = 0
                nww_descr = ((input("Enter description: ")).lower()).replace(" ","_")
                nww_loc = (input("Location: ").lower()).replace(" ","-")
                
                while not(nww_noise == 'q' or nww_noise == 'm' or nww_noise == 'l'):
                        nww_noise = input("Noise Level - Quiet (Q) Moderate (M) Loud (L): ").lower()
                filename = target_dir +\
                                 "/notww_" +\
                                 nww_descr + "_" +\
                                 nww_loc + "_" +\
                                 time.strftime("%m%d%Y%H%M%S",time.localtime())+ "_" +\
                                 "aikens.wav"
        # description session loop
        while (end_desc_sess != 'e'):
                wf = wave.open(filename, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                print("Recording in 3..")
                time.sleep(1)
                print("             2..")
                time.sleep(1)
                print("             1..")
                time.sleep(1)
                end_time = time.perf_counter() + 2.5
                stream = p.open(rate = RATE,
                                format = FORMAT, 
                                input = True,
                                channels = CHANNELS,
                                input_device_index = in_device.get('index'))
                while(end_time - time.perf_counter() > 0):
                        # read from microphone
                        wf.writeframes(stream.read(CHUNK))
                stream.stop_stream()
                stream.close()
                wf.close()
                play = 'q'
                wf = wave.open(filename, 'rb')
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                channels=wf.getnchannels(),
                                rate=wf.getframerate(),
                                output_device_index = out_device.get('index'),
                                output=True)
                play = input("Play? (p):")
                while (play == "p"):
                        data = wf.readframes(CHUNK)
                        while(len(data) > 0):
                                stream.write(data)
                                data = wf.readframes(CHUNK)
                        play = input("Play? (p):")
                stream.stop_stream()
                stream.close()
                p.terminate()
                wf.close()

                end_desc_sess = input("If finished with description session, type (e); otherwise, type anything else: ").lower()

        quit_inp = input("If finished recording, type (q). Otherwise, type anything else: ").lower()