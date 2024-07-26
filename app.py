from flask import Flask, render_template, request, jsonify
import gesture_recorder  
import random
import serial  
import pandas as pd  # To read the CSV file
import tensorflow as tf  # For loading and running the Keras __model
from collections import Counter
import os
from tensorflow import keras
import pickle
from keras.models import load_model
import numpy as np
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
# from tensorflow.keras.layers import Bidirectional, LSTM, Dense
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.initializers import Orthogonal

# Define the custom layers used in your model
# custom_objects = {'Bidirectional': Bidirectional, 'LSTM': LSTM}
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

__model = None
__model1=None
__le = None
__modelsvm=None
__lesvm=None
__scaler = None
__modelLSTM = None

def loadModel(model_path):
    global __model
    global __le
    global __model1
    global __modelsvm
    global __lesvm
    global __scaler
    global __modelLSTM

    # custom_objects = {'Bidirectional': Bidirectional, 'LSTM': LSTM, 'Orthogonal': Orthogonal}

    if os.path.exists(model_path):

        # with open(model_path, "rb") as f:  
            # __model = tf.keras.models.load_model(r"C:\Users\Mahek Upadhye\Downloads\ipd-work (2)\ipd-work\ipd-work\ipd_model_2.h5",compile=False)
            #  __modelLSTM = keras.models.load_model(r"C:\Users\Mahek Upadhye\Downloads\ipd-work (2)\ipd-work\ipd-work\lstm.h5", compile=False)
            # __modelLSTM = load_model('lstm.h5', custom_objects=custom_objects)
            # __modelsvm = pickle.load(f)
        with open('svm.pkl','rb') as f:
            __modelsvm = pickle.load(f)
        print("Model loaded successfully.")
        with open('labelLSTM.pkl','rb') as f:
            __lesvm = pickle.load(f)
        with open('label_encoder2.pkl','rb') as f:
            __le = pickle.load(f)
        with open('scaler.pkl','rb') as f:
            __scaler = pickle.load(f)

        # with open(r'C:\Users\Mahek Upadhye\Downloads\ipd-work (2)\ipd-work\ipd-work\lstm.h5','rb') as f:
        #     __modelLSTM = load_model(f)
    else:
        print(f"Error: File not found at path '{model_path}'")

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/record_gesture', methods=['POST'])
# def record_gesture():
#     global __model
#     global __le
#     gesture_id = random.randint(1000, 9999)  # Generate a random gesture ID
#     gesture_data = []
    
#     try:
#         # Open the serial port
#         ser = serial.Serial('COM4', baudrate=115200, timeout=1)
#         gesture_data = gesture_recorder.log_gesture(5, ser)  # Record gesture for 5 seconds
#     except serial.SerialException as e:
#         # Handle errors if the serial port is unavailable
#         return jsonify(success=False, message=f"Error accessing COM4: {str(e)}"), 500
#     finally:
#         if 'ser' in locals():
#             ser.close()

#     # Save the recorded gesture data to a CSV file
#     gesture_recorder.save_gesture(gesture_id, gesture_data)

#     # Load the CSV file with pandas
#     df = pd.read_csv('gesture_data_test.csv')
#     y_pred2 = np.argmax(__model.predict(df), axis=-1)
#     y_string2 = __le.inverse_transform(y_pred2)
#     print("pred: ", y_string2)
    
#     # Return the prediction results
#     return jsonify(success=True, predictions=y_string2.tolist(), message="Gesture recorded and analyzed")


@app.route('/record_gesture', methods=['POST'])
def record_gesture():
    global __model
    global __model1
    global __le
    global __modelsvm
    global __lesvm
    global __scaler
    global __modelLSTM

    try:
        ser = serial.Serial('COM10', baudrate=115200, timeout=1)
        gesture_data = gesture_recorder.log_gesture(5, ser) 
        if not gesture_data:
            raise ValueError("No gesture data recorded")
        gesture_recorder.save_gesture(gesture_data)
        data = pd.read_csv('gesture_data_test.csv')
        if data.empty:
            raise ValueError("Data file is empty")
        
        #shreyas model
        # flattened_data = data.values.flatten()

        # new_column_names = [f"{col}{i+1}" for i in range(data.shape[0]) for col in data.columns]
        
        # transformed_data = pd.DataFrame([flattened_data], columns=new_column_names)
        # y_pred = np.argmax(__model.predict(transformed_data), axis=-1)
        # y_string = __le.inverse_transform(y_pred)

        #mahek's model
        # eg1 = __model1.predict(data)
        # egp1 = [int(np.argmax(element)) for element in eg1]  # Convert int64 to regular Python int
        # print("/n/n")
        # print(egp1)
        # egp1=list(egp1)
        # counter = Counter(egp1)
        # most_common_element = counter.most_common(1)[0][0]
        # count = counter[most_common_element]

        #aasmis model
        
        # scaler.fit(data)
        test_data_scaled = __scaler.transform(data)

# Predict probabilities for each class
        predicted_probabilities = __modelsvm.predict_proba(test_data_scaled)

        # Get the index of the maximum probability for each sample
        predicted_indices = predicted_probabilities.argmax(axis=1)

        # Map the indices to the corresponding gesture names
        predicted_gesture_names = __lesvm.inverse_transform(predicted_indices)

        # Print the predicted gesture names
        print("Predicted Gesture Names SVM:")
        print("----------------------")
        for gesture_name in predicted_gesture_names:
            print(gesture_name)
        print('--------------------------')

        
        #LSTM
        # test_df = pd.read_csv('gesture_data_test2.csv')

# Apply feature scaling to the test data
        # test_data_scaled = __scaler.transform(data)

        # # Reshape the test data to include timestep dimension
        # test_data_reshaped = test_data_scaled.reshape(test_data_scaled.shape[0], 1, test_data_scaled.shape[1])

        # # Make predictions on the test data
        # predictions = __modelLSTM.predict(test_data_reshaped)

        # # Decode predicted labels back to their original gesture names
        # predicted_labels = __lesvm.inverse_transform(np.argmax(predictions, axis=1))

        # # Print predicted gesture names
        # print("Predicted Gesture Names LSTM:")
        # for gesture_name in predicted_labels:
        #     print(gesture_name)

       
        # return jsonify(success=True, predictions=y_string.tolist(), message="Gesture recorded and analyzed")
        # return jsonify(success=True, predictions=egp1, message="Gesture recorded and analyzed")
        return jsonify(success=True, predictions=predicted_gesture_names.tolist(), message="Gesture recorded and analyzed")
        
    except Exception as e:
        app.logger.error(f"Failed to process the gesture: {str(e)}")

        return jsonify(success=False, message=f"Error processing data: {str(e)}"), 500
    finally:
        print("done")
        # if 'ser' in locals():
        #     ser.close()

if __name__ == '__main__':
    print("Server running....")
    model_path = os.path.abspath(r'C:\Users\Mahek Upadhye\Downloads\ipd-work (2)\ipd-work\ipd-work\ipd_model_initial.h5')
    loadModel(model_path)
    app.run()

