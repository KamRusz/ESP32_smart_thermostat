import json
import time
import network

def do_connect():
    global api_key
    with open("credentials.json", "r") as f:     
        cred = json.load(f)
        api_key=cred["api_key"]
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(cred["ssid"], cred["passwd"])
        while not wlan.isconnected():
            time.sleep_ms(1000)
    print('network config:', wlan.ifconfig())