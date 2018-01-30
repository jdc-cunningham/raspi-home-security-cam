import os, requests, json, time
from uploadfunction import batch_upload

# define functions
def get_batch_state():
    return open('/home/pi/Adafruit_Python_MCP3008/examples/batch_state.txt', 'r').read()

def update_batch_state(batch_state):
    f = open('/home/pi/Adafruit_Python_MCP3008/examples/batch_state.txt', 'w')
    f.write(batch_state)  # python will convert \n to os.linesep
    f.close()

while True:

    # check batch_state, yes means currently in upload process, no means no upload is happening
    cur_batch_state = get_batch_state()
    if ('yes' in cur_batch_state):

        # try a new upload

        # reset variables
        to_upload = [];

        # get cur list of captured images
        cur_cam_files = os.listdir('/home/pi/Adafruit_Python_MCP3008/examples/home_security_photos')
        
        # get cur list of uploaded files
        cur_uploaded_files = open('/home/pi/Adafruit_Python_MCP3008/examples/cloud-uploaded-files.txt', "r").read().split(',')

        # compare
        for item in cur_cam_files:
            if ('.jpg' in item and '.jpg~' not in item):
                if (item not in cur_uploaded_files):
                    # append to to_upload list
                    to_upload.append(item)
        
        # done adding, check if there is anything new to upload
        if (len(to_upload) > 0):
            # start new upload process
            update_batch_state('no')
            # call batch upload
            batch_upload(to_upload)

    
    # polling
    # print('cloud upload polling...') # these get super long in the logs
    time.sleep(1)
