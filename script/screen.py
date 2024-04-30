from rpi_lcd import LCD
from time import time

class line():

    def text(self,context,duration: float=-1) -> None:
        self.context = context
        self.timer = time()
        self.pointer = 0
        self.duration = duration
        if duration >= 0:
            self.timer2 = time()

    def __init__(self,lcd, line: int, context: str='', interval: float=0.5, mode: bool = True) -> None:
        self.lcd = lcd
        self.line = line
        self.mode = mode
        self.timer = time()
        self.interval = interval
        self.text(context)
    
    def display(self) -> None:
        if self.duration >= 0 and time()-self.timer2 >= self.duration:
            self.text('')
        if self.mode and len(self.context)>16:
            if time() >= self.timer + self.interval:
                self.pointer += 1
                if self.pointer >= len(self.context)+8:
                    pointer = 0
            temp = (self.context+" "*8)*2
            self.lcd.text(temp[pointer:pointer+16], line)
        else:
            self.lcd.text(f"{self.context:<16}", line)

class screen:

    def __init__(self, interval=0.5, rows: int=2, address: int=0x27, width: int=16, blacklight: bool=True) -> None:
        self.interval = interval
        self.lcd = LCD(rows = rows, address=address, width=width, backlight=blacklight)
        self.lcd.clear()
        self.lines = [line(self.lcd,i) for i in range(1,rows+1)]

    def update(self) -> None:
        self.lines[0].display()
        self.lines[1].display()

    def backlight(self, mode=None) -> None:
        if mode is None:
            self.lcd.backlight(not(self.lcd.backlight_status))
        else:
            self.lcd.backlight(mode)