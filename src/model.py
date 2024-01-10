from keras import regularizers
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from sklearn.model_selection import KFold
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.utils import plot_model
from scikeras.wrappers import KerasClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import RandomizedSearchCV

import json

import numpy as np
import sys
sys.path.append('src')
import multifasta_matrix


SEQ_LENGTH = 389
NB_CLASSES = 12

def get_train_and_test_data():
    """Gets the training and test data for the CNN model from the training.json and test.json files.
    To be used from the main directory of the project containing the src directory.
    
    Returns :
    train_x and test_x : One hot encoded sequences padded to have a height equal to SEQ_LENGTH
    train_y and test_y : Labels made of lists of classes padded to have a length equal to SEQ_LENGTH
    """
    #I used these files because I didn't figure out how to get the datas from the pdb files -Adelin
    with open("data/SPOT-RNA-1D/training.json") as training_file :
        training_file_data = json.load(training_file)

    dict_train = dict()
    for key, elem in training_file_data.items():
        dict_train[key] = {"sequence" : elem["sequence"], "theta" : elem["angles"]["theta"] }
    #print(dict_train)

    with open("data/SPOT-RNA-1D/test.json") as test_file :
        test_file_data = json.load(test_file)

    dict_test = dict()
    for key, elem in test_file_data.items():
        dict_test[key] = {"sequence" : elem["sequence"], "theta" : elem["angles"]["theta"] }
    #print(dict_test)

    list_seq_lengths = []
    for key in dict_train.keys() :
         list_seq_lengths.append(len(dict_train[key]["sequence"]))
    
    for key in dict_test.keys() :
         list_seq_lengths.append(len(dict_test[key]["sequence"]))
    
    seq_length = max(list_seq_lengths)
    #print(seq_length)

    assert seq_length == SEQ_LENGTH

    train_x = [multifasta_matrix.one_hot_encoding(dict_train[key]["sequence"]) for key in dict_train.keys()]
    #print(train_x)

    test_x = [multifasta_matrix.one_hot_encoding(dict_test[key]["sequence"]) for key in dict_test.keys()]
    #print(test_x)

    classes = [-180,-150,-120,-90,-60,-30,0,30,60,90,120,150,180]

    train_y = []
    for key in dict_train.keys():
        key_y_list = []
        for t in dict_train[key]["theta"]:
            for i in range (1,len(classes)):
                if (t <= classes[i] and t > classes[i-1]):
                        key_y_list.append(i)
                        #print(i,t)
        train_y.append(key_y_list)
    
    #print(train_y)

    test_y = []
    for key in dict_test.keys():
        key_y_list = []
        for t in dict_test[key]["theta"]:
            for i in range (1,len(classes)):
                if (t <= classes[i] and t > classes[i-1]):
                        key_y_list.append(i)
                        #print(i,t)
        test_y.append(key_y_list)
    
    #print(test_y)

    train_x_padded = []
    for l in train_x :
        train_x_padded.append( np.pad(l, [(0, SEQ_LENGTH-len(l)), (0, 0)], mode='constant', constant_values=0) )
    train_x_padded_array = np.array(train_x_padded)
         
    #print(train_x_padded_array)
    #print([len(l) for l in train_x_padded_array])

    test_x_padded = []
    for l in test_x :
        test_x_padded.append( np.pad(l, [(0, SEQ_LENGTH-len(l)), (0, 0)], mode='constant', constant_values=0) )
    test_x_padded_array = np.array(test_x_padded)

    #print(test_x_padded_array)
    #print([len(l) for l in test_x_padded_array])

    for l in train_y :
        while (len(l) != SEQ_LENGTH) :
             l.append(0)
    train_y_array = np.array(train_y)
    
    #print(train_y_array)
    #print([len(l) for l in train_y_array])


    for l in test_y :
        while (len(l) != SEQ_LENGTH) :
             l.append(0)
    test_y_array = np.array(test_y)
    
    #print(test_y_array)
    #print([len(l) for l in test_y_array])

    #To check visualy if there is missing data in the arrays
    #print(True in np.isnan(train_x_padded_array), True in np.isnan(train_y_array), True in np.isnan(test_x_padded_array), True in np.isnan(test_y_array))
    
    return train_x_padded_array, train_y_array, test_x_padded_array, test_y_array



def create_model(nb_canals = 32, filter_height = 3, filter_width = 4, pooling_height = 1, pooling_width = 4, nb_after_flatten = 100, padding_opt = "same", kernel_init_opt = "he_uniform", learning_rate_opt = 0.01, lambda_l1 = 0.01):
    """Creates the structure of the CNN model for the angle prediction.
    
    Parameters :
    nb_canals = 32 : Number of output canals for the 2D convolution layer
    filter_height = 3 : Height of the filter defined for the 2D convolution layer
    filter_width = 4 : Width of the filter defined for the 2D convolution layer
    pooling_height = 1 : Height of the pooling window for the pooling layer
    pooling_width = 4 : Width of the pooling window for the pooling layer
    nb_after_flatten = 100 : Number of neurons for the dense layer after the flatten layer
    padding_opt = "same" : Padding option for the 2D convolution layer
    kernel_init_opt = "he_uniform" : Kernel initialization option for the 2D convolution layer
    learning_rate_opt = 0.01 : Learning rate option for the optimizer
    lambda_l1 = 0.01 : Option for the l1 regularizer

    Returns :
    model
    """

    #Creates the model
    model = Sequential()
    
    #Adds a 2D convolution layer to the model
    model.add(Conv2D(nb_canals, (filter_height, filter_width), activation='relu', padding= padding_opt, kernel_initializer= kernel_init_opt, input_shape=(SEQ_LENGTH, 4, 1)))
    
    #Adds a pooling layers to the model
    model.add(MaxPooling2D((pooling_height, pooling_width)))
    
    #Adds a flattening layer to the model
    model.add(Flatten())

    #Adds a dense layer to the model
    model.add(Dense(nb_after_flatten, activation='relu', kernel_initializer=kernel_init_opt, kernel_regularizer=regularizers.l1(lambda_l1)))

    # Add output layer for multi-class predictions
    model.add(Dense(SEQ_LENGTH, activation='sigmoid'))

	# compile model
    opt = SGD(learning_rate= learning_rate_opt, momentum=0.9)
    model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])
    model.summary()

    return model


def fit_model(train_x, train_y, test_x, test_y, dict_params_model = dict()): 
        
	# define model
    model = create_model(**dict_params_model)

	# fit model
    history = model.fit(train_x, train_y, epochs=500, batch_size=32, validation_data=(test_x, test_y), verbose=1)

	# evaluate model
    acc = model.evaluate(test_x, test_y, verbose=1)

    print(history)
    print(acc)

    return model



def RandomizedSearch(train_x, train_y, test_x, test_y, verbose = 0):
    """Function performing a randomized search to tune the hyperparameters

    """

    print(train_y.shape)
    print(train_x.shape)

    print(train_y)
    print(train_x)

	#Dictionnary containing the hyperparameters needing to be tuned
    param_search = {
    "nb_canals" : [32, 64, 128],
    "filter_height" : [2,3,4],
    "filter_width" : [2,3,4],
    "pooling_height" : [1,2,3],
    "pooling_width" : [2,3,4],
    "nb_after_flatten" : [10,50,100],
    "padding_opt" : ["same","valid"],
    "kernel_init_opt" : ["he_uniform", "he_normal"],
    "learning_rate_opt" : [0.1,0.05,0.01],
	"lambda_l1" : [0.001,0.01,0.1]
	}


    model_search = KerasClassifier(build_fn=create_model, verbose=1,nb_canals = 32, filter_height = 3, filter_width = 4, pooling_height = 1, pooling_width = 4, nb_after_flatten = 100, padding_opt = "same", kernel_init_opt = "he_uniform", learning_rate_opt = 0.01, lambda_l1 = 0.01)

    kfold = StratifiedKFold(n_splits=5, shuffle=True)

    random_search = RandomizedSearchCV(model_search, param_search, cv=kfold, n_iter=100, random_state = 42)

	# Fit the randomized search to the data
    random_result = random_search.fit(train_x, train_y, epochs=100, batch_size=32, validation_data=(test_x, test_y), verbose=1)

	# Print the best parameters and the corresponding accuracy
    if verbose == 1 :
        print("Best Parameters:", random_result.best_params_)
        print("Best Accuracy:", random_result.best_score_)

    return random_result.best_params_

#def predict_angles(inputs):
#    outputs
#    return outputs

if __name__ == "__main__" :
    train_x, train_y, test_x, test_y = get_train_and_test_data()
    #RandomizedSearchCV doesn't work with multioutput classifiers.
    #Error : Supported target types are: ('binary', 'multiclass'). Got 'multiclass-multioutput' instead.
    #dict_params_random = RandomizedSearch(train_x, train_y, test_x, test_y, verbose = 1)
    model = fit_model(train_x, train_y, test_x, test_y) #, dict_params_random

    print(model.predict(test_x[:1]))
