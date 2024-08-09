import tkinter as tk
import customtkinter as ctk
from pydub import AudioSegment
from pydub.playback import play
from PIL import Image
import threading
import time
import pyaudio
import wave
import os 
from EmotionDetector import EmotionDetector
from Predict import ModelPredictor


class AudioPlayer:
    def __init__(self, audio_path):
        self.window = ctk.CTkToplevel()
        width = int(self.window.winfo_screenwidth()/2 - (708/2))
        height = int(self.window.winfo_screenheight()/2 - (512/2))
        self.window.geometry(f"708x512+{width}+{height}")
        self.window.title("Audio Player")
        self.window.resizable(False, False)

        #back Button
        self.menu_btn = ctk.CTkButton(self.window, text="<", command=self.handleBack)
        self.menu_btn.configure(width=15, height=30, corner_radius=8,fg_color="#F6867A", hover_color="#EB7B70", font=('Inter',20), text_color="#FFFFFF" )
        self.menu_btn.place(x=70, y=30)
        #FILE NAME
        self.filename_lbl = ctk.CTkLabel(self.window, text=f"Filename: {os.path.basename(audio_path)}")
        self.filename_lbl.configure(fg_color="transparent",
                        font=('Inter', 16),
                        text_color="#23295A")

        self.filename_lbl.place(x=125, y=35)



        #player frame
        self.player_frame = ctk.CTkFrame(self.window, width=571, height=367,corner_radius=20)
        self.player_frame.configure(fg_color="#2A295C")
        self.player_frame.place( relx=0.5, rely=0.5, anchor = tk.CENTER)
        self.PATH = audio_path

        #timer frame
        self.timer_frame = ctk.CTkFrame(self.player_frame, width=531, height=220,corner_radius=8)
        self.timer_frame.configure(fg_color="#FFFFFF")
        self.timer_frame.place(x=20 ,y=47)

        #timer counter
        self.time_lbl = ctk.CTkLabel(self.timer_frame, text="00:00:00")
        self.time_lbl.configure(fg_color="transparent",
                        font=('Inter', 26),
                        text_color="#23295A")

        self.time_lbl.place(relx=0.5, y=65,anchor = tk.CENTER)

        #LINE (di ko magawa yung may circle na gumagalaw)
        self.canvas = tk.Canvas(self.timer_frame, width=400, height=5, highlightthickness=0)
        self.canvas.place(relx=0.5, y=100, anchor=tk.CENTER)
        self.line = self.canvas.create_line(
            (400 - 300) / 2, 20,
            (400 + 300) / 2, 20,
            fill="black",
            width=2
        )

        #play/pause icon
        self.play_icon = ctk.CTkImage(light_image=Image.open("icons\\recorder_frame\\play_icon.png"), size=(16,16))
        #play/pause button
        self.play_btn = ctk.CTkButton(self.player_frame,  text="", image=self.play_icon, command=self.playPause)
        self.play_btn.configure(width=52, height=52, corner_radius=0,fg_color="#ffffff", hover_color="#E0E0E0")
        self.play_btn.place(x=269, y=160)

        self.play_lbl =  ctk.CTkLabel(self.player_frame, text="Pause")
        self.play_lbl.configure(fg_color="#ffffff",
                            text_color="#23295A",
                            font=('Inter', 14))
        self.play_lbl.place(x=273   , y=220)

        
        #Detect button
        self.detect_btn = ctk.CTkButton(self.player_frame, text="Detect Emotion", command=self.detectEmotion)
        self.detect_btn.configure(width=70, height=50, corner_radius=100,fg_color="#FFFFFF", hover_color="#C3B1E1", font=('Inter',16), text_color="#23295A" )
        self.detect_btn.place(relx=0.5, rely=0.85,anchor = tk.CENTER)



        self.totalTime = 0
        self.isPlaying = False
        self.threadStarted = False

        self.CHUNK = 1024
        self.FILE = audio_path
        self.wf =  wave.open(self.FILE, 'rb')
        self.audio = pyaudio.PyAudio()
        self.audioStreamOpen = False

        pass
    
    def playAudio(self):

        if not self.audioStreamOpen:
            self.stream = self.audio.open(format=self.audio.get_format_from_width(self.wf.getsampwidth()), channels=self.wf.getnchannels(), rate=self.wf.getframerate(), output=True)
            self.audioStreamOpen = True
        
        while True:
            if self.isPlaying:
                data=self.wf.readframes(self.CHUNK)
                while data and  self.isPlaying:
                    self.stream.write(data)
                    data = self.wf.readframes(self.CHUNK)
               

                    if not data:
                        # Close and terminate the stream
                        self.stream.close()
                        self.audio.terminate()
                        self.resetConfiguration()
                
            else: break

    def resetConfiguration(self):
        self.isPlaying = False
        self.totalTime = 0
        self.threadStarted = False
        self.audio = pyaudio.PyAudio()
        self.audioStreamOpen = False
        self.wf =  wave.open(self.FILE, 'rb')
        self.play_icon.configure(light_image=Image.open("icons\\recorder_frame\\restart_icon.png"), size=(24,29))
        self.play_lbl.configure(text="Restart")

    def playPause(self):
        self.isPlaying = not self.isPlaying
        
        if self.isPlaying:
            
            self.play_icon.configure(light_image=Image.open("icons\\recorder_frame\\pause_icon.png"), size=(16,16))
            self.play_lbl.configure(text="Pause")
            
            if not self.threadStarted:
                self.threadStarted = True
                threading.Thread(target=self.startTimer, daemon=True).start()
                threading.Thread(target=self.playAudio, daemon=True).start()                

        else:
            self.threadStarted=False
            self.play_icon.configure(light_image=Image.open("icons\\recorder_frame\\play_icon.png"), size=(16,16))
            self.play_lbl.configure(text="Start")
    
    def startTimer(self):
        while True:
            
            if self.isPlaying:


                seconds = self.totalTime % 60 
                minutes =  (int(self.totalTime/60) ) % 60
                hours = (int(self.totalTime/3600))
                self.time_lbl.configure(text=f"{hours:02}:{minutes:02}:{seconds:02}")
                
                self.totalTime = self.totalTime + 1
                time.sleep(1)
            else: 
                break

    def handleBack(self):
            self.resetConfiguration()
            self.window.destroy()

    def detectEmotion(self):

        self.window.withdraw()
        pred = ModelPredictor(self.PATH)
        emotion = pred.predict()
        self.emotionDetector = EmotionDetector(self.window, emotion)
        self.emotionDetector.detectorWindow.wait_window()
        self.window.deiconify()        

        pass
if __name__ == "__main__":
    AudioPlayer()