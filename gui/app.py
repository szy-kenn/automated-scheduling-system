import customtkinter as ct
from PIL import Image

ct.set_default_color_theme("gui/app.json")
FONT_FAMILY = "Montserrat"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
PRIMARY_COLOR = "black"
PRIMARY_BUTTON = "#DADFF7"
HOVER_COLOR = "#50C878"

class Frame(ct.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


class Button(ct.CTkButton):
    
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
        
        self.label.configure(text="")

    def button_callback(self):
        print("button clicked")


class App(ct.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Automated Scheduling System")
        self.iconbitmap("assets\dna-white.ico")
        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.home = None
        self.scheduler = None
        self.create_scheduler()
        self.create_home()
        self.show_frame(self.home)

    def show_frame(self, frame):
        frame.tkraise()

    def create_scheduler(self):
        self.scheduler = ct.CTkFrame(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, corner_radius=0)

        self.scheduler.grid_columnconfigure(0, weight=1)
        self.scheduler.grid_rowconfigure(0, weight=1)
        self.scheduler.grid(row=0, column=0, sticky="nsew")

        label = ct.CTkLabel(self.scheduler, text="This is a new frame")
        label.grid()

    def create_home(self):

        self.home = ct.CTkFrame(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, corner_radius=0)

        self.home.grid_columnconfigure(0, weight=1)
        self.home.grid_rowconfigure(0, weight=1)
        self.home.grid(row=0, column=0, sticky="nsew")
        # ICON
        icon_img = ct.CTkImage(light_image=Image.open("assets\dna.png"),
                                          dark_image=Image.open("assets\dna-white.png"),
                                          size=(55, 47))
        icon_label = ct.CTkLabel(self.home, image=icon_img, text="")
        icon_label.grid(row=0, column=0, pady=56)

        # HEADER
        header = ct.CTkFrame(self.home, width=SCREEN_WIDTH, height=SCREEN_HEIGHT/4)
        header.grid(row=1, column=0)

        # HEADING
        heading_font = ct.CTkFont(FONT_FAMILY, 26, "bold")
        heading = ct.CTkLabel(header, 
                                         text="AUTOMATED SCHEDULING SYSTEM", 
                                         font=heading_font,
                                         fg_color="transparent", 
                                         anchor="center")
        heading.pack()

        # SUBHEADING
        subheading_font = ct.CTkFont(FONT_FAMILY, 12)
        subheading = ct.CTkLabel(header,
                                            text="A university course scheduler application using Genetic Algorithm.",
                                            font=subheading_font,
                                            fg_color="transparent",
                                            anchor="center")
        subheading.pack(after=heading)

        # MAIN BUTTONS
        buttons_frame = ct.CTkFrame(self.home, width=SCREEN_WIDTH, height=SCREEN_HEIGHT/4)
        buttons_frame.grid(row=2, column=0, padx=40, pady=40)
        buttons_frame.grid_rowconfigure((0, 1), weight=1)
        buttons_frame.grid_columnconfigure((0, 1), weight=1)

        start_btn_label = ct.CTkLabel(buttons_frame, text="")
        start_btn_label.grid(row=0, column=0)

        btn_font = ct.CTkFont("Roboto", 16, "bold")
        start_btn = Button(buttons_frame, 
                           Button.PRIMARY, 
                           start_btn_label,
                           label_text="Start Scheduling!",
                           width=198, 
                            height=44, 
                            corner_radius=0, 
                            text="START",
                            font=btn_font,
                            command=lambda: self.show_frame(self.scheduler))   

        start_btn.grid(row=1, column=0, padx=5)

        how_it_works_label = ct.CTkLabel(buttons_frame, text="")
        how_it_works_label.grid(row=0, column=1)

        how_it_works_btn = Button(buttons_frame,
                                  Button.SECONDARY,
                                  how_it_works_label, 
                                  "What is a Genetic Algorithm?",
                                  width=198, 
                                  height=44,
                                  corner_radius=0,
                                  text="HOW IT WORKS",
                                  text_color="white",
                                  font=btn_font,
                                  fg_color="transparent",
                                  border_color="white",
                                  border_width=1)

        how_it_works_btn.grid(row=1, column=1, padx=5)


app = App()
app.mainloop()