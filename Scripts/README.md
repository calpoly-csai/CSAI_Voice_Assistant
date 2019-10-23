To run these programs, you must ensure that you have the following:

1. Python 3.x
2. Pyaudio (python -m pip install pyaudio)
3. Wave (pip install wave)

All programs need to be run from the Scripts directory. Programs will not run otherwise.

Also, you need to ensure that the path to the CSAI Voice Assistant repository is in the Scripts/Utils/READ.json. To do so, simply run 
AddPath.py and insert the path there. All the programs run based on this path. 

# Audio Data Recording

To obtain audio data for the wake word, please view the audio recording script ```Audio_Data_Recording.py```
To run this program, you must ensure that you have the following:

1. Python 3.x
2. Pyaudio (python -m pip install pyaudio)
3. Wave (pip install wave)

Also, modifications to the script need to be made. 

1. At line 19 of ```Audio_Data_Recording.py```, you must replace None with a string of YOUR last name. 
   Ex: Replace None with "ewenike"
  
2. If you are not using Windows, you must change the double backslashs in line 118 to single forward slashes.
   Ex: wf = wave.open("%s\\Data\\%s\\%s" % (PATH...... to wf = wave.open("%s/Data/%s/%s" % (PATH......
   
After these modifications, your program should run. Be sure to follow the spec description guidelines in the Data/WakeWord directory for correct labeling. 

# Train Model

Train_Model.py simply trains a model by obtaining the data within the Wake Word and Not Wake Word directories. Data will be converted to MFCCs using the Feature Extraction class and read into the WW Model class. The program will then either train a new model and retrain existing models.

If you would like to retrain existing models, simply make them arguments when running Train_Model.py with the ```-i```. 

```python Train_Model.py -i /Path/To/Model.h5```

If no ```-i``` argument is passed, the program will train a new model. 

The resulting model will be saved in Model/Wake Word/Models 

To train on a completely random set of train and test data, input the ```--rand``` argument.

```python Train_Model.py --rand```


# Awaken NIMBUS

Awaken NIMBUS will make predictions on real-time and output <<nimbus>> on consecutive positive activations ```-a```.

## Usage

This program requires that a pretrained model is input ```-i
```python False_Positives_Detection_Live.py -i /Path/To/Model.h5``` 

There are additional features for the user. If the user would like the know the prediction score of each prediction, such can be done ```-p```. To modify the number of predictions for an activation, simply use the ```-a``` argument.

```python False_Positives_Detection_Live.py -i /Path/To/Model. -p -a 10 ```


# False Positives Detection Live

False Positives Detection Live will make predictions on real-time audio and save any audio streams that cause activation. The purpose is to catch audio that causes false activation. The false positive audio will then be stored in the Not Wake Word directory of the Data directory. 

Caution: Ensure the wake word is NOT spoken during this time. Such will cause false negatives when training on not wake word data that is the actual wake word.

## Usage

This program requires that a pretrained model is input ```-i```. A location ```-l``` and a label description ```-d``` are also required to label the audio data. Once the desired number of false activations occur ```-n```(default = 4), the program will retrain a new model. Such is done by running the following:

```python False_Positives_Detection_Live.py -i /Path/To/Model.h5 -l Classroom -d serious-iss -n 7``` 

To train on a randomized set of train and test data, use the ```rand``` argument.

```python False_Positives_Detection_Live.py -i /Path/To/Model.h5 -l Classroom -d serious-iss --rand``` 

There are additional features for the user. The user can retrain on the same model ```-r```. If the user would like the know the prediction score of each prediction, such can be done ```-p```. To modify the number of predictions for an activation, simply use the ```-a``` argument. 

```python False_Positives_Detection_Live.py -i /Path/To/Model.h5 -l Classroom -d serious-iss -n 7 -p -a 10 -r```

# False Positives Detection File

This script take audio file(s) that presumably do not contain the wake word
("Nimbus"), perform prediction on every 2.432s frame with .128s strides, and
save the frame as a wav file if it's predicted to be the wake word. The output
wav files should then be used to train the model to be more robust against
false activation.

Prereqs: numpy, speechpy, keras (or tensorflow), pydub, and ffmpeg. You can
install ffmpeg with "brew install ffmpeg" if you have homebrew installed, or
download it from https://ffmpeg.org. Other prereqs are python libraries and can
be installed with "pip install library".

Usage:  python False_Positives_Detection_File.py model source target_dir [name]
Where:  model is a HDF5 dump of the model you're training on.
        source is an audio file or a directory (the script will recursively go
            through the tree and ignore non-audio files)
        target_dir is the directory where the false positive frames should be
            output.
        name (optional) is your name. You can modify the global NAME in the
            script to avoid having to type it.

Formats supported: raw, wav, mp3, and all other formats supported by FFmpeg
(https://en.wikipedia.org/wiki/FFmpeg)


# Nimbus Non-Wake Word Audio Scraping

Scraping sound content from project gutenburg audio books.

To run this script:
  1. Install pydub:   <pre>$pip3 install pydub</pre>      https://github.com/jiaaro/pydub.git

  2. Install ffmpeg:  <pre>$brew install ffmpeg</pre>    https://ffmpeg.org/documentation.html

  3. Select an audio book from project gutenburg:      https://www.gutenberg.org/browse/categories/1
  4. Grab the url for the "Audio Book Index" file
  5. Run the following command: <pre>$python3 scrape_gutenburg_audio.py <audio_book_index_file_link>...</pre>

  ## IMPORTANT
  - This data will be labeled as Non-Wake Word samples, so make sure to select an audiobook that does NOT contain the word "nimbus"
  - Before selecting an audiobook to use, make sure it has not already been downloaded by another team member.  Click the link below to see a list of already-selected audiobooks
  https://docs.google.com/spreadsheets/d/16qjEKGVPLV9DD26VwshZuQmmn-eqI_dHJBcDHU2mPTY/edit?usp=sharing

  ## SCRIPTS

  - If you wish to create your own script using pydub's AudioSegment library, make sure to set your AudioSegment instantiation to the spec-adjusted instantiation.  Then you can export with your desired output file specifications

  Example:
  ```python
  from pydub import AudioSegment

  sound = AudioSegment.from_mp3(mp3_file_name)
  sound = sound.set_frame_rate(RATE).set_channels(CHANNELS).set_sample_width(FORMAT)

  # rest of code...
  ```

# Nimbus Data Augmentation and Generator

This module provides 2 classes, AudioAugmenter and DataGenerator. The AudioAugmenter is a wrapper for raw audio bytes that provides methods for audio manipulation, currently supporting padding, changing pitch, adding random noise, and speeding up audio. DataGenerator is a generator-like object that can be fed into the train functions of TensorFlow; it should be initialized with
audio segments (or raw bytes) and randomly applies augmentation methods from AudioAugmenter to them.

Prereqs: Pydub and NumPy

