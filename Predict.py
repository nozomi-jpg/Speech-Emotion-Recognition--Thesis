import os
import pickle
from statistics import mode
from Preprocessing import preprocessor
from Feature_extractor import feature_extractor
from sklearn import svm
import joblib
import numpy as np

class ModelPredictor:

    def __init__(self, audio_path):
        self.audio_path = audio_path

    def predict(self):
        cleaned_audio_folder = ".\\cleaned_audios" #Name of the folder for cleaned audios

        #Create new folder for cleaned audios if it doesn't exist
        if not os.path.exists(cleaned_audio_folder):
            os.makedirs(cleaned_audio_folder)

        #For Preprocessing Audio Files
        file_name = (os.path.basename(self.audio_path)).split(".")[0]
        process = preprocessor(self.audio_path, cleaned_audio_folder, file_name)
        process.process_audio()
        
        audio_path = os.path.join(cleaned_audio_folder, f'cleaned_{file_name}.wav')
        # Default frame length and hop length in Librosa; can stil be changed
        frame_length = 2048
        hop_length = 512

        extractor = feature_extractor(audio_path, frame_length, hop_length)
        features = extractor.extract_all_features()
        print(features)
        #Remove features based from PI result
        features = np.delete(features, [0,1,21,24,27,28,30,32,33,38,39,40,41,42,43,44,45,46]) 
        print(features)
        # Predict Emotion
        # load the model from disk
        models = joblib.load('model.pkl')
        
        prediction = []
        i=0

        while i < len(models):
            pred = models[i].predict([features])
            prediction.append(pred)
            i=i+1

        prediction = np.ravel(prediction)
        finalPrediction = mode(prediction)

        if finalPrediction == 0:
            emotion = 'Happy'
        elif finalPrediction == 1:
            emotion = 'Sad' 
        elif finalPrediction == 2:
            emotion = 'Neutral' 
        elif finalPrediction == 3:
            emotion = 'Angry'  
        
        return emotion