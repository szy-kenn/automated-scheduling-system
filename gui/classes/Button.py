from customtkinter import CTkButton
from constants import * 

class Button(CTkButton):
    
    PRIMARY = 1
    SECONDARY = 2

    def __init__(self, master, type, label, label_text, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        self.type = type
        self.label = label
        self.label_text = label_text
        self.bind("<Enter>", command= lambda x: self.hover())
        self.bind("<Leave>", command= lambda x: self.unhover())

    def hover(self):
        if self.type == 1:
            self.configure(fg_color=HOVER_COLOR,
                           text_color="white")
        elif self.type == 2:
            self.configure(fg_color=HOVER_COLOR,
                           border_color=HOVER_COLOR,
                           text_color="white")
            
        if self.label != None:
            self.label.configure(text=self.label_text)
        # hover_label = ct.CTkLabel(self.master,
        #                                      text="HOVER LABEL")
        # hover_label.grid(row=self.grid_info()['row']-1, column=self.grid_info()['column'])

    def unhover(self):
        if self.type == 1:
            self.configure(fg_color=PRIMARY_BUTTON,
                           text_color=PRIMARY_COLOR)
        elif self.type == 2:
            self.configure(fg_color=PRIMARY_COLOR,
                           border_color=PRIMARY_BUTTON,
                           text_color=PRIMARY_BUTTON)
            
        if self.label != None:
            self.label.configure(text="")

    def button_callback(self):
        print("button clicked")