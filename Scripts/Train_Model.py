"""
Title: Train Model
Author: Chidi Ewenike
Date: 08/09/2019
Organization: Cal Poly CSAI
Description: Trains the current wake word model on either new data
             or an existing model

"""
from Utils.WW_Model_Class import Model
import tensorflow
from tensorflow import keras
import sys
from Utils.Feature_Extraction_Class import Feature_Extraction


def main():
    """
    Trains a using the ww_model.py class

    Args:
        None

    Returns:
        None

    """

    # Instantiate Model class
    ww_model = Model()

    # Perform feature extraction on current data
    ext_feat = Feature_Extraction()

    # Trains a new model if no model files are passed as args
    if (len(sys.argv) == 1):

        ext_feat.Obtain_WW_Audio_Data()
        ww_model.build_model()
        ww_model.preprocess()
        ww_model.train_model()

    # Trains all models in args on new data
    else:

        for model in sys.argv[1:]:
            ext_feat.Obtain_WW_Audio_Data()

            try:
                ww_model.load(model)
                ww_model.train_model()

            # Ignore all non-.h5 args
            except OSError:
                print("%s does not exist and will be ignored" % model)

            # Print out the summary of the model
            print(ww_model.model.summary())


if __name__ == "__main__":
    main()
