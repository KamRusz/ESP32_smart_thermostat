from machine import Pin
import micropython
from peripherals import (
    backup_load,
    user_override_pos,
    user_override_neg,
    button_pos,
    button_neg,
    )

micropython.alloc_emergency_exception_buf(100)

backup = backup_load()

button_pos.irq(trigger=Pin.IRQ_FALLING, handler=user_override_pos)
button_neg.irq(trigger=Pin.IRQ_FALLING, handler=user_override_neg)
