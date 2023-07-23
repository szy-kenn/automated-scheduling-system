import customtkinter as ct
import tkinter as tk
from . import Button

class SegmentedButton(tk.Frame):
    def __init__(self, master, width, height, *, values:list) -> None:
        self.master = master
        self.width = width
        self.height = height
        super().__init__(master, width=width, height=height, background="black",
                         highlightthickness=1, highlightbackground="white", )

        self.values = values
        self.length = len(self.values)

        for idx, value in enumerate(self.values):
            value_button = Button(self, Button.SECONDARY, None, None, 
                                   width=self.width/self.length+1, height=self.height,
                                   text_color="white", fg_color="transparent",
                                    corner_radius=0, text=value, font=ct.CTkFont("Roboto", 12))
            
            value_button.grid(row=0, column=idx, ipady=3, ipadx=5)
