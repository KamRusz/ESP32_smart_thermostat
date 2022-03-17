from machine import Pin, PWM, Timer
import urequests
import time
import json
from peripherals import Screen, oled, sensor, backup_load, neo, set_servo, user_override_pos, user_override_neg, button_pos, button_neg, screen, room_temp, room_humi, relay_check, tim0, tim1, tim2, tim3
from wificonnect import api_key
import micropython
import settings
micropython.alloc_emergency_exception_buf(100)
     
backup = backup_load()

'''
tim0 = Timer(0)
tim1 = Timer(1)
tim2 = Timer(2)
tim3 = Timer(3)


def relay_check():
    print("relay check temp =",room_temp, "target_temp =", backup["target_temp"]) 
    if room_temp+settings.HYSTERESIS<backup["target_temp"]:
        relay.on()
    elif room_temp>backup["target_temp"]+settings.HYSTERESIS/2:
        relay.off()
      
def measurement(tim1):
    global backup, room_temp, room_humi, relay
    print("pomiar")
    sensor.measure()
    room_temp = sensor.temperature()
    room_humi = sensor.humidity()
    relay_check()

time.sleep(1)
measurement(tim1)

#tim1.init(period=settings.SENSOR_DELAY, mode=Timer.PERIODIC, callback=temp2)


def hello1():
    #global backup
    response = urequests.get(f"https://esp32-smart-thermostat.herokuapp.com/helloget?api=123456789&temp={room_temp}&humi={room_humi}&user_temp=0")
    print(response.text)
    x= int(response.json()["target_temp"])
    backup["target_temp"] = x
    angle = settings.TEMP_ALIGN[str(x)]
    fluent_servo(angle)
'''
       
def hello():
    global room_temp, room_humi
    URL = "https://esp32-smart-thermostat.herokuapp.com/hello"
    params = {
        "api_key":api_key,
        "room_temp":room_temp,
        "room_humi":room_humi,
        "user_temp":0
        }
    print(params)
    res = urequests.request("POST", URL, json = params)
    print(res.text)
    backup["target_temp"] = int(res.json()["target_temp"])
    tim2.init(period=settings.SERVO_SET_DELAY, mode=Timer.ONE_SHOT, callback=set_servo)

'''
neo[i] = (0, 0, 0)
neo.write()
'''
'''
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
'''            
        
#button_pos = Pin(settings.BUT_ADD_PIN, Pin.IN, Pin.PULL_UP)
#button_neg = Pin(settings.BUT_SUB_PIN, Pin.IN, Pin.PULL_UP)
button_pos.irq(trigger=Pin.IRQ_FALLING, handler=user_override_pos)
button_neg.irq(trigger=Pin.IRQ_FALLING, handler=user_override_neg)

