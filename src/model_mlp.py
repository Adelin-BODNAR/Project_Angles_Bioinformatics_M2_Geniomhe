import pandas as pd
import numpy as np
from keras import regularizers
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import mean_absolute_error
import json
import os 
import sys

def load_data(csv_file):
    """
    Charger les matrices one-hot encodées depuis le fichier CSV
    """
    data_matrix = pd.read_csv(csv_file)
    return data_matrix

def load_labels(labels_file):
    """
    Charger les étiquettes le label en excluant la première ligne.
    """
    labels = pd.read_csv(labels_file, header=None, names=['label'], skiprows=1)
    return labels['label']

def build_model(input_shape, output_dim):
    """
    Construire le modèle MLP.
    """
    model = Sequential()
    model.add(Dense(30, input_dim=input_shape, activation='relu', kernel_regularizer=regularizers.l1(0.01)))
    model.add(Dense(20, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
    model.add(Dropout(0.1))
    model.add(Dense(20, activation='relu', kernel_regularizer=regularizers.l1(0.01)))
    model.add(Dropout(0.2))
    model.add(Dense(20, activation='relu', kernel_regularizer=regularizers.l1(0.01)))
    model.add(Dropout(0.2))
    model.add(Dense(output_dim, activation='softmax', kernel_regularizer=regularizers.l1(0.01)))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model

def main():
    # fichier CSV contenant les matrices one-hot encodées pour l'entraînement
    train_csv_file = sys.argv[1]
    # Charger les matrices one-hot encodées pour l'entraînement
    train_data_matrix = load_data(train_csv_file)
    # Charger les labels pour l'entraînement
    train_labels_file = sys.argv[2]
    train_labels = load_labels(train_labels_file)

    # Séparer les caractéristiques (matrices one-hot encoded) pour l'entraînement
    X_train = train_data_matrix.drop(['A', 'U', 'G', 'C'], axis=1)
    # Charger les labels pour l'entraînement
    y_train = train_labels
    # Converting Labels to Categories
    y_train = to_categorical(y_train)

    # Resizing data
    X_train = X_train.astype('float32')

    # Construire le modèle pour l'entraînement
    model = build_model(X_train.shape[1], y_train.shape[1])

    # Entraîner le modèle
    es = EarlyStopping(monitor='val_acc', mode='max', verbose=1, patience=30)
    history = model.fit(X_train, y_train, validation_split=0.2, epochs=500, batch_size=250, callbacks=[es], verbose=1)

    # Sauvegarder le modèle
    model.save('modele.h5')

   
    # fichier content les matrices one-hot encodées pour le test
    test_csv_file = sys.argv[3]
    # Charger les matrices one-hot encodées pour le test
    test_data_matrix = load_data(test_csv_file)
    # Charger les étiquettes (classes) pour le test
    test_labels_file = sys.argv[4]
    test_labels = load_labels(test_labels_file)

    # Séparer les caractéristiques (matrices one-hot encoded) pour le test
    X_test = test_data_matrix.drop(['A', 'U', 'G', 'C'], axis=1)
    # Charger les étiquettes (classes) pour le test
    y_test = test_labels
    # Converting Labels to Categories
    y_test = to_categorical(y_test)

    # Resizing data
    X_test = X_test.astype('float32')

    # Évaluer le modèle sur le jeu de test
    score = model.evaluate(X_test, y_test, batch_size=250, verbose=1)
    print("Scores on the test set: loss=%s accuracy=%s" % tuple(score))

    # Calculer et imprimer le MAE
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(np.argmax(y_test, axis=1), np.argmax(y_pred, axis=1))
    print("Mean Absolute Error:", mae)

    # Predictions on the test set
    predictions = model.predict(X_test)

    # Convert predictions to class labels
    predicted_labels = np.argmax(predictions, axis=1)

    # Create a dictionary for saving to JSON
    result_dict = {'true_labels': y_test.tolist(), 'predicted_labels': predicted_labels.tolist()}

    # Save predictions to a JSON file
    output_json_file = 'predictions.json'
    with open(output_json_file, 'w') as json_file:
        json.dump(result_dict, json_file)

    # Calculate and print the MAE
    mae = mean_absolute_error(y_test, predicted_labels)
    print("Mean Absolute Error:", mae)

if __name__ == "__main__":
    main()
