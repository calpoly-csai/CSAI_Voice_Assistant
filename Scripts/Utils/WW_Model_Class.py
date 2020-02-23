"""
Title: Wake Word Model
Author: Chidi Ewenike
Date: 08/09/2019
Organization: Cal Poly CSAI
Description: The class for the model architecture and training

"""
import json
import os
import random

import numpy as np
import tensorflow as tf

from datetime import datetime
from tensorflow.keras import layers, models
from Utils.OS_Find import Path_OS_Assist


class Model:

    def __init__(self):
        """
        Constructor for the Model class

        Args:
            self - The current object

        Returns:
            None

        """

        self.delim = Path_OS_Assist()

        with open(os.getcwd() + "%sUtils%sPATH.json" %
                  (self.delim, self.delim), "r") as path_json:
            self.REPO_PATH = json.load(path_json)["PATH"]

        self.JSON_PATH = self.REPO_PATH + "%sData%sWakeWord%sMFCC%s" % \
            (self.delim, self.delim, self.delim, self.delim)

        # name of json data files
        self.WW_TRAIN = "Wake_Word_Train_Data.json"
        self.NWW_TRAIN = "Not_Wake_Word_Train_Data.json"
        self.WW_TEST = "Wake_Word_Test_Data.json"
        self.NWW_TEST = "Not_Wake_Word_Test_Data.json"
        self.WW_DATA = "ww_data.json"
        self.NWW_DATA = "nww_data.json"

        self.CONFIDENCE = 0.6  # prediction confidence
        self.GRU_UNITS = 64  # GRU unit size
        self.DROPOUT = 0.3  # dropout size
        self.ACTIVATIONS = 4  # number of activations for confident activation
        self.EPOCHS = 20  # number of fwd and bckwd props
        self.BATCH_SIZE = 8  # batch size

        self.ww_test_data = {}
        self.ww_test_data_keys = []
        self.ww_train_data = {}
        self.ww_train_data_keys = []

        # not wake word train & test data with shuffled list of keys
        self.nww_test_data = {}
        self.nww_test_data_keys = []
        self.nww_train_data = {}
        self.nww_train_data_keys = []

        self.ww_data = {}
        self.ww_data_keys = []
        self.ww_data = {}
        self.ww_data_keys = []

        # not wake word train & test data with shuffled list of keys
        self.nww_data = {}
        self.nww_data_keys = []
        self.nww_data = {}
        self.nww_data_keys = []

        # input list of training & test data and labels
        self.train_data = []
        self.train_labels = []
        self.test_data = []
        self.test_labels = []

    def build_model(self):
        """
        Constructs the model architecture for training

        Args:
            self - The current object

        Returns:
            None

        """

        # define a model as a sequence of layers
        self.model = models.Sequential()

        # 8 dense, feed-forward layers, 16 neurons each
        self.model.add(layers.Dense(units=16,
                                    activation='relu',
                                    input_shape=(36, 13)))
        self.model.add(layers.Dense(units=16, activation='relu'))
        self.model.add(layers.Dense(units=16, activation='relu'))
        self.model.add(layers.Dense(units=16, activation='relu'))
        self.model.add(layers.Dense(units=16, activation='relu'))
        self.model.add(layers.Dense(units=16, activation='relu'))
        self.model.add(layers.Dense(units=16, activation='relu'))
        self.model.add(layers.Dense(units=16, activation='relu'))

        # GRU with desired number of neurons on the
        # output layer of each NN in the GRU
        self.model.add(layers.GRU(self.GRU_UNITS, dropout=self.DROPOUT))

        # Dense-connected output for binary classification
        self.model.add(layers.Dense(1, activation='sigmoid'))

        # define loss and optimzer fns
        self.model.compile(optimizer='adam',
                           loss='binary_crossentropy',
                           metrics=['acc'])

    def randomized_preprocess(self):
        """
        Preprocesses the MFCCs and labels corresponding
        audio with WW/NWW labels

        Args:
            self - The current object

        Returns:
            None

        """

        # open the JSON from the path containing the data JSON
        with open(os.path.join(self.JSON_PATH, self.WW_DATA)) as f_in:

            # load the data from the json into a dict
            self.ww_data = json.load(f_in)

            # obtain list of keys
            self.ww_data_keys = list(self.ww_data.keys())

            # shuffle the list
            random.shuffle(self.ww_data_keys)

        # open the JSON from the path containing the data JSON
        with open(os.path.join(self.JSON_PATH, self.NWW_DATA)) as f_in:

            # load the data from the json into a dict
            self.nww_data = json.load(f_in)

            # obtain list of keys
            self.nww_data_keys = list(self.nww_data.keys())

            # shuffle the list
            random.shuffle(self.nww_data_keys)

        # iterate through the list of ww train keys
        for i in range(int(len(self.ww_data_keys)*0.8)):

            # hash into the dict and store it in the input list
            self.train_data.append(self.ww_data[
                self.ww_data_keys[i]])

            # label the corresponding data
            self.train_labels.append(1)

        # iterate through the list of nww train keys
        for i in range(int(len(self.nww_data_keys)*0.8)):

            # hash into the dict and store it in the input list
            self.train_data.append(self.nww_data[
                self.nww_data_keys[i]])

            # label the corresponding data
            self.train_labels.append(0)

        # iterate through the list of ww test keys
        for i in range(int(len(self.ww_data_keys)*0.8),
                       len(self.ww_data_keys)):

            # hash into the dict and store it in the input list
            self.test_data.append(self.ww_data[self.ww_data_keys[i]])

            # label the corresponding data
            self.test_labels.append(1)

        # iterate through the list of nww test keys
        for i in range(int(len(self.nww_data_keys)*0.8),
                       len(self.nww_data_keys)):

            # hash into the dict and store it in the input list
            self.test_data.append(self.nww_data[
                self.nww_data_keys[i]])

            # label the corresponding data
            self.test_labels.append(0)

        # convert the data lists to np arrays of type float
        self.test_data = np.array(self.test_data, dtype=float)
        self.train_data = np.array(self.train_data, dtype=float)
        self.test_labels = np.array(self.test_labels, dtype=float)
        self.train_labels = np.array(self.train_labels, dtype=float)

    def preprocess(self):
        """
        Preprocesses the MFCCs and labels corresponding
        audio with WW/NWW labels

        Args:
            self - The current object

        Returns:
            None

        """

        # open the JSON from the path containing the data JSON
        with open(os.path.join(self.JSON_PATH, self.WW_TRAIN)) as f_in:

            # load the data from the json into a dict
            self.ww_train_data = json.load(f_in)

            # obtain list of keys
            self.ww_train_data_keys = list(self.ww_train_data.keys())

            # shuffle the list
            random.shuffle(self.ww_train_data_keys)

        # open the JSON from the path containing the data JSON
        with open(os.path.join(self.JSON_PATH, self.NWW_TRAIN)) as f_in:

            # load the data from the json into a dict
            self.nww_train_data = json.load(f_in)

            # obtain list of keys
            self.nww_train_data_keys = list(self.nww_train_data.keys())

            # shuffle the list
            random.shuffle(self.nww_train_data_keys)

        # open the JSON from the path containing the data JSON
        with open(os.path.join(self.JSON_PATH, self.WW_TEST)) as f_in:

            # load the data from the json into a dict
            self.ww_test_data = json.load(f_in)

            # obtain list of keys
            self.ww_test_data_keys = list(self.ww_test_data.keys())

            # shuffle the list
            random.shuffle(self.ww_test_data_keys)

        # open the JSON from the path containing the data JSON
        with open(os.path.join(self.JSON_PATH, self.NWW_TEST)) as f_in:

            # load the data from the json into a dict
            self.nww_test_data = json.load(f_in)

            # obtain list of keys
            self.nww_test_data_keys = list(self.nww_test_data.keys())

            # shuffle the list
            random.shuffle(self.nww_test_data_keys)

        # iterate through the list of ww train keys
        for i in range(len(self.ww_train_data_keys)):

            # hash into the dict and store it in the input list
            self.train_data.append(self.ww_train_data[
                self.ww_train_data_keys[i]])

            # label the corresponding data
            self.train_labels.append(1)

        # iterate through the list of nww train keys
        for i in range(len(self.nww_train_data_keys)):

            # hash into the dict and store it in the input list
            self.train_data.append(self.nww_train_data[
                self.nww_train_data_keys[i]])

            # label the corresponding data
            self.train_labels.append(0)

        # iterate through the list of ww test keys
        for i in range(len(self.ww_test_data_keys)):

            # hash into the dict and store it in the input list
            self.test_data.append(self.ww_test_data[self.ww_test_data_keys[i]])

            # label the corresponding data
            self.test_labels.append(1)

        # iterate through the list of nww test keys
        for i in range(len(self.nww_test_data_keys)):

            # hash into the dict and store it in the input list
            self.test_data.append(self.nww_test_data[
                self.nww_test_data_keys[i]])

            # label the corresponding data
            self.test_labels.append(0)

        # convert the data lists to np arrays of type float
        self.test_data = np.array(self.test_data, dtype=float)
        self.train_data = np.array(self.train_data, dtype=float)
        self.test_labels = np.array(self.test_labels, dtype=float)
        self.train_labels = np.array(self.train_labels, dtype=float)

    def train_model(self):
        """
        Initiates the training sequence for the model

        Args:
            self - The current object

        Returns:
            None

        """

        self.history = self.model.fit(self.train_data, self.train_labels,
                                      epochs=self.EPOCHS,
                                      batch_size=self.BATCH_SIZE, verbose=1,
                                      validation_data=(self.test_data,
                                                       self.test_labels))
        print(self.model.evaluate(self.test_data, self.test_labels))

        accuracy = int(((self.history.history['acc'])[self.EPOCHS-1])*100)

        model_name = "%s%sModel%sWake Word%sModels%sww_" \
            "model_%s_%s.h5" % (self.REPO_PATH, self.delim, self.delim,
                                self.delim, self.delim,
                                datetime.now().strftime("%m%d%Y%H%M%S_"),
                                str(accuracy))

        self.model.save(model_name)
        print("%s has been saved." % model_name)

    def load(self, model_name):
        """
        Constructor for the Model class

        Args:
            self - The current object
            model_name (str) - Name of the model file to load
        Returns:
            None

        """
        self.model = models.load_model(model_name)
