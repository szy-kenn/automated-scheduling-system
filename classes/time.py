class time:

    def __init__(self, str_time: str) -> None:
        # 10:30
        self.hour = int(str_time[:2])
        self.minute = int(str_time[3:5])
        self.period = str_time [6:]
        self.fulltime = str_time


    