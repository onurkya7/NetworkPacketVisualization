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

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame_33 = customtkinter.CTkFrame(self.home_frame, corner_radius=0)
        self.home_frame_33.grid(row=0, column=0,ipady= 500, sticky="nsew")
        self.home_frame_33.grid_rowconfigure(10, weight=1)
        self.home_frame_33.grid_columnconfigure(1, weight=1)
        self.frame_info = customtkinter.CTkFrame(self.home_frame_33)
        self.frame_info.grid(row=1, column=0, columnspan=2, rowspan=4, pady=20, padx=100, sticky="nsew")
        self.frame_info.grid_rowconfigure(10, weight=1)
        self.frame_info.grid_columnconfigure(1, weight=1)
        self.labelinfo_mode = customtkinter.CTkLabel(self.home_frame_33, 
                                                     text="Listening makes attacking easier to understand..",
                                                     font=customtkinter.CTkFont(size=21, weight="bold"),image= self.gb_image)
        self.labelinfo_mode.grid(row=0, column=0, pady=20, padx=100, sticky="w")    
        self.entry_6 = customtkinter.CTkEntry(self.frame_info,
                                                width=650,
                                                placeholder_text="Select Pcap File")
        self.entry_6.grid(row=1, column=0,  pady=5, padx=10, sticky="we")
        self.entry_7 = customtkinter.CTkEntry(self.frame_info,
                                                width=650,
                                                placeholder_text="Select Csv File")
        self.entry_7.grid(row=3, column=0,  pady=5, padx=10, sticky="we")
        self.folder_button = customtkinter.CTkButton(self.frame_info,
                                                text="Browse",
                                                border_width=2,
                                                image=self.browse_image,
                                                fg_color="black",  # <- no fg_color
                                                command=self.my_fun)
        self.folder_button.grid(row=1, column=1,padx=10, sticky="ew")
        self.folder_button_2 = customtkinter.CTkButton(self.frame_info,
                                                text="Browse",
                                                border_width=2,
                                                image=self.browse_image,
                                                fg_color="black",  # <- no fg_color
                                                command=self.my_fun)
        self.folder_button_2.grid(row=3, column=1,padx=10, sticky="ew")
        self.home_label_1 = customtkinter.CTkLabel(self.frame_info,
                                                        text="Pcap:")
        self.home_label_1.grid(row=0, column=0, columnspan=1, pady=5, padx=0, sticky="")
        self.home_label_2 = customtkinter.CTkLabel(self.frame_info,
                                                        text="Csv:")
        self.home_label_2.grid(row=2, column=0, columnspan=1, pady=5, padx=0, sticky="")
        self.home_frame_44 = customtkinter.CTkFrame(self.home_frame, corner_radius=0)
        self.home_frame_44.grid(row=0, column=1,ipady= 500,ipadx=70,padx=0, sticky="nsew")
    
    
        # create second frame
        ##frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame_11 = customtkinter.CTkFrame(self.second_frame, corner_radius=0,fg_color="transparent")
        self.second_frame_11.grid(row=0, column=0,ipady= 500,ipadx=50, sticky="nsew")
        self.second_frame_11.grid_rowconfigure(10, weight=1)
        self.second_frame_11.grid_columnconfigure(3, weight=1)
        self.second_frame_22 = customtkinter.CTkFrame(self.second_frame, corner_radius=0,fg_color="transparent")
        self.second_frame_22.grid(row=0, column=1,ipady= 500,ipadx=100, sticky="nsew")
        self.second_frame_22.grid_rowconfigure(1, weight=1)
        self.second_frame_22.grid_columnconfigure(0, weight=1)   
        self.labelfree_mode = customtkinter.CTkLabel(self.second_frame_11, text="")
        self.labelfree_mode.grid(row=2, column=1, pady=20, padx=40, sticky="w")
        self.labelfree2_mode = customtkinter.CTkLabel(self.second_frame_11, text="")
        self.labelfree2_mode.grid(row=2, column=1, pady=20, padx=40, sticky="w")
        self.labelfree3_mode = customtkinter.CTkLabel(self.second_frame_11, text="")
        self.labelfree3_mode.grid(row=5, column=1, pady=20, padx=40, sticky="w")
        self.labelfree4_mode = customtkinter.CTkLabel(self.second_frame_11, text="")
        self.labelfree4_mode.grid(row=5, column=1, pady=20, padx=40, sticky="w")
        self.labelfree5_mode = customtkinter.CTkLabel(self.second_frame_11, text="       Enter the package number:")
        self.labelfree5_mode.grid(row=3, column=0, pady=20, padx=40, sticky="w")
        #self.labelswitch_1 = customtkinter.CTkLabel(self.second_frame_11, text="       Use Json:")
        #self.labelswitch_1.grid(row=5, column=0, pady=20, padx=40, sticky="w")        
        self.switch_1 = customtkinter.CTkSwitch(self.second_frame_11,text=" JSON",progress_color="green")
        self.switch_1.grid(row=4, column=1,pady=10, padx=10)     
        self.entry_1 = customtkinter.CTkEntry(self.second_frame_11,
                                            width=200,
                                            placeholder_text="")
        self.entry_1.grid(row=3, column=1,  pady=20, padx=10, sticky="we")
        self.button_10 = customtkinter.CTkButton(self.second_frame_11,
                                                text="Analyze",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.analysis)
        self.button_10.grid(row=5, column=1, padx=20, pady=10)
        self.textbox_1 = customtkinter.CTkTextbox(self.second_frame_22, fg_color="black", corner_radius=0,text_color="white")
        self.textbox_1.grid(row=0, column=0, ipadx= 70,ipady= 300,pady=60,padx=20, sticky="nsew")       
        self.textbox_1.insert("0.0", "Enter package index and analyze..")

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame_1 = customtkinter.CTkFrame(self.third_frame, corner_radius=0,fg_color="transparent")
        self.third_frame_1.grid(row=1, column=0,padx=10,pady=10,sticky="nsew")
        self.third_frame_2 = customtkinter.CTkFrame(self.third_frame, corner_radius=0,fg_color="transparent")
        self.third_frame_2.grid(row=1, column=1,padx=10,pady=10,sticky="nsew")
        self.third_frame_3 = customtkinter.CTkFrame(self.third_frame, corner_radius=0,fg_color="transparent")
        self.third_frame_3.grid(row=2, column=0,padx=10,pady=10,sticky="nsew")
        self.third_frame_4 = customtkinter.CTkFrame(self.third_frame, corner_radius=0,fg_color="transparent")
        self.third_frame_4.grid(row=2, column=1,padx=10,pady=10,sticky="nsew")
        self.third_frame_0 = customtkinter.CTkFrame(self.third_frame, corner_radius=0,fg_color="transparent")
        self.third_frame_0.grid(row=0, column=0,padx=10,pady=10,sticky="nsew")
        self.third_frame_0.grid_columnconfigure(4, weight=1)
        self.third_button_1 = customtkinter.CTkButton(self.third_frame_0,
                                                text="Graph",
                                                border_width=2,  
                                                fg_color=None,
                                                command=self.graph)
        self.third_button_1.grid(row=0, column=0, padx=70, pady=10)
        self.third_button_2 = customtkinter.CTkButton(self.third_frame_0,
                                                text="Delete",
                                                border_width=2,  
                                                fg_color=None,  
                                                command=self.delete)
        self.third_button_2.grid(row=0, column=1, padx=70, pady=10)
        self.third_entry = customtkinter.CTkEntry(self.third_frame_0,
                                                width=30,
                                                placeholder_text="Folder")
        self.third_entry.grid(row=0, column=2,  pady=5, padx=70,ipadx=50, sticky="we")
        self.third_entry.insert("0",0)

        self.third_label_2 = customtkinter.CTkLabel(self.third_frame_3,
                                                        text="Source Ip Limit:")
        self.third_label_2.grid(row=1, column=0, columnspan=1, pady=10, padx=200, sticky="")
        self.third_label_3 = customtkinter.CTkLabel(self.third_frame_3,
                                                        text="Dest Ip Limit:")
        self.third_label_3.grid(row=3, column=0, columnspan=1, pady=10, padx=200, sticky="")
        self.third_entry_2= customtkinter.CTkEntry(self.third_frame_3,
                                                width=50,
                                                placeholder_text="Count_S")
        self.third_entry_2.grid(row=2, column=0,  pady=10, padx=200, sticky="we")
        self.third_entry_2.insert("0",0)
        self.third_entry_3 = customtkinter.CTkEntry(self.third_frame_3,
                                            width=50,
                                            placeholder_text="Count_D ")
        self.third_entry_3.grid(row=4, column=0,  pady=10, padx=200, sticky="we")
        self.third_entry_3.insert("0",0)
    

        #settings (fourth frame)
        self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.fourth_frame_1 = customtkinter.CTkFrame(self.fourth_frame, corner_radius=0,fg_color="transparent")
        self.fourth_frame_1.grid(row=0, column=0,padx=10,pady=10,sticky="nsew")
        self.scaling_label = customtkinter.CTkLabel(self.fourth_frame_1, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=0, column=0, padx=20, pady=(20, 0))
        self.scaling_label_1 = customtkinter.CTkLabel(self.fourth_frame_1, text="Screen Brightness:", anchor="w")
        self.scaling_label_1.grid(row=2, column=0, padx=20, pady=(20, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.fourth_frame_1, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=1, column=0, padx=20, pady=(10, 20))
        self.slider_1 = customtkinter.CTkSlider(self.fourth_frame_1, command=self.slider_callback, from_=0, to=1)
        self.slider_1.grid(row=3,column=0, pady=20, padx=20)
        self.slider_1.set(0.8)

        # create fifth frame
        self.fifth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.fifth_frame_1 = customtkinter.CTkFrame(self.fifth_frame, corner_radius=0,fg_color="transparent")
        self.fifth_frame_1.grid(row=0, column=0,padx=10,pady=10,sticky="nsew")
        self.fifth_frame_2 = customtkinter.CTkFrame(self.fifth_frame, corner_radius=0,fg_color="transparent")
        self.fifth_frame_2.grid(row=1, column=0,padx=10,pady=10,sticky="nsew")
        self.fifth_entry= customtkinter.CTkEntry(self.fifth_frame_1,
                                                width=100,
                                                placeholder_text="0")
        self.fifth_entry.grid(row=1, column=0,  pady=5, padx=60, sticky="we")
        self.fifth_entry_2= customtkinter.CTkEntry(self.fifth_frame_1,
                                                width=100,
                                                placeholder_text="0")
        self.fifth_entry_2.grid(row=1, column=1,  pady=5, padx=60, sticky="we")
        self.fifth_entry_3= customtkinter.CTkEntry(self.fifth_frame_1,
                                                width=100,
                                                placeholder_text="0")
        self.fifth_entry_3.grid(row=1, column=2,  pady=5, padx=60, sticky="we")
        self.fifth_entry_4= customtkinter.CTkEntry(self.fifth_frame_1,
                                                width=100,
                                                placeholder_text="0")
        self.fifth_entry_4.grid(row=1, column=3,  pady=5, padx=60, sticky="we")
        self.fifth_entry_5= customtkinter.CTkEntry(self.fifth_frame_1,
                                                width=100,
                                                placeholder_text="0")
        self.fifth_entry_5.grid(row=1, column=4,  pady=5, padx=60, sticky="we")
        self.fifth_label = customtkinter.CTkLabel(self.fifth_frame_1, text="  Protocol Filter:", anchor="w",image=self.ftp_image,compound="left")
        self.fifth_label.grid(row=0, column=0, padx=10, pady=(20, 0))
        self.fifth_label_2 = customtkinter.CTkLabel(self.fifth_frame_1, text="  Time Filter Min:", anchor="w",image=self.mintime_image,compound="left")
        self.fifth_label_2.grid(row=0, column=1, padx=10, pady=(20, 0))
        self.fifth_label_3 = customtkinter.CTkLabel(self.fifth_frame_1, text="  Time Filter Max:", anchor="w",image=self.maxtime_image,compound="left")
        self.fifth_label_3.grid(row=0, column=2, padx=10, pady=(20, 0))
        self.fifth_label_4 = customtkinter.CTkLabel(self.fifth_frame_1, text="  Length Filter Min:", anchor="w",image=self.minlen_image,compound="left")
        self.fifth_label_4.grid(row=0, column=3, padx=10, pady=(20, 0))
        self.fifth_label_5 = customtkinter.CTkLabel(self.fifth_frame_1, text="  Length Filter Max:", anchor="w",image=self.maxlen_image,compound="left")
        self.fifth_label_5.grid(row=0, column=4, padx=10, pady=(20, 0))
        self.fifth_button = customtkinter.CTkButton(self.fifth_frame_1,
                                                text="Filter",
                                                border_width=2,  
                                                fg_color="black",  
                                                command=self.filter)
        self.fifth_button.grid(row=0, column=5, padx=10, pady=10)
        self.fifth_button2 = customtkinter.CTkButton(self.fifth_frame_1,
                                                text="Delete",
                                                border_width=2,  
                                                fg_color=None,  
                                                command=self.delete2)
        self.fifth_button2.grid(row=1, column=5, padx=10, pady=10)



        # set default values
        self.scaling_optionemenu.set("100%")
        self.appearance_mode_menu.set("Dark")

        # select default frame
        self.select_frame_by_name("home")


if __name__ == "__main__":
    app = App()
    app.mainloop()
