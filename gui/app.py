import customtkinter as ct
import tkinter as tk
from CTkScrollableDropdown import *
from PIL import Image, ImageTk
from classes import *
from constants import *
from algo.final import Genetic

ct.set_default_color_theme("gui/app.json")

class App(ct.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Automated Scheduling System")
        self.iconbitmap("assets\dna-white.ico")
        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.year_values = ["1st Year", "2nd Year", "3rd Year", "4th Year"]
        self.year_var = ct.StringVar(value=self.year_values[1])
        self.department_values = ["1st Semester", "2nd Semester"]
        self.department_var = ct.StringVar(value=self.department_values[0])

        self.courses = {
            "1st Semester" : {  "1st Year": [
                            "COMP20023: Computer Programming 1", 
                            "NSTP10013: CWTS/ROTC", 
                            "GEED10103: Filipinolohiya at Pambansang Kaunlaran", 
                            "COMP20013: Introduction to Computing",
                            "GEED10053: Mathematics in the Modern World", 
                            "PHED01: Physical Education 1", 
                            "GEED20023: Politics, Governance and Citizenship", 
                            "GEED10063: Purposive Communication"
                        ], "2nd Year": [
                            "COSC-FE1: CS Free Elective 1",
                            "COMP20063: Data Structures and Algorithms",
                            "COMP20073: Discrete Structures 2",
                            "GEED10093: Ethics",
                            "COSC30023: Logic Design and Digital Computer Circuits",
                            "COSC30013: Modeling and Simulation",
                            "COMP20083: Object Oriented Programming",
                            "PHED03: Physical Education 3"
                            # "GEED10223: World Literature"  
                        ], "3rd Year": [

                        ], "4th Year": [

                        ]},
            "2nd Semester" : {  "1st Year": [
                            "MATH20333: Calculus", 
                            "COMP20033: Computer Programming 2", 
                            "NSTP10023: CWTS/ROTC",
                            "COMP20043: Discrete Structures 1",
                            "GEED10113: Pagsasalin sa Kontekstong Filipino",
                            "PHED02: Physical Education 2",
                            "GEED10083: Science, Technology and Society",
                            "GEED10023: Understanding the Self"
                        ], "2nd Year": [
                            "COMP20113: Technical Documentation and Presentation Skills", 
                            "PHED10042: Team Sports", 
                            "GEED20113: People and Earth's Ecosystem", 
                            "COMP20103: Operating Systems",
                            "COMP20093: Information Management", 
                            "COSC3033: Design and Analysis of Algorithms", 
                            "COSC-FE2: CS Free Elective", 
                            "GEED10073: Art Appreciation"
                        ], "3rd Year": [

                        ], "4th Year": [

                        ]},
        }

        self.home = None
        self.scheduler = None
        self.schedule_frame = None
        self.create_scheduler()
        self.create_home()
        self.show_frame(self.home)

    def show_frame(self, frame):
        frame.tkraise()

    def create_scheduler(self):
        self.scheduler = ct.CTkFrame(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, corner_radius=0)
        # self.scheduler.grid_columnconfigure(0, weight=1)
        # self.scheduler.grid_rowconfigure(0, weight=1)
        self.scheduler.grid(row=0, column=0, sticky="nsew")

        self.scheduler_canvas = tk.Canvas(self.scheduler,
                                          width=SCREEN_WIDTH,
                                          height=SCREEN_HEIGHT,
                                          highlightthickness=0,
                                          background="black")
        
        self.scheduler_canvas.place(x=0, y=0)

        # icons
        self.dna_icon = ImageTk.PhotoImage(Image.open("assets\dna-white.png").resize((32, 30)))
        self.scheduler_canvas.create_image(19, 17, image=self.dna_icon, anchor="nw")

        self.home_icon = ImageTk.PhotoImage(Image.open("assets\home-icon-white.png").resize((32, 30)))
        self.scheduler_canvas.create_image(19, 82, image=self.home_icon, anchor="nw")

        # self.history_icon = ImageTk.PhotoImage(Image.open("assets\history-icon-white.png").resize((32, 30)))
        # self.scheduler_canvas.create_image(19, 146, image=self.history_icon, anchor="nw")

        # self.log_icon = ImageTk.PhotoImage(Image.open("assets\log-icon-white.png").resize((32, 30)))
        # self.scheduler_canvas.create_image(19, 212, image=self.log_icon, anchor="nw")

        self.scheduler_home()

    def scheduler_home(self):
        
        self.scheduler_canvas.create_rectangle(-1, 66, 71, 126, fill="#2C2B2B")
        self.home_icon = ImageTk.PhotoImage(Image.open("assets\home-icon-white.png").resize((32, 30)))
        self.scheduler_canvas.create_image(19, 82, image=self.home_icon, anchor="nw")

        # division lines
        self.scheduler_canvas.create_line(0, 66, SCREEN_WIDTH, 66, fill=DARK_GRAY)
        self.scheduler_canvas.create_line(71, 66, 71, SCREEN_HEIGHT, fill=DARK_GRAY)
        self.scheduler_canvas.create_line(505, 66, 505, SCREEN_HEIGHT, fill=DARK_GRAY)
        self.scheduler_canvas.create_line(71, 200, 505, 200, fill=DARK_GRAY)
        self.scheduler_canvas.create_line(505, 240, SCREEN_WIDTH, 240, fill=DARK_GRAY)
        self.scheduler_canvas.create_line(505, 374, SCREEN_WIDTH, 374, fill=DARK_GRAY)

        # headings
        self.scheduler_canvas.create_text(99, 25, text="Automated Scheduling System", 
                                          fill="white", font=('Roboto 12'), anchor="nw")
        self.scheduler_canvas.create_text(88, 82, text="Program and Level:", 
                                    fill="white", font=('Roboto 16 bold'), anchor="nw")
        self.scheduler_canvas.create_text(88, 216, text="Courses:", 
                                          fill="white", font=('Roboto 16 bold'), anchor="nw")
        self.scheduler_canvas.create_text(522, 82, text="Constraints:", 
                                          fill="white", font=('Roboto 16 bold'), anchor="nw")
        self.scheduler_canvas.create_text(522, 251, text="Parameters:", 
                                          fill="white", font=('Roboto 16 bold'), anchor="nw")
        
        # program and level section
        self.scheduler_canvas.create_text(88, 125, text="Department:", 
                                          fill="white", font=('Roboto 12'), anchor="nw")
        self.scheduler_canvas.create_text(88, 161, text="Year Level:", 
                                          fill="white", font=('Roboto 12'), anchor="nw")

        department_option = ct.CTkComboBox(self.scheduler_canvas, width=240, 
                                           state="readonly", variable=self.department_var)

        CTkScrollableDropdown(department_option, values=self.department_values, justify="left", 
                              button_color="#151515", fg_color="#151515",
                              hover_color=DARK_GRAY, frame_corner_radius=5, 
                              command= lambda x: self._update_department(x))
        
        self.scheduler_canvas.create_window(200, 123, window=department_option, anchor="nw")

        year_option = ct.CTkComboBox(self.scheduler_canvas, width=240, state="readonly",
                                     variable=self.year_var)

        CTkScrollableDropdown(year_option, values=self.year_values, justify="left", 
                              button_color="#151515", fg_color="#151515",
                              hover_color=DARK_GRAY, frame_corner_radius=5,
                              command=lambda x: self._update_year(x))
        
        self.scheduler_canvas.create_window(200, 159, window=year_option, anchor="nw")
        self._update_courses()

        constraints = ["Lunch Break", "Dismissal Time", "PE Last Class", "Lab Last Class",
                       "Maximum Class", "Lab on the Same Day", "Non-Lab in Lab Day", "Free Day"]
        
        self.switch_var = [ct.StringVar(value="on") for _ in range(len(constraints))]

        for idx, constraint in enumerate(constraints):
            switch = ct.CTkSwitch(self.scheduler_canvas, text=constraint + " Constraint",
                                  variable=self.switch_var[idx], onvalue="on", offvalue="off")
            if idx < 4:
                self.scheduler_canvas.create_window(522, 122 + (idx * 26), window=switch, anchor="nw")
            else:
                self.scheduler_canvas.create_window(861, 122 + ((idx%4) * 26), window=switch, anchor="nw")

        # parameter_options = SegmentedButton(self.scheduler_canvas, width=525, height=28,
        #                                     values=["Balanced", "Accurate", "Experimental", "Chaos", "Custom"])
        # self.scheduler_canvas.create_window(522, 280, window=parameter_options, anchor="nw")

        self.scheduler_canvas.create_text(522, 278, anchor="nw", text="Mutation Rate:", fill="white", font=('Roboto 10'))
        self.scheduler_canvas.create_text(522, 300, anchor="nw", text="Population Size:", fill="white", font=('Roboto 10'))
        self.scheduler_canvas.create_text(522, 322, anchor="nw", text="Maximum Generations:", fill="white", font=('Roboto 10'))
        self.scheduler_canvas.create_text(522, 344, anchor="nw", text="Tournament Size:", fill="white", font=('Roboto 10'))
        
        mutrate_var = ct.StringVar(value="1.12%")
        mutrate_label = ct.CTkLabel(self.scheduler_canvas, fg_color="#151515",
                                    corner_radius=5, width=66, height=18,
                                    textvariable=mutrate_var,
                                    font=ct.CTkFont("Roboto", 12))
        
        mutrate_slider = ct.CTkSlider(self.scheduler_canvas, 
                                      from_=0, to=5, width=393, number_of_steps=200)
        mutrate_slider.set(1.12)
        mutrate_slider.configure(command= lambda x: mutrate_var.set(f"{round(x, 2)}%"))
        
        self.scheduler_canvas.create_window(780, 280, window=mutrate_slider, anchor="nw")
        
        self.scheduler_canvas.create_window(689, 278, window=mutrate_label, anchor="nw")

        popsize_var = ct.StringVar(value="2000")
        popsize_label = ct.CTkLabel(self.scheduler_canvas,
                                    textvariable=popsize_var, fg_color="#151515",
                                    corner_radius=5, width=66, height=18,
                                    font=ct.CTkFont("Roboto", 12))
        
        self.scheduler_canvas.create_window(689, 300, window=popsize_label, anchor="nw")
        
        popsize_slider = ct.CTkSlider(self.scheduler_canvas, 
                                      from_=50, to=5000, width=393, number_of_steps=99)
        popsize_slider.set(2000)
        popsize_slider.configure(command= lambda x: popsize_var.set(f"{int(x)}"))
        self.scheduler_canvas.create_window(780, 304, window=popsize_slider, anchor="nw")

        maxgen_var = ct.StringVar(value="50")
        maxgen_label = ct.CTkLabel(self.scheduler_canvas,
                                    textvariable=maxgen_var, fg_color="#151515",
                                    corner_radius=5, width=66, height=18,
                                    font=ct.CTkFont("Roboto", 12))
        
        self.scheduler_canvas.create_window(689, 322, window=maxgen_label, anchor="nw")

        maxgen_slider = ct.CTkSlider(self.scheduler_canvas, 
                                      from_=50, to=1000, width=393, number_of_steps=19)
        maxgen_slider.set(50)
        maxgen_slider.configure(command= lambda x: maxgen_var.set(f"{int(x)}"))
        self.scheduler_canvas.create_window(780, 326, window=maxgen_slider, anchor="nw")

        acc_conflict_var = ct.StringVar(value="5")
        acc_conflict_label = ct.CTkLabel(self.scheduler_canvas,
                                    textvariable=acc_conflict_var, fg_color="#151515",
                                    corner_radius=5, width=66, height=18,
                                    font=ct.CTkFont("Roboto", 12))
        
        self.scheduler_canvas.create_window(689, 344, window=acc_conflict_label, anchor="nw")

        acc_conflict_slider = ct.CTkSlider(self.scheduler_canvas, 
                                      from_=2, to=10, width=393, number_of_steps=10)
        acc_conflict_slider.set(5)
        acc_conflict_slider.configure(command= lambda x: acc_conflict_var.set(f"{int(x)}"))
        self.scheduler_canvas.create_window(780, 348, window=acc_conflict_slider, anchor="nw")

        # # progress bar
        # progress_bar = ct.CTkProgressBar(self.scheduler_canvas, orientation="horizontal",
        #                                  width=226, height=17, corner_radius=10)
        # self.scheduler_canvas.create_window(821, 438, window=progress_bar, anchor="nw")

        # start / stop btn
        control_btn = Button(self.scheduler_canvas, Button.PRIMARY,
                             None, None, width=220, height=44, text="START",
                            font=ct.CTkFont("Roboto", 20, "bold"),
                            command=lambda: self.start_algorithm(popsize_var, mutrate_var, maxgen_var, acc_conflict_var))
        
        self.scheduler_canvas.create_window(743, 499, window=control_btn, anchor="nw")

    def create_home(self):

        self.home = ct.CTkFrame(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, corner_radius=0, fg_color="black")

        self.home.grid_columnconfigure(0, weight=1)
        self.home.grid_rowconfigure(0, weight=1)
        self.home.grid(row=0, column=0, sticky="nsew")

        self.bg_image = tk.PhotoImage(file="assets\dna-bg-5.png")

        self.home_canvas = tk.Canvas(self.home, 
                                     width=SCREEN_WIDTH, 
                                     height=SCREEN_HEIGHT, 
                                     highlightthickness=0)
        self.home_canvas.place(x=0, y=-35)

        self.home_canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        self.home_canvas.create_text(SCREEN_WIDTH/2, 
                                     SCREEN_HEIGHT/2, 
                                     text="Automated Scheduling System",
                                     fill="white",
                                     font=('Montserrat 36'))
        self.home_canvas.create_text(SCREEN_WIDTH/2, 
                                     SCREEN_HEIGHT/2+40, 
                                     text="A university course scheduler application using Genetic Algorithm.",
                                     fill="gray",
                                     font=('Montserrat 12'))
        self.home_canvas.create_text(SCREEN_WIDTH/2, 80, 
                                     text="-- DESIGN AND ANALYSIS OF ALGORITHMS --",
                                     fill="gray",
                                     font=('Montserrat 10'))

        # MAIN BUTTONS
        buttons_frame = ct.CTkFrame(self.home_canvas, width=SCREEN_WIDTH, height=SCREEN_HEIGHT/4)
        buttons_frame.grid(row=2, column=0, padx=40, pady=40)
        buttons_frame.grid_rowconfigure((0, 1), weight=1)
        buttons_frame.grid_columnconfigure((0, 1), weight=1)

        self.home_canvas.create_window(SCREEN_WIDTH/2, 
                                       SCREEN_HEIGHT-(SCREEN_HEIGHT/8), 
                                       window=buttons_frame)

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

    def _update_department(self, choice):
        self.department_var.set(choice)
        self._update_courses(self.department_var.get(), self.year_var.get())

    def _update_year(self, choice):
        self.year_var.set(choice)
        self._update_courses(self.department_var.get(), self.year_var.get())

    def _truncate_text(self, text, max_len=40, ellipsis="..."):
        if len(text) > max_len:
            return text[:max_len - len(ellipsis)] + ellipsis
        return text

    def _update_courses(self, dept=None, yr=None):
        if dept == None:
            dept = self.department_var.get()
        if yr == None:
            yr = self.year_var.get()
        print(self.courses[dept][yr])
        courses = self.courses[dept][yr]
        
        for idx, course in enumerate(courses):
            course_label = ct.CTkLabel(self.scheduler_canvas,
                                       text=self._truncate_text(course), fg_color="#151515",
                                       corner_radius=5, width=330, height=41,
                                       font=ct.CTkFont("Roboto", 12))
            self.scheduler_canvas.create_window(123, 252+(idx*46),
                                                window=course_label, anchor="nw")

    def start_algorithm(self, popsize, mutrate, maxgen, acc_conflicts):
        print(popsize.get(), mutrate.get(), maxgen.get(), acc_conflicts.get())

        constraints_param = {
            '_lunch_break' : True, 
            '_dismissal' : True, 
            '_pe_last' : True,
            '_lab_last' : True, 
            '_maxclass' : True, 
            '_lab_sameday' : True, 
            '_nonlab_in_lab' : True, 
            '_free_day' : True
        }
        for idx, var in enumerate(self.switch_var):
            if var.get() == "off":
                constraints_param[list(constraints_param.keys())[idx]] = False
        print(constraints_param)
        genetic = Genetic(int(popsize.get()), float(mutrate.get()[:mutrate.get().index("%")])/100, 
                          int(maxgen.get()), int(acc_conflicts.get()), **constraints_param)
        optimal_solutions = genetic.start_world()
        if optimal_solutions != None:
            # print("".join(optimal_solution))
            self.show_schedule(optimal_solutions)
            self.show_frame(self.schedule_frame)

    def show_schedule(self, schedules):

        current_sched = 0

        def _show(idx):
            
            nonlocal current_sched

            if 5 >= idx >= 0:
                schedule = schedules[idx]
                current_sched = idx
            else:
                return

            title = ct.CTkLabel(self.schedule_frame, text=f"Schedule {idx+1}", font=ct.CTkFont("Roboto", 24, "bold"))
            title.grid(row=0, column=3, columnspan=1)

            timeslots = ["7:30 AM - 9:00 AM", "9:00 AM - 10:30 AM", "10:30 AM - 12:00 NN",
                        "12:00 NN - 1:30 PM", "1:30 PM - 3:00 PM", "3:00 PM - 4:30 PM",
                        "4:30 PM - 6:00 PM", "6:00 PM - 7:30 PM", "7:30 PM - 9:00 PM"]
            
            course_dict = {
                'A': 'Technical Documentation',
                'B': 'Art Appreciation',
                'C': "People and the Earth's Ecosystem",
                'D': 'CS Free Elective 2',
                'E': "Design and Analysis of Algorithms",
                'F': "Team Sports",
                'G': "Operating System (LEC)",
                'H': "Operating System (LAB)",
                'I': "Information Management (LEC)",
                'J': "Information Management (LAB)",
                '0': "None"
            }

            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

            for idx, _day in enumerate(days):
                _slot_label = ct.CTkLabel(self.schedule_frame, text=_day,
                                      font=ct.CTkFont("Roboto", 12, "bold"), 
                                      wraplength=100, justify="center", 
                                        fg_color=DARK_GRAY)
                _slot_label.grid(row=1, column=idx+1, sticky="nsew", padx=1, pady=1)

            for idx, _slot in enumerate(timeslots):
                _slot_label = ct.CTkLabel(self.schedule_frame, text=_slot,
                                        font=ct.CTkFont("Roboto", 10, "bold"), 
                                        justify="center", fg_color=DARK_GRAY)
                _slot_label.grid(row=idx+2, column=0, sticky="nsew", padx=1, pady=1)

            for idx, timeslot in enumerate(schedule):
                if timeslot != "1":
                    if timeslot == "0":
                        txt_color = "gray"
                    else:
                        txt_color = "white"
                    timeslot = ct.CTkLabel(self.schedule_frame, text=course_dict[timeslot], text_color=txt_color,
                                        font=ct.CTkFont("Roboto", 12), wraplength=100, justify="center", fg_color="#151515")
                    timeslot.grid(row=idx%10+2, column=idx//10+1, sticky="nsew", padx=1, pady=1)
            
        self.schedule_frame = ct.CTkFrame(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, corner_radius=0, fg_color="black")

        self.schedule_frame.grid(row=0, column=0, sticky="nsew", ipadx=5, ipady=5)
        self.schedule_frame.rowconfigure(list(range(11)), weight=1)
        self.schedule_frame.columnconfigure(list(range(7)), weight=1)

        self.arrow_left = tk.PhotoImage(file="assets/arrow-left.png")
        arrow_left_btn = ct.CTkButton(self.schedule_frame, text=">", command=lambda : _show(current_sched+1))
        arrow_left_btn.grid(row=0, column=4)
        arrow_right_btn = ct.CTkButton(self.schedule_frame, text="<", command=lambda : _show(current_sched-1))
        arrow_right_btn.grid(row=0, column=2)
        _show(0)

app = App()
app.eval('tk::PlaceWindow . center')
app.mainloop()