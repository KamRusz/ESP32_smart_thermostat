TEMP_ALIGN = {
    14: 180,
    15: 165,
    16: 150,
    17: 135,
    18: 120,
    19: 105,
    20: 90,
    21: 75,
    22: 60,
    23: 45,
    24: 30,
    25: 15,
    26: 0,
    }      # Map of "temperature scale":"servo angles" on existing thermostat

SCR_OFF_TIME = 15000      # in ms timer0 - delay to turn screen off
SENSOR_DELAY = 300000     # in ms timer1 - delay between measurements (T/H)
SERVO_SET_DELAY = 1000   # in ms timer2 - delay before servo engage
HYSTERESIS = 1  # in C degrees default 1 C degree - for preserving relays life
EM_BUFF = 100   # buffer for key innterrupt
DB_CYCLE = 32   # how many cycles to debounce button
BACKUP_PATH = "backup.json"  # path to initial backup file
USER_TEMP_URL = "https://esp32thermo.herokuapp.com/usertemp"  # Path to heroku API - overwriting target temp
TEMP_REQ_URL = "https://esp32thermo.herokuapp.com/humitemp"   # Path to heroku API - sending data
SEND_REQ_DEL = 1000  # seconds to delay sending master request

# Pin settings
OLED_WIDTH = 128         # oled width in pixels
OLED_HEIGHT = 64         # oled height in pixels
SCL_PIN = 22
SDA_PIN = 21
SERVO_PIN = 16
RELAY_PIN = 17
NEO_PIN = 15
BUT_ADD_PIN = 19
BUT_SUB_PIN = 18

# DEBUG
DEBUG = True
