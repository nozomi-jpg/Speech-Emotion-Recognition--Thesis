import numpy as np
from pydub import AudioSegment
import noisereduce as nr

class preprocessor:
    def __init__(self, AUDIO_PATH, OUTPUT_FOLDER, FILE_NAME):
        self.audio_path = AUDIO_PATH    
        self.output_folder = OUTPUT_FOLDER   
        self.file_name = FILE_NAME   
    
    #REDUCE NOISE AND ADJUST LOUDNESS
    def process_audio(self):
        audio = AudioSegment.from_file(self.audio_path)  #Load the audio file
        samples = np.array(audio.get_array_of_samples()) #Convert audio to numpy array
        reduced_noise = nr.reduce_noise(samples, sr=audio.frame_rate) #Reduce noise

        #Convert reduced noise signal back to audio
        cleaned_audio = AudioSegment(
            reduced_noise.tobytes(), 
            frame_rate=audio.frame_rate, 
            sample_width=audio.sample_width, 
            channels=audio.channels
        )

        #Adjust Loudness
        target_dBFS = -20.0
        change_in_dBFS = target_dBFS - cleaned_audio.dBFS
        normalized_sound = cleaned_audio.apply_gain(change_in_dBFS)
        normalized_sound.export(self.output_folder + "/cleaned_" + self.file_name + ".wav", format="wav")