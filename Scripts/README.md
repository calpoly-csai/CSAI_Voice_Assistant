# Nimbus False Activation Detection

This script take audio file(s) that presumably do not contain the wake word
("Nimbus"), perform prediction on every 2.432s frame with .128s strides, and
save the frame as a wav file if it's predicted to be the wake word. The output
wav files should then be used to train the model to be more robust against
false activation.

Prereqs: numpy, speechpy, keras (or tensorflow), pydub, and ffmpeg. You can
install ffmpeg with "brew install ffmpeg" if you have homebrew installed, or
download it from https://ffmpeg.org. Other prereqs are python libraries and can
be installed with "pip install library".

Usage:  python false_pos_detect.py model source target_dir [name]
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
