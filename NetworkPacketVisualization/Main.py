import customtkinter
import os
from PIL import Image
import pyshark 
import tkinter as tk
from tkinter import filedialog
import collections
import matplotlib.pyplot as plt
import numpy as np
import screen_brightness_control as sbc
import time
import os.path

class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()

        self.title(" ")
        self.geometry("1920x1080")
        customtkinter.set_default_color_theme("dark-blue")
        customtkinter.set_appearance_mode("dark")

        # set grid layout 1x2 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logoo.png")), size=(30, 30))
        self.gb_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "gb.jpg")),size=(900,70))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.browse_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "browse.png")), size=(20, 20))
        self.data_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "data.jpg")), size=(168, 105))
        self.minlen_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "minlen.png")), size=(20, 20))
        self.maxlen_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "maxlen.png")), size=(20, 20))
        self.mintime_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "mintime.png")), size=(20, 20))
        self.maxtime_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "maxtime.png")), size=(20, 20))
        self.ftp_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "ftp.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "house.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "house.png")), size=(24, 24))
        self.packet_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "packet.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "packet.png")), size=(24, 24))
        self.analysis_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "analysis.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "analysis.png")), size=(24, 24))
        self.settings_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "settings.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "settings.png")), size=(24, 24))
                                        
    
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(8, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  KAMIKAZE     ", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=21, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=34)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=17, text=" Home                                 ",
                                                   fg_color="transparent",font=customtkinter.CTkFont(size=16, weight="normal"), text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=17, text=" Packet Details                    ",
                                                      fg_color="transparent",font=customtkinter.CTkFont(size=16, weight="normal"), text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.packet_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=17, text=" Analysis Of Packets               ",
                                                      fg_color="transparent",font=customtkinter.CTkFont(size=16, weight="normal"), text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.analysis_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=17, text=" Settings                          ",
                                                      fg_color="transparent",font=customtkinter.CTkFont(size=16, weight="normal"), text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.settings_image, anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=9, column=0, sticky="ew")

        self.frame_5_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=17, text=" Analysis by Filtering                           ",
                                                      fg_color="transparent",font=customtkinter.CTkFont(size=16, weight="normal"), text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.settings_image, anchor="w", command=self.frame_5_button_event)
        self.frame_5_button.grid(row=4, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=10, column=0, padx=20, pady=20, sticky="s")


if __name__ == "__main__":
    app = App()
    app.mainloop()