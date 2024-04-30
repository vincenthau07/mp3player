from script.music import music
from script.gpio import button
import time, os

#def main():
music2 = music(loop=True)
bt = button()
time.sleep(1)
mode = True
while True:
    bt.reflesh()
    #if mode:
    if not(music2.get_busy()) and not(music2.paused):
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
        music2.scrn.backlight()
        '''mode = False
        flag = True
        if music2.paused == False:
            music2.pause()
        lcd.clear()'''
        
    elif bt.button_event[3] == 3:
        music2.scrn.backlight()
        exit()
    
    music2.scrn.update()