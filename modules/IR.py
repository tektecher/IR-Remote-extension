from machine import Pin
from time import ticks_us
from time import ticks_diff

timeStart = -1
data = 0
dataBitIndex = 0
irQueue = [ ]
pin = None
pinIR = None

def onIRPinChange(p):
    global timeStart, data, dataBitIndex, irQueue
    if p.value() == 1:
        t = ticks_diff(ticks_us(), timeStart)
        if t > 2000 and t < 3000: # start signal
            data = 0
            dataBitIndex = 0
        else:
            data |= (1 if t > 1000 and t < 2000 else 0) << dataBitIndex
            dataBitIndex = dataBitIndex + 1
            if dataBitIndex == 12:
                irQueue.append(data)
    else:
        timeStart = ticks_us()

def read(p):
    global irQueue, pin, pinIR
    if p != pin:
        if pinIR:
            del pinIR
        pinIR = Pin(p, Pin.IN, Pin.PULL_UP)
        pinIR.irq(onIRPinChange, Pin.IRQ_FALLING|Pin.IRQ_RISING)
        p = pin
    if len(irQueue):
        data = irQueue[0]
        irQueue = irQueue[1:]
        return data
    else:
        return -1
