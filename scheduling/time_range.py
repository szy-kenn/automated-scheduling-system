from .functions import *
from datetime import time

class TimeRange:
    def __init__(self, start_time: time, end_time: time) -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.size = (time_to_sec(self.end_time) - time_to_sec(self.start_time))    # in seconds

    def get_size(self, unit: str='seconds'):
        match unit:
            case 'seconds':
                return self.size
            case 'minutes':
                return self.size / 60
            case 'hours':
                return self.size / 3600

    def __repr__(self) -> str:
        return f"{self.start_time.strftime('%H:%M:%S')} - {self.end_time.strftime('%H:%M:%S')}"