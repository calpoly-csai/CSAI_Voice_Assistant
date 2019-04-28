# ==============================
# Part 1 of the demo
#
# Remove comments for the demo
# ==============================


def ConvertToMFCC(fileName, path):
# ==============================
# Part 3 of the demo
# Remove pass
# Remove comments for the demo
# ==============================
        pass

def readAudioData(fileName):
# ==============================
# Part 2 of the demo
# Remove pass
# Remove comments for the demo
# ==============================
        pass

def obtainAudioData(data_inp):

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
                        curr_data[sample.replace(".wav","")] = ConvertToMFCC(sample,audio_dir)

        # place contents into the json 
        with open(json_type, 'w') as outfile:
                json.dump(curr_data, outfile)

        print("<<" + json_type + ">> has been stored in the directory: " + str(os.getcwd()))

if __name__ == '__main__':
        data_inp = 0

        while not((data_inp == "Wake Word") or (data_inp == "Not Wake Word")):
                data_inp = input("Enter Desired Data to Process (Wake Word or Not Wake Word): ")

        obtainAudioData(data_inp)