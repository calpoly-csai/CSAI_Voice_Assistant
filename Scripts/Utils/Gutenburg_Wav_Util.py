from pydub import AudioSegment

FORMAT = 2      # '2' corresponds to 16-bit format in pydub's set_sample_width
CHANNELS = 1    # mono
RATE = 16000    # sample rate


def mp3_to_wav(mp3_file_name, wav_file_name):
    """Converts mp3 files to wav files.

    Takes an input mp3 file name and and output wav file name.
    This function assumes the pydub and ffmpeg libraries have been installed.
    This function assumes the constants FORMAT, CHANNELS, and RATE have been
    set at the top of this file.
    """
    sound = AudioSegment.from_mp3(mp3_file_name)
    sound = sound.set_frame_rate(RATE).set_channels(CHANNELS).set_sample_width(FORMAT)
    sound.export(wav_file_name, format="wav")


def split_wav(sound_length, wav_file_name, wav_split_prefix):
    """Splits wav files into files of given length.

    Takes a length of time, input wav file name, and a file name prefix.
    This function assumes the pydub and ffmpeg libraries have been installed.
    This function does not make changes to wav file format.
    Up to 'sound_length' seconds of data can be excluded from split files based
    on file overflow length.
    """
    split_index = 0
    t1 = 0
    t2 =  sound_length * 1000   # indexed in milliseconds, multiply by 1000
    sound = AudioSegment.from_wav(wav_file_name)

    # keep adding splits of file until the end is reached
    while t2 < len(sound):
        split = sound[t1:t2]
        split.export("{}_split_{}.wav".format(wav_split_prefix, split_index), format="wav")

        # shift split times forward by sound_length
        t1 += sound_length * 1000
        t2 += sound_length * 1000
        split_index += 1
