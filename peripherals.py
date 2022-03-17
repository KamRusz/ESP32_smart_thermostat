import ssd1306
from machine import Pin, I2C, Timer
import gfx
import settings
import dht12
import time
import json
import neopixel
from servo import Servo

##############################################
#Obj initialization

i2c = I2C(scl=Pin(settings.SCL_PIN), sda=Pin(settings.SDA_PIN))
oled = ssd1306.SSD1306_I2C(settings.OLED_WIDTH, settings.OLED_HEIGHT, i2c)
graphics = gfx.GFX(settings.OLED_WIDTH, settings.OLED_HEIGHT, oled.pixel)
sensor = dht12.DHT12(i2c)
servo = Servo(Pin(settings.SERVO_PIN))
time.sleep_ms(100)
servo.write_us(0)
relay=Pin(settings.RELAY_PIN, Pin.OUT)
neo = neopixel.NeoPixel(Pin(settings.NEO_PIN), 1)
tim0 = Timer(0)
tim1 = Timer(1)
tim2 = Timer(2)
tim3 = Timer(3)
button_pos = Pin(settings.BUT_ADD_PIN, Pin.IN, Pin.PULL_UP)
button_neg = Pin(settings.BUT_SUB_PIN, Pin.IN, Pin.PULL_UP)

##############################################

def measurement_onetime():
    global room_temp, room_humi
    print("pomiar initial")
    sensor.measure()
    room_temp = sensor.temperature()
    room_humi = sensor.humidity()
    
measurement_onetime()

def backup_load():
    global backup
    with open("backup.json", "r") as f:
        backup = json.load(f)   
    return backup

def backup_save():
    with open("backup.json", "w") as f:
        json.dump(backup, f)
        
def relay_check():
    global room_temp
    print("relay check temp =",room_temp, "target_temp =", backup["target_temp"]) 
    if room_temp+settings.HYSTERESIS<backup["target_temp"]:
        relay.on()
    elif room_temp>backup["target_temp"]+settings.HYSTERESIS/2:
        relay.off()        

def  fluent_servo(target_angle):
    global backup
    current_angle = int(backup["servo_angle"])
    print("target angle = ",target_angle, "current angle = ",current_angle)
    if target_angle==current_angle:
        return
    if target_angle<current_angle:
        pitch=-1
    else:
        pitch=1
    for i in range(current_angle,target_angle+pitch,pitch):
        servo.write_angle(i)
        #neo[0]=(i,180-i,0)
        #neo.write()        
        time.sleep_ms(60)
    #neo[0]=(0,0,0)
    #neo.write()  
    backup["servo_angle"]=target_angle
    servo.write_us(0)
    backup_save()
    
def set_servo(tim2):
    global backup
    angle = settings.TEMP_ALIGN[str(backup["target_temp"])]
    fluent_servo(angle)
    
def debounce(pin):
    prev = None
    for _ in range(32):
        current_value = pin.value()
        if prev != None and prev != current_value:
            return None
        prev = current_value
    return prev

def user_override_pos(pin):
    global backup, room_temp, room_humi
    tim0.init(period=settings.SCR_OFF_TIME, mode=Timer.ONE_SHOT, callback=screen.oled_off)
    tim2.init(period=settings.SERVO_SET_DELAY, mode=Timer.ONE_SHOT, callback=set_servo)
    tim1.deinit()
    d = debounce(pin)
    if d == None:
        return
    elif not d:
        if Screen.screen_on==False:
            print("screen on")
            screen.main_gui(backup, room_temp, room_humi)
            Screen.screen_on=True
        else:
            if backup["target_temp"]<=25:
                backup["target_temp"]+=1
            #print(backup["target_temp"])
            screen.main_gui(backup, room_temp, room_humi)
            user_temp = backup["target_temp"]
            relay_check()
            time.sleep_ms(100)
    #tim1.init(period=5000, mode=Timer.PERIODIC, callback=measurement)
    #response = urequests.get(f"https://esp32-smart-thermostat.herokuapp.com/helloget?api=123456789&temp={room_temp}&humi={room_humi}&user_temp={user_temp}")
    #response = urequests.post(f"https://esp32-smart-thermostat.herokuapp.com/helloget?api=123456789&temp={room_temp}&humi={room_humi}&user_temp={user_temp}")

def user_override_neg(pin):
    global backup, room_temp, room_humi, relay
    tim0.init(period=settings.SCR_OFF_TIME, mode=Timer.ONE_SHOT, callback=screen.oled_off)
    tim2.init(period=settings.SERVO_SET_DELAY, mode=Timer.ONE_SHOT, callback=set_servo)
    tim1.deinit()
    d = debounce(pin)
    if d == None:
        return
    elif not d:
        if Screen.screen_on==False:
            print("screen on")
            screen.main_gui(backup, room_temp, room_humi)
            Screen.screen_on=True
        else:
            if backup["target_temp"]>=15:
                backup["target_temp"]-=1
            #print(backup["target_temp"])
            screen.main_gui(backup, room_temp, room_humi)
            user_temp = backup["target_temp"]
            relay_check()
            time.sleep_ms(100)
    #tim1.init(period=5000, mode=Timer.PERIODIC, callback=measurement)
    #response = urequests.get(f"https://esp32-smart-thermostat.herokuapp.com/helloget?api=123456789&temp={room_temp}&humi={room_humi}&user_temp={user_temp}")


class Screen():
    TEMP = [
    [0,0,1,1,0,0,1,0,1,1,1,1],
    [0,1,0,0,1,0,0,0,1,0,0,0],
    [0,1,0,0,1,0,0,0,1,0,0,0],
    [0,1,0,0,1,0,0,0,1,0,0,0],
    [0,1,0,0,1,0,0,0,1,1,1,1],
    [0,1,0,0,1,0,0,0,0,0,0,0],
    [0,1,0,0,1,0,0,0,0,0,0,0],
    [0,1,0,0,1,0,0,0,0,0,0,0],
    [1,0,0,0,0,1,0,0,0,0,0,0],
    [1,0,0,0,0,1,0,0,0,0,0,0],
    [0,1,1,1,1,0,0,0,0,0,0,0],
            ]
    HUMI = [
    [0,0,0,1,0,0,0],
    [0,0,1,1,1,0,0],
    [0,0,1,1,1,0,0],
    [0,1,1,1,1,1,0],
    [0,1,1,1,1,1,0],
    [1,0,0,1,1,0,1],
    [1,0,0,1,0,1,1],
    [1,1,1,0,1,1,1],
    [1,1,0,1,0,0,1],
    [1,0,1,1,0,0,1],
    [0,1,1,1,1,1,0],
            ]
    screen_on=False
    
    def __init__(self, oled):
        self.oled = oled
        
    def off(self):
        self.oled.fill(0)
        oled.show()
        
    def oled_off(self, tim0):
        oled.fill(0)
        print("screen_off")
        Screen.screen_on=False
        oled.show()
        
    def on(self):
        self.oled.fill(1)
        oled.show()
        
    def main_gui(self, backup, t, h):
        oled.fill(0)
        graphics.rect(0,0,128,20,1)
        graphics.rect(0,20,65,44,1)
        graphics.rect(64,20,64,44,1)
        graphics.circle(106,29,2,1)
        for y, row in enumerate(Screen.TEMP):
           for x, c in enumerate(row):
               oled.pixel(x+47, y+26, c)
        for y, row in enumerate(Screen.HUMI):
            for x, c in enumerate(row):
                oled.pixel(x+47, y+46, c)
        oled.text("zadana temp:", 3, 5)
        if backup["target_temp"] == 14:
            oled.text("min", 102, 5)
        elif backup["target_temp"] == 26:
            oled.text("max", 102, 5)
        else:
            oled.text(f"{backup["target_temp"]}", 102, 5)
        oled.text(f"temp", 6, 28)
        oled.text(f"{t} C", 71, 28)
        oled.text(f"wilg", 6, 48)
        oled.text(f"{h}%", 71, 48)
        oled.show()
          
screen = Screen(oled) 

        
        
        