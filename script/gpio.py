from time import time
import RPi.GPIO as GPIO

class button():

    def __init__(self, ROW = [23,24,25,12], LONGCLICKDURATION = 1, DOUBLECLICKINTERVAL = 0.25):
        self.ROW = ROW
        self.timer1 = [-1]*len(self.ROW)
        self.timer2 = [-1]*len(self.ROW)
        self.last_click = [0]*len(self.ROW)
        self.click = [0]*len(self.ROW)
        self.button_event = [0]*len(self.ROW)
        self.LONGCLICKDURATION = LONGCLICKDURATION
        self.DOUBLECLICKINTERVAL = DOUBLECLICKINTERVAL
        
        GPIO.setwarnings(False)
        # BCM numbering
        GPIO.setmode(GPIO.BCM)
        # Set Row pins as output
        for i in ROW:
            GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def update(self):
        self.last_click = self.click[:]
        self.click = [0]*len(self.ROW)
        self.button_event = [0]*len(self.ROW)
        for i in range(4):
            for j in range(len(self.ROW)):
                self.click[j] += (GPIO.input(self.ROW[j])==GPIO.HIGH)
        
        for i in range(len(self.ROW)):
            if self.click[i] == 4:
                self.click[i] = 1
            elif self.click[i] == 0:
                self.click[i] = 0
            else:
                self.click[i] = self.last_click[i]
            
            if self.timer1[i] == -1:
                if self.timer2[i] == -1:
                    if self.click[i] and not(self.last_click[i]):
                        self.timer1[i] = time()
                elif time() - self.timer2[i] <= self.DOUBLECLICKINTERVAL:
                    if self.click[i] and not(self.last_click[i]):
                        self.timer1[i] = time()
                else:
                    self.button_event[i] = 1
                    self.timer1[i] = -1
                    self.timer2[i] = -1
            elif time() - self.timer1[i] < self.LONGCLICKDURATION:
                if self.timer2[i] == -1:
                    if not(self.click[i]) and self.last_click[i]:
                        self.timer1[i] = -1
                        self.timer2[i] = time()
                elif time() - self.timer2[i] <= self.DOUBLECLICKINTERVAL:
                    if not(self.click[i]) and self.last_click[i]:
                        self.button_event[i] = 2
                        self.timer1[i] = -1
                        self.timer2[i] = -1
                else:
                    self.timer2[i] = -1
            else:
                self.button_event[i] = 3
                self.timer1[i] = -1
                self.timer2[i] = -1