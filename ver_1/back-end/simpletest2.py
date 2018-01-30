import json
import requests
import os, getpass
from take_photo import snap
from start_cam import start_camera
webhook_url = 'your-webhook-url'

# check first
test_str = open('/home/pi/Adafruit_Python_MCP3008/examples/testfile.txt', 'r').read()
if ('camera on' in test_str):
    second_state = open('/home/pi/Adafruit_Python_MCP3008/examples/second-state.txt', 'r').read()
    print(second_state)
    if ('loop in progress' not in second_state):
        print ('if ran')
        f = open('/home/pi/Adafruit_Python_MCP3008/examples/second-state.txt', 'w')
        f.write('loop in progress')  # python will convert \n to os.linesep
        f.close()
        
# called in another script now, camera-check.py
#         slack_data = {'text': "Camera Armed"}
#         # slack send information
#         response = requests.post(
#             webhook_url, data=json.dumps(slack_data),
#             headers={'Content-Type': 'application/json'}
#         )
#         if response.status_code != 200:
#             raise ValueError(
#                 'Request to slack returned an error %s, the response is:\n%s'
#                 % (response.status_code, response.text)
#             )

        print('this executed')

        import time

        # Import SPI library (for hardware SPI) and MCP3008 library.
        import Adafruit_GPIO.SPI as SPI
        import Adafruit_MCP3008

        # upload script

        # Software SPI configuration:
        CLK  = 18
        MISO = 23
        MOSI = 24
        CS   = 25
        mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

        # comparison
        recent_values = []; # empty array
        
        # dynamic threshold setting
        default_threshold = 700
        high_threshold = default_threshold

        # Main program loop.
        while True:

            # this has a debouncer, for every 6 sequential sensor reads, if at least 2 are above 800
            # take a picture
            # remove the last one (first in list after 6 have been recorded)
            
            motion_sensor_output = mcp.read_adc(0)
            
            # print (motion_sensor_output)
            
            # compare and get threshold
            if (motion_sensor_output > high_threshold):
                # compare first digit
                if (int(str(motion_sensor_output)[:1]) > int(str(high_threshold)[:1])):
                    # update new high threshold
                    high_threshold = int(str(motion_sensor_output)[:1] + '00')
            else:
                # add to highest threshold, maybe PIR to ADC outputting less than 700 as peak value
                # highest, low-baseline measured, currently back down to 0-4
                if (motion_sensor_output > 160 and motion_sensor_output < default_threshold):
                    high_threshold = int(str(motion_sensor_output)[:1] + '00')
            
            if (motion_sensor_output > high_threshold):

                cur_sens_arr_cnt = len(recent_values)

                trimmed_motion_sensor_output = str(motion_sensor_output)[:1]

                if (cur_sens_arr_cnt == 6):

                    # remove last one (first in list)
                    recent_values.pop(0)

                    # add new measurement
                    recent_values.append(trimmed_motion_sensor_output)

                    # check occurrence count, if at least 2 trigger camera eg. [0,8,8,0,0,0] or [8,8,0,0,0,0] etc...
                    occur_count = recent_values.count(trimmed_motion_sensor_output)
                    if (occur_count >= 2):

                        # take picture
                        snap()

                else:

                    # add new measurement
                    recent_values.append(trimmed_motion_sensor_output)
                    
                    # take first 6 pictures anyway due to 300ms lag
                    snap()

            time.sleep(0.3)


elif ('camera off' in test_str):
    # end raspistill
    os.system("pkill raspistill")
    # terminate processes
    os.system('pkill -f simpletest2.py')
