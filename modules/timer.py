import time
import modules.globals

def timer(sec):
    globals.timerrunning = True
    globals.timer = sec
    while globals.timer > 0:
        #print(globals.timer)
        time.sleep(1)
        globals.timer -= 1
    globals.timerrunning = False
