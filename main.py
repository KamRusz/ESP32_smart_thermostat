import micropython
from machine import Pin

import settings
from peripherals import (backup_load, button_neg, button_pos,
                         user_override_neg, user_override_pos)

micropython.alloc_emergency_exception_buf(settings.EM_BUFF)

backup = backup_load()

button_pos.irq(trigger=Pin.IRQ_FALLING, handler=user_override_pos)
button_neg.irq(trigger=Pin.IRQ_FALLING, handler=user_override_neg)
