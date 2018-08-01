import os, threading
from threading import Thread
import requests, json
webhook_url = 'your webhook'

# function: update cloud upload status
# def update_cloud_status(status):
#     f = open('/home/pi/Adafruit_Python_MCP3008/examples/cloud-upload-status.txt', 'w')
#     f.write(status)  # python will convert \n to os.linesep
#     f.close()

# reconnect to WiFi by restarting
hostname = 'www.example.com' # or other domain
response = os.system('ping -c 1 ' + hostname)
if response == 0:
    print ('Pi disconnected, rebooting')
    # set system-on.txt state to 'no' for camera-check.py to start the 3 main threads again
    # upon reconnect to WiFi
    f = open('/home/pi/Adafruit_Python_MCP3008/examples/system-on.txt', 'w')
    f.write('no')
    f.close()
    g = open('/home/pi/Adafruit_Python_MCP3008/examples/second-state.txt', 'w')
    g.write('')
    g.close()
    h = open('/home/pi/Adafruit_Python_MCP3008/examples/batch_state.txt', 'w')
    h.write('yes')
    h.close()
    i = open('/home/pi/Adafruit_Python_MCP3008/examples/cloud-uploaded-files.txt', 'w')
    i.write('') # random comment to add commit msg
    i.close()
    os.system('pkill raspistill')
    os.system('pkill -f simpletest2.py')
    os.system('pkill -f cloudupload.py')
    from subprocess import call
    call("sudo shutdown -r now", shell=True)
    exit()

def update_batch_state(batch_state):
    f = open('/home/pi/Adafruit_Python_MCP3008/examples/batch_state.txt', 'w')
    f.write(batch_state)  # python will convert \n to os.linesep
    f.close()

def reset_cloud_uploaded_files():
    f = open('/home/pi/Adafruit_Python_MCP3008/examples/cloud-uploaded-files.txt', 'w')
    f.write('')  # python will convert \n to os.linesep
    f.close()

def update_system_state(system_state):
    f = open('/home/pi/Adafruit_Python_MCP3008/examples/system-on.txt', 'w')
    f.write(system_state)  # python will convert \n to os.linesep
    f.close()
    
def update_test_file(system_state):
    f = open('/home/pi/Adafruit_Python_MCP3008/examples/testfile.txt', 'w')
    f.write(system_state)  # python will convert \n to os.linesep
    f.close()
    
def update_second_str():
    requests.get("http://your-ip/obscure-string.php?camera_on=no&key=your-key")

str = open('/home/pi/Adafruit_Python_MCP3008/examples/testfile.txt', 'r').read()
second_str = requests.get("http://your-ip/obscure-string.php")
system_on = open('/home/pi/Adafruit_Python_MCP3008/examples/system-on.txt', 'r').read()
if (('camera on' in str or 'camera on' in second_str) and 'yes' not in system_on):
    # set system state
    update_system_state('yes')
    update_test_file('camera on')

    # start camera
    def cam_start():
        os.system('raspistill -t 0 -s -w 1280 -h 720 -ex sports -awb auto -o /home/pi/Adafruit_Python_MCP3008/examples/home_security_photos/motion_image%04d.jpg')
    # start PIR sensor listener
    def pir_start():
        os.system('/usr/bin/python /home/pi/Adafruit_Python_MCP3008/examples/simpletest2.py')
    # cloud upload
    def cloud_upload_start():
        os.system('/usr/bin/python /home/pi/Adafruit_Python_MCP3008/examples/cloudupload.py')

    Thread(target=cam_start).start()
    Thread(target=pir_start).start()
    Thread(target=cloud_upload_start).start()
    
    # send slack notification
    slack_data = {'text': "Camera armed"}
    # slack send information
    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
    
    # call upload outside?
    # os.system('/usr/bin/python /home/pi/Adafruit_Python_MCP3008/examples/cloudupload.py')
elif ('camera off' in str):
    # update system state
    update_system_state('no')
    update_second_str()
    # kill processes
    os.system("pkill raspistill")
    os.system('pkill -f simpletest2.py')
    # update_cloud_status('not uploading')
    update_batch_state('yes')
    reset_cloud_uploaded_files()
    os.system('pkill -f cloudupload.py')
    # os.system('/usr/bin/python cloud_off.py') # might interrupt an upload in progress will add in loop
    # run again to have it kill the processes
    # os.system('/usr/bin/python /home/pi/Adafruit_Python_MCP3008/examples/simpletest2.py')
