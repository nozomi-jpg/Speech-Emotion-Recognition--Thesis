import tkinter as tk
import customtkinter as ctk
from PIL import Image

class EmotionDetector:
    def __init__(self, window, emotion):
        self.emotion = emotion #sample

        #main frame
        width = int(window.winfo_screenwidth()/2 - (708/2))
        height = int(window.winfo_screenheight()/2 - (512/2))
        self.detectorWindow = ctk.CTkToplevel()
        self.detectorWindow.geometry(f"708x512+{width}+{height}")
        self.detectorWindow.title("Emotion Detector")
        self.detectorWindow.resizable(False, False)

        self.detector_frame = ctk.CTkFrame(self.detectorWindow, width=572, height=700,corner_radius=20)
        self.detector_frame.configure(fg_color="#2A295C")
        self.detector_frame.place(relx=0.5, y=-21,anchor=tk.CENTER)

        #Detected Emotion Heading
        self.detector_lbl = ctk.CTkLabel(self.detectorWindow, text="DETECTED EMOTION")
        self.detector_lbl.configure(fg_color = "#2A295C",
                        font=('Inter', 20),
                        text_color="#FFFFFF")

        self.detector_lbl.place(relx=0.5, y=60,anchor = tk.CENTER)

        #Emotion Icon
        self.emotion_icon = ctk.CTkImage(light_image=Image.open(f"icons\\emotions\\{self.emotion}.png"), size=(144,144))
        self.emotion_icon_lbl =  ctk.CTkLabel(self.detector_frame, image=self.emotion_icon, text="")
        self.emotion_icon_lbl.configure(fg_color = "transparent")

        self.emotion_icon_lbl.place(relx=0.5, rely=0.76, anchor=tk.CENTER)

        #Emotion Label
        self.emotion_lbl = ctk.CTkLabel(self.detectorWindow, text=f"{self.emotion}")
        self.emotion_lbl.configure(fg_color = "#2A295C",
                        font=('Inter', 32),
                        text_color="#FFFFFF")

        self.emotion_lbl.place(relx=0.5, y=272,anchor = tk.CENTER)

        #Button
        self.menu_btn = ctk.CTkButton(self.detectorWindow, text="Back To Recorder", command=self.handleClick)
        self.menu_btn.configure(width=229, height=50, corner_radius=8,fg_color="#F6867A", hover_color="#EB7B70", font=('Inter',20), text_color="#FFFFFF" )
        self.menu_btn.place(relx=0.5, rely=0.8,anchor = tk.CENTER)

    def handleClick(self):
        self.detectorWindow.destroy()
