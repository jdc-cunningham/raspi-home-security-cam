import os

def snap():
    
    global os

    os.system('pkill -SIGUSR1 raspistill')