from yeelight import *

class BulbManager:
    def __init__(self):
        self.ip = ['192.168.0.129']
        self.bulbs = []
        for i in self.ip:
            self.bulbs.append(Bulb(i))
    
    def normalLight(self):
        try:
            for i in self.bulbs:
                i.set_color_temp(3000)
                i.set_brightness(18)
        except:
            print('There was a problem with setting the bulbs!')
    
    def activeLight(self):
        try:
            for i in self.bulbs:
                i.set_rgb(184, 89, 247)
                i.set_brightness(18)
        except:
            print('There was a problem with setting the bulbs!')
            