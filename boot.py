# This file is executed on every boot (including wake-boot from deepsleep)
import wificonnect
import webrepl

wificonnect.do_connect()
# import esp
# esp.osdebug(None)

# webrepl.start()
