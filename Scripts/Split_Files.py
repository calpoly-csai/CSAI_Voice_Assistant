"""
Title: Split Files
Author: Sai Swaroop Pamidi
Date: 02/02/2020
Organization: Cal Poly CSAI
Description: split audio files into test and train data
Need to delete the Train_Data and Test_Data in both Wake_Word
and Not_Wake_Word first time to run this script. This is
to set a soft permission to the files.
"""
import argparse
import json
import os
import random
import shutil
import sys

from Utils.OS_Find import Path_OS_Assist
''' splits your audiofiles in notWakeWord and WakeWord '''
''' input path to your downloaded audio file folder, input -p1 WakeWord or -p2
    NotWakeWord and  -s split%'''


def parser():
    isNotWakeWord = False
    isWakeWord = False
    parser = argparse.ArgumentParser()
    parser.add_argument('-s',
                        required=True,
                        help="split % for the training set", type=float)
    parser.add_argument('-p1',
                        required=False,
                        help="path for the wake word audiofiles", type=str)
    parser.add_argument('-p2',
                        required=False,
                        help="path for not wake word audiofiles", type=str)

    args = parser.parse_args()
    if not(0 < args.s < 1):
        print("splitFiles.py: error: argument -s: invalid "
              "float value: ", args.s)
        print("split % has to strictly between 0 and 1")
        exit()
    if len(sys.argv) > 3:
        if '-p1' in sys.argv:
            isWakeWord = True
        if '-p2' in sys.argv:
            isNotWakeWord = True
    else:
        print("usage: splitFiles.py: required to use -p1 or -p2 ")
        exit()

    return args, isWakeWord, isNotWakeWord


def clearFolder(path):
    files = os.listdir(path)
    for i in files:
        os.remove(os.path.join(path, i))


def split(args, path, p):
    AudioFiles = os.listdir(p)
    if '.DS_Store' in AudioFiles:
        AudioFiles.remove('.DS_Store')
    folderList = os.listdir(path)
    if "Test_Data" not in folderList:
        os.mkdir(os.path.join(path, "Train_Data"), 0o777)
    else:
        clearFolder(os.path.join(path, "Train_Data"))

    if "Train_Data" not in folderList:
        os.mkdir(os.path.join(path, "Test_Data"), 0o777)
    else:
        clearFolder(os.path.join(path, "Test_Data"))
    for i in AudioFiles:
        val = random.randint(1, 100)
        if val <= (args.s * 100):
            oldPath = os.path.join(p, i)
            newPath = os.path.join(path, "Train_Data", i)
            shutil.copy(oldPath, newPath)
        else:
            oldPath = os.path.join(p, i)
            newPath = os.path.join(path, "Test_Data", i)
            shutil.copy(oldPath, newPath)


def main():
    parseVal = parser()
    args = parseVal[0]
    isWakeWord = parseVal[1]
    isNotWakeWord = parseVal[2]
    delim = Path_OS_Assist()
    with open(os.getcwd() + "%sUtils%sPATH.json" %
              (delim, delim), "r") as path_json:
        REPO_PATH = json.load(path_json)["PATH"]
    if isWakeWord:
        path = os.path.join(REPO_PATH, "Data", "WakeWord",
                            "Audio", "Wake_Word")
        split(args, path, args.p1)
    if isNotWakeWord:
        path = os.path.join(REPO_PATH, "Data", "WakeWord",
                            "Audio", "Not_Wake_Word")
        split(args, path, args.p2)


if __name__ == "__main__":
    main()
