try:
    from pygame import mixer
    import os, sys
    import random
    import RPi.GPIO as GPIO
    import time
    from rpi_lcd import LCD

    LONGCLICKDURATION = 1
    DOUBLECLICKINTERVAL = 0.25
    bluetooth_address = "38:88:A4:DD:5C:63"
    lcd = LCD(rows = 2, address=0x27, width=16, backlight=True)
    lcd.clear()
    class screen:
        tstart = 0
        sstart = -1
        n = 0
        line1 = None
        line2 = None
        timer = -1
        def __init__(self, interval=0.5) -> None:
            self.interval = interval
        def l1(self,txt):
            self.line1 = txt
            self.n = 0
            if len(self.line1) > 16:
                self.line1 += ' '*8
                self.sstart = time.time()
                lcd.text((self.line1*2)[:16],1)
            else:
                lcd.text(f"{txt:<16}",1)
        def l2(self,txt,seconds):
            self.line2 = f"{txt:<16}"
            if seconds != -1:
                self.tstart = time.time()
                self.timer = seconds
            lcd.text(self.line2, 2)
        def reflesh(self):
            if self.timer != -1 and time.time()-self.tstart >= self.timer:
                self.timer = -1
                lcd.text(" "*16, 2)
            if len(self.line1) > 16 and time.time()-self.sstart >= self.interval:
                self.sstart = time.time()
                self.n = (self.n+1)%len(self.line1)
                lcd.text((self.line1*2)[self.n:self.n+16], 1)
        
        def backlight(self):
            lcd.backlight(not(lcd.backlight_status))

    '''class screen2:
        dev = []
        dev_id = []
        pointer = 0
        def devices(self):
            lcd.clear()
            lcd.text("Scanning BT dev", 1)
            os.system("bluetoothctl power off")
            time.sleep(0.5)
            os.system("bluetoothctl power on")
            time.sleep(0.5)
            nearby_devices = bluetooth.discover_devices(duration=15, lookup_names=True,
                                                flush_cache=True, lookup_class=False)
            self.pointer = 0
            #x = os.system(f"bluetoothctl paired-devices")
            #x = list(x.split())
            self.dev = []
            self.dev_id = []
            for addr, name in nearby_devices:
                self.dev.append(name)
                self.dev_id.append(addr)
            if len(self.dev) > 0:
                lcd.text(f"1.{self.dev[0]:<16}"[:16], 1)
            else:
                lcd.text(f"No BT devices", 1)
        def previous(self):
            if len(self.dev) > 0:
                self.pointer = (self.pointer-1)%len(self.dev)
                lcd.text(f"{self.pointer+1}.{self.dev[self.pointer]:<16}"[:16], 1)
        def next(self):
            if len(self.dev) > 0:
                self.pointer = (self.pointer+1)%len(self.dev)
                lcd.text(f"{self.pointer+1}.{self.dev[self.pointer]:<16}"[:16], 1)
        def choose(self):
            
            if len(self.dev) > 0:
                global bluetooth_address
                os.system("bluetoothctl scan on")
                os.system("^Z")
                time.sleep(8)
                os.system(f"bluetoothctl disconnect {bluetooth_address}")
                bluetooth_address = self.dev_id[self.pointer]
                os.system(f"bluetoothctl trust {bluetooth_address}")
                os.system(f"bluetoothctl pair {bluetooth_address}")
                time.sleep(1)
                os.system(f"bluetoothctl connect {bluetooth_address}")
                os.system(f"bluetoothctl exit")'''
    '''def sprint(txt):
        lcd.clear()
        lcd.return_home()
        lcd.write(txt)
    def print_horizontal_line():
        term_size = os.get_terminal_size()
        print('-' * term_size.columns)
    '''
    scrn = screen()
    #scrn2 = screen2()
    class music():
        list = []
        recent = 0
        paused = False
        volume = 100
        times = 1
        
        def __init__(self, dir: str="/home/shing/mp3player/music", loop: bool=True) -> None:
            self.dir = dir
            self.loop = loop
            mixer.init()
            mixer.music.set_volume(self.volume/100*self.times)
        def load(self):
            self.list = []
            mixer.music.stop()
            self.list.extend(list(os.listdir(self.dir)))
            self.list.sort()
            self.recent = random.randint(0, len(self.list)-1)
            #print(f"Loaded {len(self.list)} songs...")
            #print_horizontal_line()
            #sprint(f"Loaded {len(self.list)}")
            #time.sleep(1)
            scrn.l2(f"Loaded {len(self.list)} songs", 1)
        def shuffle(self):
            n = self.list[self.recent]
            self.list.pop(self.recent)
            random.shuffle(self.list)
            self.list.insert(0,n)
            self.recent = 0
            #print("Shuffled.")
            #for i in range(len(self.list)):
            #    print(f"{i+1}. {self.list[i]}")
            #print_horizontal_line()
            '''sprint(f"Shuffled")
            time.sleep(1)
            sprint(self.list[self.recent][:-4])'''
            scrn.l2("Shuffled", 1)
            
        def start(self):
            mixer.music.load(f"{self.dir}/{self.list[self.recent]}")
            mixer.music.play()
            #print(f"Now playing {self.list[self.recent]}.")
            #print_horizontal_line()
            #sprint(self.list[self.recent][:-4])
            scrn.l1(self.list[self.recent][:-4])
        def play_next(self):
            self.recent = (self.recent + self.loop) % len(self.list)
            mixer.music.load(f"{self.dir}/{self.list[self.recent]}")
            mixer.music.play()
            #print(f"Now playing {self.list[self.recent]}.")
            #print_horizontal_line()
            #sprint(self.list[self.recent][:-4])
            scrn.l1(self.list[self.recent][:-4])
        def next(self):
            if self.paused:
                self.pause()
            self.recent = (self.recent + 1) % len(self.list)
            mixer.music.load(f"{self.dir}/{self.list[self.recent]}")
            mixer.music.play()
            #print("Next.")
            #print(f"Now playing {self.list[self.recent]}.")
            #print_horizontal_line()
            #sprint(self.list[self.recent][:-4])
            scrn.l1(self.list[self.recent][:-4])
        
        def previous(self):
            if self.paused:
                self.pause()
            self.recent = (self.recent - 1) % len(self.list)
            mixer.music.load(f"{self.dir}/{self.list[self.recent]}")
            mixer.music.play()
            #print("Previous.")
            #print(f"Now playing {self.list[self.recent]}.")
            #print_horizontal_line()
            #sprint(self.list[self.recent][:-4])
            scrn.l1(self.list[self.recent][:-4])
        
        def pause(self):
            if self.paused:
                mixer.music.unpause()
                #print("Unpaused.")
                #sprint(self.list[self.recent][:-4])
                lcd.text(' '*16,2)
                
            else:
                mixer.music.pause()
                scrn.l2("Pause", -1)
                #print("Paused.")
                #sprint("Paused")
            self.paused = not(self.paused)
        def volume_up(self):
            self.volume = min(100,self.volume+5)
            mixer.music.set_volume(self.volume/100*self.times)
            #print(f"Volume: {self.volume}")
            #print_horizontal_line()
            scrn.l2(f"Volume: {self.volume}%", 1)
        def volume_down(self):
            self.volume = max(0,self.volume-5)
            mixer.music.set_volume(self.volume/100*self.times)
            #print(f"Volume: {self.volume}")
            #print_horizontal_line()
            scrn.l2(f"Volume: {self.volume}%", 1)
        def reconnect_bluetooth(self,ID=bluetooth_address):
            i = not(self.paused)
            if i:
                self.pause()
                scrn.l2(f"Connecting to BT", -1)
            try:
                os.system(f"bluetoothctl disconnect {ID}")
                os.system(f"bluetoothctl connect {ID}")
            except Exception as exc:
                print(exc)
            if i:
                #time.sleep(1)
                self.pause()
            else:
                #print_horizontal_line()
                scrn.l2(f"Pause", -1)
    # Set the Row Pins
    ROW = [23,24,25,12]
    GPIO.setwarnings(False)
    # BCM numbering
    GPIO.setmode(GPIO.BCM)
    # Set Row pins as output
    for i in ROW:
        GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    class button():
        timer1 = [-1]*len(ROW)
        timer2 = [-1]*len(ROW)
        last_click = [0]*len(ROW)
        click = [0]*len(ROW)
        button_event = [0]*len(ROW)
        def __init__(self):
            pass
        def reflesh(self):
            self.last_click = self.click[:]
            self.click = [0]*len(ROW)
            self.button_event = [0]*len(ROW)
            for i in range(4):
                for j in range(len(ROW)):
                    self.click[j] += (GPIO.input(ROW[j])==GPIO.HIGH)
            
            for i in range(len(ROW)):
                if self.click[i] == 4:
                    self.click[i] = 1
                elif self.click[i] == 0:
                    self.click[i] = 0
                else:
                    self.click[i] = self.last_click[i]
                
                if self.timer1[i] == -1:
                    if self.timer2[i] == -1:
                        if self.click[i] and not(self.last_click[i]):
                            self.timer1[i] = time.time()
                    elif time.time() - self.timer2[i] <= DOUBLECLICKINTERVAL:
                        if self.click[i] and not(self.last_click[i]):
                            self.timer1[i] = time.time()
                    else:
                        self.button_event[i] = 1
                        self.timer1[i] = -1
                        self.timer2[i] = -1
                elif time.time() - self.timer1[i] < LONGCLICKDURATION:
                    if self.timer2[i] == -1:
                        if not(self.click[i]) and self.last_click[i]:
                            self.timer1[i] = -1
                            self.timer2[i] = time.time()
                    elif time.time() - self.timer2[i] <= DOUBLECLICKINTERVAL:
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
                
    #def main():
    music2 = music(loop=True)
    bt = button()
    music2.load()
    time.sleep(1)
    music2.start()
    mode = True
    while True:
        bt.reflesh()
        #if mode:
        if not(mixer.music.get_busy()) and not(music2.paused):
            music2.play_next()
        if bt.button_event[0] == 1:
            music2.volume_down()
        elif bt.button_event[0] == 2:
            music2.previous()
        elif bt.button_event[0] == 3:
            os.system("sudo shutdown -h now")
        if bt.button_event[1] == 1:
            music2.pause()
        elif bt.button_event[1] == 2:
            music2.shuffle()
        elif bt.button_event[1] == 3:
            music2.load()
        if bt.button_event[2] == 1:
            music2.volume_up()
        elif bt.button_event[2] == 2:
            music2.next()
        elif bt.button_event[2] == 3:
            pass
        if bt.button_event[3] == 1:
            music2.reconnect_bluetooth()
        elif bt.button_event[3] == 2:
            scrn.backlight()
            '''mode = False
            flag = True
            if music2.paused == False:
                music2.pause()
            lcd.clear()'''
            
        elif bt.button_event[3] == 3:
            scrn.backlight()
            exit()
        
        scrn.reflesh()
        '''else:
            if flag:
                
                scrn2.devices()
                flag = False
            if bt.button_event[0] == 1:
                scrn2.previous()
            elif bt.button_event[0] == 3:
                scrn.backlight()
            if bt.button_event[1] == 1:
                scrn2.choose()
                print("Hello World")
                mode = True
            if bt.button_event[2] == 1:
                scrn2.next()
            if bt.button_event[3] == 1:
                flag = True
            elif bt.button_event[3] == 3:
                scrn.backlight()
                exit()'''
except Exception as e:
    with open("text.txt","w") as txt:
        txt.write(str(e))