"""
Title: Train Model
Author: Chidi Ewenike
Date: 08/09/2019
Organization: Cal Poly CSAI
Description: Trains the current wake word model on either new data
             or an existing model

"""
import argparse
import sys
import tensorflow

from tensorflow import keras
from Utils.Feature_Extraction_Class import Feature_Extraction
from Utils.WW_Model_Class import Model

parser = argparse.ArgumentParser()
parser.add_argument('-i',
                    action="store",
                    required=False,
                    help="Input Model to Detect False Activations")
parser.add_argument('--rand',
                    action="store_true",
                    required=False,
                    help="Randomize training and test data")

args = parser.parse_args()


def main():
    # Trains a model using the ww_model.py class

    # Instantiate Model class
    ww_model = Model()

    # Perform feature extraction on current data
    ext_feat = Feature_Extraction()

    if not(args.rand):
        ww_model.preprocess()

    else:
        ww_model.randomized_preprocess()

    ext_feat.Obtain_WW_Audio_Data()

    # Trains a new model if no model files are passed as args
    if (args.i is None):

        ww_model.build_model()
        ww_model.train_model()

    # Trains all models in args on new data
    else:

        try:
            ww_model.load(args.i)
            ww_model.train_model()

        # Ignore all non-.h5 args
        except OSError:
            print("%s does not exist and will be ignored" % model)

        # Print out the summary of the model
        print(ww_model.model.summary())


if __name__ == "__main__":
    main()
