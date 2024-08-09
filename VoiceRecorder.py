import time
import threading
import tkinter as tk
import customtkinter as ctk
from PIL import Image
import pyaudio
import wave
from datetime import datetime
from EmotionDetector import EmotionDetector
from Predict import ModelPredictor

class VoiceRecorder():

    def __init__(self):
        self.window = ctk.CTkToplevel()
        width = int(self.window.winfo_screenwidth()/2 - (708/2))
        height = int(self.window.winfo_screenheight()/2 - (512/2))
        self.window.geometry(f"708x512+{width}+{height}")
        self.window.title("Voice Recorder")
        self.window.resizable(False, False)

        #recorder frame
        self.recorder_frame = ctk.CTkFrame(self.window, width=571, height=367,corner_radius=20)
        self.recorder_frame.configure(fg_color="#2A295C")
        self.recorder_frame.place( relx=0.5, rely=0.5, anchor = tk.CENTER)

        #timer frame
        self.timer_frame = ctk.CTkFrame(self.recorder_frame, width=163, height=163,corner_radius=90)
        self.timer_frame.configure(fg_color="#FFFFFF")
        self.timer_frame.place(x=203 ,y=47)

        #timer counter
        self.time_lbl = ctk.CTkLabel(self.timer_frame, text="00:00:00")
        self.time_lbl.configure(fg_color="transparent",
                        font=('Inter', 26),
                        text_color="#23295A")

        self.time_lbl.place(relx=0.5, y=65,anchor = tk.CENTER)

        #recorder icon container
        self.recorder_icon = ctk.CTkImage(light_image=Image.open("icons\\recorder_frame\\recorder_icon.png"), size=(20,32))
        self.recorder_icon_lbl =  ctk.CTkLabel(self.timer_frame, text="", image=self.recorder_icon)
        self.recorder_icon_lbl.configure(fg_color = "transparent")

        self.recorder_icon_lbl.place(relx=0.5, y=110,anchor = tk.CENTER)

        #record/restart icon
        self.restart_icon = ctk.CTkImage(light_image=Image.open("icons\\recorder_frame\\restart_icon.png"), size=(24,29))
        #record/restart button
        self.restart_btn = ctk.CTkButton(self.recorder_frame,  text="", image=self.restart_icon, command=self.restartRecording )
        self.restart_btn.configure(width=52, height=52, corner_radius=10,fg_color="#ffffff", hover_color="#E0E0E0")
        self.restart_btn.place(x=112, y=265)

        self.restart_lbl =  ctk.CTkLabel(self.recorder_frame, text="Restart")
        self.restart_lbl.configure(fg_color="transparent",
                            text_color="#ffffff",
                            font=('Inter', 14))
        self.restart_lbl.place(x=110, y=327)

        #play/pause icon
        self.play_icon = ctk.CTkImage(light_image=Image.open("icons\\recorder_frame\\start_record_icon.png"), size=(16,16))
        #play/pause button
        self.play_btn = ctk.CTkButton(self.recorder_frame,  text="", image=self.play_icon, command=self.playPause)
        self.play_btn.configure(width=52, height=52, corner_radius=10,fg_color="#ffffff", hover_color="#E0E0E0")
        self.play_btn.place(x=269, y=265)

        self.play_lbl =  ctk.CTkLabel(self.recorder_frame, text="Record")
        self.play_lbl.configure(fg_color="transparent",
                            text_color="#ffffff",
                            font=('Inter', 14))
        self.play_lbl.place(x=273   , y=327)

        #stop icon
        self.stop_icon = ctk.CTkImage(light_image=Image.open("icons\\recorder_frame\\stop_icon.png"), size=(16,16))
        #stop button
        self.stop_btn = ctk.CTkButton(self.recorder_frame,  text="", image=self.stop_icon, command=self.stopRecording, state="disabled")
        self.stop_btn.configure(width=52, height=52, corner_radius=10,fg_color="#ffffff", hover_color="#E0E0E0" )
        self.stop_btn.place(x=423, y=265)

        self.stop_lbl =  ctk.CTkLabel(self.recorder_frame, text="Stop")
        self.stop_lbl.configure(fg_color="transparent",
                            text_color="#ffffff",
                            font=('Inter', 14))
        self.stop_lbl.place(x=435, y=327)

        #back Button
        self.menu_btn = ctk.CTkButton(self.window, text="<", command=self.handleBack)
        self.menu_btn.configure(width=15, height=30, corner_radius=8,fg_color="#F6867A", hover_color="#EB7B70", font=('Inter',20), text_color="#FFFFFF" )
        self.menu_btn.place(x=70, y=30)


        self.totalTime = 0
        self.isRecording = False
        self.threadStarted = False

        self.audio = pyaudio.PyAudio()
        self.audioStreamOpen = False

        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024

        self.frames = [] 

    def playPause(self):
        self.stop_btn.configure(state="normal")
        self.isRecording = not self.isRecording

        if self.isRecording:

            self.play_icon.configure(light_image=Image.open("icons\\recorder_frame\\pause_icon.png"))
            self.play_lbl.configure(text="Pause")

            if not self.threadStarted:
                self.threadStarted = True
                threading.Thread(target=self.startTimer, daemon=True).start()
                threading.Thread(target=self.recordAudio, daemon=True).start()

        else:
            self.threadStarted=False
            self.play_icon.configure(light_image=Image.open("icons\\recorder_frame\\play_icon.png"))
            self.play_lbl.configure(text="Start")



    def startTimer(self):
        while True:
            if self.isRecording:
                seconds = self.totalTime % 60 
                minutes =  (int(self.totalTime/60) ) % 60
                hours = (int(self.totalTime/3600))
                self.time_lbl.configure(text=f"{hours:02}:{minutes:02}:{seconds:02}")
                
                self.totalTime = self.totalTime + 1
                time.sleep(1)
            else: break

    def recordAudio(self):
        if not self.audioStreamOpen:
            self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, frames_per_buffer=self.CHUNK, input=True)
            self.audioStreamOpen = True

        while True:
            if self.isRecording:
                data=self.stream.read(self.CHUNK)
                self.frames.append(data)

            else: break


    def stopRecording(self):
        
        self.isRecording = False

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        self.messageBoxTopLevel()
        self.messageBox.wait_window()

        if self.msgAnswer == True:
            self.messageBox.destroy()
            timeStamp =  datetime.now().strftime("%Y-%m-%d") + '-' + datetime.now().strftime("%H-%M-%S")      
            self.fileName = f"{timeStamp}.wav"  #use this to determine which audio file to pass to emotion detector
            
            file = wave.open(f"audio_file\\{self.fileName}", "wb")
            file.setnchannels(self.CHANNELS)
            file.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            file.setframerate(self.RATE)
            file.writeframes(b"".join(self.frames))
            file.close()
            
            self.resetConfiguration()

            self.window.withdraw()
            pred = ModelPredictor(f"audio_file\\{self.fileName}")
            emotion = pred.predict()
            self.emotionDetector = EmotionDetector(self.window, emotion)
            self.emotionDetector.detectorWindow.wait_window()
            self.window.deiconify()        
        

        else: 
            self.resetConfiguration()
        return
    
    def resetConfiguration(self):
        self.play_lbl.configure(text="Record")
        self.play_btn.configure(state="normal")
        self.play_icon.configure(light_image=Image.open("icons\\recorder_frame\\start_record_icon.png"), size=(16,16))
        self.stop_btn.configure(state="disabled")
        self.time_lbl.configure(text="00:00:00")

        self.isRecording = False
        self.totalTime = 0
        self.threadStarted = False
        self.audioStreamOpen = False
        self.frames = []
        self.audio = pyaudio.PyAudio()

    def restartRecording(self):
        self.resetConfiguration()

    def messageBoxTopLevel(self):
        width = int(self.window.winfo_screenwidth()/2 - (530/2))
        height = int(self.window.winfo_screenheight()/2 - (200/2))
        
        self.messageBox = ctk.CTkToplevel()
        self.messageBox.grab_set()
        self.messageBox.geometry(f'530x200+{width}+{height}')
        self.messageBox.configure(
            fg_color = "#474FA3",
            corner_radius = 10
        )

        self.messageBox.overrideredirect(1)    
        self.question_lbl = ctk.CTkLabel(self.messageBox, text="Do you want to start detecting emotion?")
        self.question_lbl.configure(font=('Inter', 20),
                               text_color="#FFFFFF")
        self.question_lbl.place(relx=0.5, y=40, anchor = tk.CENTER)

        #detectButton
        self.detect_btn = ctk.CTkButton(self.messageBox, text="Detect", command=lambda:self.handleClick(True))
        self.detect_btn.configure(width=229, height=50, corner_radius=8,fg_color="#FFFFFF", hover_color="#E0E0E0", font=('Inter',20), text_color="#474FA3")
        self.detect_btn.place(x=23, y=90)

        #CancelButton
        self.cancel_btn = ctk.CTkButton(self.messageBox, text="Cancel", command=lambda:self.handleClick(False))
        self.cancel_btn.configure(width=229, height=50, corner_radius=8,fg_color="#FF8679", hover_color="#EB7B70", font=('Inter',20))
        self.cancel_btn.place(x=276, y=90)
    
    def handleClick(self,value):
        self.msgAnswer = value
        self.messageBox.destroy()

    def handleBack(self):
        self.window.destroy()



if __name__=="__main__":
    VoiceRecorder()