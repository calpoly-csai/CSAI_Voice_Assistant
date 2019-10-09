import re
import requests
import sys
import os

from Gutenburg_Wav_Util import mp3_to_wav, split_wav

SOUND_LENGTH = 2.5      # length of each sound split

# check for correct number of arguments
if len(sys.argv) < 2:
    print('Usage: scrape_gutenburg_audio.py <audio_book_index_file_link>...')
    sys.exit(0)

# apropriate regexps for common gutenburg html forms
regexps = [r'<li><a href="mp3-16bit\/(\d+)-(\d+)\.mp3">.*\.mp3<\/a>',
            r'<li><a href="mp3-32bit\/(\d+)-(\d+)\.mp3">.*\.mp3<\/a>',
            r'<li><a href="mp3\/(\d+)-(\d+)\.mp3">.*\.mp3<\/a>']

# apropriate mp3 link string frames for common gutenburg html forms
mp3_link_frames = ["https://www.gutenberg.org/files/{}/mp3-16bit/{}-{}.mp3",
                    "https://www.gutenberg.org/files/{}/mp3-32bit/{}-{}.mp3",
                    "https://www.gutenberg.org/files/{}/mp3/{}-{}.mp3"]

# process each link user provides
for i in range(1, len(sys.argv)):
    link = sys.argv[i]

    # send web request, get content
    r = requests.get(link)
    if r.status_code != 200: # error response -> output code, skip to next link
        print('error {} in web response... skipping link'.format(r.status_code))
        continue
    # decode to ascii to run regex queries on
    content = r.content.decode('utf-8')

    # scrape html to get mp3 file info
    file_info = mp3_link_frame = None
    for j in range(len(regexps)):
        file_info = re.findall(regexps[j], content)
        # check if this file regex matched
        if len(file_info) > 0:
            mp3_link_frame = mp3_link_frames[j]
            break

    # check for unrecognized html format
    if mp3_link_frame == None:
        print('unrecognized html format found... skipping link')
        continue

    # file information found, downloading can begin
    # prompt user for book name to serve as file directory
    dir = input("book name: ").lower().replace(" ", "_")

    # make directory if it doesnt already exist
    if not os.path.isdir(dir):
        os.mkdir("./{}".format(dir))

    # get file id
    file_index = file_info[0][0]
    file_section_index = 1

    # begin downloading
    print("downloading from {}".format(link))
    for j in range(len(file_info)):
        # get section id
        section_id = file_info[j][1]

        # open file for writing mp3 to
        mp3_file_name = "tmp.mp3"
        mp3_out = open(mp3_file_name, 'wb+')

        # format download link
        download_link = mp3_link_frame.format(file_index, file_index, section_id)

        # send web request, get content
        mp3_response = requests.get(download_link)
        if mp3_response.status_code != 200:
            # error response given, print code and skip to next link
            print('error {} in mp3 response... skipping file'.format(mp3_response.status_code))
            continue

        # save mp3 file
        mp3_out.write(mp3_response.content)
        mp3_out.close()

        # get file name and prefix for splits
        wav_file_name = "{}_{}.wav".format(file_index, file_section_index)
        wav_split_prefix = "./{}/section_{:02d}".format(dir, file_section_index)

        # export mp3 file to a wav file
        mp3_to_wav(mp3_file_name, wav_file_name)

        # split wav files into multiple segments of length = SOUND_LENGTH
        split_wav(SOUND_LENGTH, wav_file_name, wav_split_prefix)

        # remove temporary files
        os.remove(wav_file_name)
        os.remove(mp3_file_name)
        file_section_index += 1

    # print output
    print('wav splits saved to directory: {}'.format(dir))
