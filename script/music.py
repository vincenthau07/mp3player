import os, random
from screen import screen
from audioplayer import AudioPlayer
from mutagen.mp3 import MP3
from time import time

class music():
    
    def __init__(self, dir: str="/home/shing/mp3player/music", loop: bool=True, volume: int=100, times: float = 1, bluetooth_address="38:88:A4:DD:5C:63") -> None:

        self.audiofile = None
        self.volume = volume
        self.bluetooth_address = bluetooth_address
        self.scrn = screen()
        self.playlist = []
        self.paused = False
        self.dir = dir
        self.loop = loop
        self.times = times
        self.load()

    def load(self):
        self.playlist = []
        if self.audiofile is not None:
            self.audiofile.pause()
        self.playlist.extend(list(os.listdir(self.dir)))
        self.playlist.sort()
        self.recent = random.randint(0, len(self.playlist)-1)
        self.scrn.lines[1].text(f"Loaded {len(self.playlist)} songs", 1)

    def shuffle(self):
        n = self.playlist[self.recent]
        self.playlist.pop(self.recent)
        random.shuffle(self.playlist)
        self.playlist.insert(0,n)
        self.recent = 0
        self.scrn.lines[1].text("Shuffled", 1)


    def play(self):
        if self.audiofile is not None:
            self.audiofile.stop()
        self.audiofile = AudioPlayer(f"{self.dir}/{self.playlist[self.recent]}")
        self.audioDuration = MP3(self.audiofile.filename).info.length+0.05
        self.audioStart = time()
        self.audiofile.volume = self.volume
        self.audiofile.play()
        self.scrn.lines[0].text(self.playlist[self.recent][:-4])

    def play_next(self):
        self.recent = (self.recent + self.loop) % len(self.playlist)
        self.play()

    def next(self):
        self.recent = (self.recent + 1) % len(self.list)
        self.play()
    
    def previous(self):
        self.recent = (self.recent - 1) % len(self.list)
        self.play()
    
    def pause(self):
        if self.paused:
            self.audiofile.resume()
            self.scrn.lines[1].text("",2)
            
        else:
            self.audiofile.pause()
            self.scrn.lines[1].text("Pause")
        self.paused = not(self.paused)
    def volume_up(self):
        self.volume = min(100,self.volume+5)
        self.audiofile.volume = self.volume
        self.scrn.lines[1].text(f"Volume: {self.volume}%", 1)
    def volume_down(self):
        self.volume = max(0,self.volume-5)
        self.audiofile.volume = self.volume
        #print(f"Volume: {self.volume}")
        #print_horizontal_line()
        self.scrn.lines[1].text(f"Volume: {self.volume}%", 1)
    def reconnect_bluetooth(self):
        i = not(self.paused)
        if i:
            self.pause()
            self.scrn.lines[1].text(f"Connecting to BT")
        try:
            os.system(f"bluetoothctl disconnect {self.bluetooth_address}")
            os.system(f"bluetoothctl connect {self.bluetooth_address}")
        except Exception as exc:
            print(exc)
        if i:
            #time.sleep(1)
            self.pause()
        else:
            #print_horizontal_line()
            self.scrn.lines[1].text(f"Pause")
    def get_busy(self):
        return time()-self.audioStart <= self.audioDuration