# this script is triggered by a CRON schedule
# for me I am doing every 2 minutes so my CRON tab looks like this (without the #)
# */2 * * * * /usr/bin/python /home/pi/wifi-reconnect.py

# this code is from this thread
# https://www.raspberrypi.org/forums/viewtopic.php?t=133665

# check if not connected to the internet
import os
hostname = 'www.example.com' # or other domain
response = os.system('ping -c 1 ' + hostname)
if response != 0:
    print ('Pi disconnected, rebooting')
    # set system-on.txt state to 'no' for camera-check.py to start the 3 main threads again
    # upon reconnect to WiFi
    f = open('/home/pi/Adafruit_Python_MCP3008/examples/system-on.txt', 'w')
    f.write('no')
    f.close()
    from subprocess import call
    call("sudo shutdown -r now", shell=True)

