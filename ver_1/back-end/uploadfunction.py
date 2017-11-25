import os.path
import sys, time, requests, json, binascii
import boto
from boto.s3.key import Key
import boto.s3.connection
region_host = 'your-region'
# yes this is the dumb way to do this, I also have the CLI session version but had problems at the time
s3Conn = boto.connect_s3('key','secret_key', host=region_host)
mybucket = "your-bucket-name"

# slack
webhook_url = 'your-webhook-url'

# function: update batch state
def update_batch_state(batch_state):
    f = open('/home/pi/Adafruit_Python_MCP3008/examples/batch_state.txt', 'w')
    f.write(batch_state)  # python will convert \n to os.linesep
    f.close()

# function: update cloud uploaded files list
def update_cloud_uploaded_files_list(file_item):

    # get current list
    cur_list_str = open('/home/pi/Adafruit_Python_MCP3008/examples/cloud-uploaded-files.txt', 'r')
    cur_list = cur_list_str.readlines()

    # update cur list by adding file_item
    new_list = cur_list.append(file_item)
    write_me = ",".join(cur_list)

    # update cloud-uploaded-files.txt
    f = open('/home/pi/Adafruit_Python_MCP3008/examples/cloud-uploaded-files.txt', 'w')
    f.write(write_me)  # python will convert \n to os.linesep
    f.close()

# external reference
upload_counter = 0

def file_upload(file_path,file_name,call_back,file_list):

    global s3Conn, mybucket, update_cloud_uploaded_files, time, os, upload_counter

    today_date = time.strftime("%m-%d-%Y")
    ran_4_hex = binascii.b2a_hex(os.urandom(2))

    bucketobj = s3Conn.get_bucket(mybucket)
    k = Key(bucketobj)
    k.key = ran_4_hex + '_' + today_date + '_' + file_name
    # k.new_key = file_name
    k.set_contents_from_filename(file_path)
    update_cloud_uploaded_files_list(file_name)
    print('file uploaded: ' + file_name)
    upload_counter += 1
    time.sleep(0.1) # delay in lieu of not having a callback from s3 "upload complete" still a guess
    call_back(file_list)

def batch_upload(upload_list):

    global file_upload, upload_counter, update_batch_state, webhook_url, json

    if (upload_counter < len(upload_list)):
        file_upload('/home/pi/Adafruit_Python_MCP3008/examples/home_security_photos/'+upload_list[upload_counter],upload_list[upload_counter],batch_upload,upload_list)
    else:
        # done
        # send slack notification
        slack_msg = "Uploaded " + str(upload_counter) + " files"
        slack_data = {'text': slack_msg}
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
        # reset upload counter
        upload_counter = 0
        # update batch state
        update_batch_state('yes')
