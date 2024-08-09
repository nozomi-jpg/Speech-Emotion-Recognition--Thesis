import tkinter as tk
from tkinter import *
from tkinter import filedialog
from pydub import AudioSegment
import customtkinter as ctk
from PIL import Image
import time
from VoiceRecorder import VoiceRecorder
from AudioPlayer import AudioPlayer
class Menu:
    def __init__(self):
        self.window = tk.Tk()
        width = int(self.window.winfo_screenwidth()/2 - (708/2))
        height = int(self.window.winfo_screenheight()/2 - (512/2))
        self.window.geometry(f"708x512+{width}+{height}")
        self.window.title("Speech Emotion Recognition")
        self.window.resizable(False, False)
        
        #Upload button
        self.upload_btn = ctk.CTkButton(self.window, text="", command=self.upload_file)
        self.upload_btn.configure(width=200, 
                                  height=200, 
                                  corner_radius=8,
                                  fg_color="#FFFFFF", 
                                  hover_color="#EEEEEE",
                                  border_width = 8, 
                                  font=('Inter',20), 
                                  text_color="#474FA3",
                                  border_color="#23295A",
                                )
        self.upload_btn.place(x=100, y=140)

        #upload icon container
        self.upload_icon = ctk.CTkImage(light_image=Image.open("icons\\menu\\upload_icon.png"), size=(60,60))
        self.upload_icon_lbl =  ctk.CTkLabel(self.upload_btn, text="", image=self.upload_icon)
        self.upload_icon_lbl.configure(fg_color = "transparent")

        self.upload_icon_lbl.place(relx=0.5, y=85,anchor = tk.CENTER)


        self.upload_lbl =  ctk.CTkLabel(self.upload_btn, text="Upload Audio File")
        self.upload_lbl.configure(text_color="#474FA3", fg_color="transparent", font=('Inter', 16))
        self.upload_lbl.place(relx=0.5, y=160,anchor = tk.CENTER)

        #Record Button
        self.record_btn = ctk.CTkButton(self.window, text="", command=self.record_audio)
        self.record_btn.configure(width=200, 
                                  height=200, 
                                  corner_radius=8,
                                  fg_color="#FFFFFF", 
                                  hover_color="#E0E0E0",
                                  border_width = 8, 
                                  font=('Inter',20), 
                                  text_color="#474FA3",
                                  border_color="#23295A")
        self.record_btn.place(x=400, y=140)

        #recorder icon container
        self.record_icon = ctk.CTkImage(light_image=Image.open("icons\\menu\\record_icon.png"), size=(40,60))
        self.record_icon_lbl =  ctk.CTkLabel(self.record_btn, text="", image=self.record_icon)
        self.record_icon_lbl.configure(fg_color = "transparent")

        self.record_icon_lbl.place(relx=0.5, y=85,anchor = tk.CENTER)


        self.record_lbl =  ctk.CTkLabel(self.record_btn, text="Record Audio")
        self.record_lbl.configure(text_color="#474FA3", fg_color="transparent", font=('Inter', 16))
        self.record_lbl.place(relx=0.5, y=160,anchor = tk.CENTER)

        self.window.mainloop()


        pass

  
    def upload_file(self):
        self.window.filepath = filedialog.askopenfilename(initialdir='/', title="Upload an Audio File", filetypes=(("WAV files", "*.wav"), ("all files", "*.*")))
        
        if (self.window.filepath):
            self.window.withdraw()
            self.audioPlayer = AudioPlayer(self.window.filepath)
            self.audioPlayer.window.wait_window()
            self.window.deiconify()
            
    def record_audio(self):
        self.window.withdraw()
        time.sleep(1)
        self.voiceRecorder = VoiceRecorder()
        self.voiceRecorder.window.wait_window()
        time.sleep(1)
        self.window.deiconify()

if __name__=="__main__":
    Menu()
