So... my junk SD card died(one of those no-brand regular black SD cards). It completely died I can't even clone the SD card, this is not great.
I thought my Pi had died so I switched out a new pi with the camera hardware and plugged it in, still not working.
I was like what the heck is wrong with this thing, then happened to try my other SD card and boom. Green LED goes on, boots up. Tried old Pi same thing... using new SD card was fine(new sd card had existing Pi OS on it already).

### Dependencies

#### Web front end(on/off)
* [Apache PHP](https://www.raspberrypi.org/forums/viewtopic.php?t=214213)
#### Back end
* Python
* AWS boto3(originally using boto)

### Process log

Man this is bad... so I installed Apache and PHP as noted above
It's trying to read this state file now but not able to
Oh... that's right I need the ADC MCP3008 library from Adafruit

I'm using the first set to install eg. `build-essential python-dev`... `setup.py`

After the ADC MCP3008 library is installed, you copy the back end files into the `/examples/` folder
Once the `/back-end/` files are in the path `/home/pi/Adafruit_Python_MCP3008/examples` the front end is happy/can read camera state.

I need to figure out the AWS boto3 setup part and credentials for the S3 bucket

I'm adding the `sudo crontab -e` part in, won't do anything yet

This is the line:

`* * * * * /usr/bin/python/ /home/pi/Adafruit_Python_MCP3008/examples/camera-check.py`

That runs every minute polling to check if that front end file says "on"

~~[Install boto](https://stackoverflow.com/questions/2481287/how-do-i-install-boto)

[AWS cli](https://aws.amazon.com/cli/)

[Details on setting up credentails for AWS](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)~~

I was initially trying to use boto but it had problems installing and could not connect(didn't help I mispelled east as easet for the bucket region)

[install boto3 with pip](https://pypi.org/project/boto3/)

[boto3 upload example](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html)

[manage bucket user permissions](https://console.aws.amazon.com/iam)

[example bucket url](https://s3.console.aws.amazon.com/s3/buckets/your-bucket/?region=us-east-2&tab=overview)

Look at your bucket for info.

Sign into your slack account and get your webhook channel for the camera arm/upload notifications.
Yeah I mentioned my credentials are hardcoded vs. using `.env` file

Pip installer for awscli fails, trying apt-get
Fails due to error `TypeError: unsupported operand type(s) for -=: 'Retry' and 'int'`

`No module named requests` pip install save-my-life

Crap there is a hard-coded wifi down check domain in camera-check.py pick a dependent domain or your own local network ip.

oh my god there's another obscure thing, this secondary arming file on a remote server... with abstracted url hmm

Yeah this is pretty bad... pretty much a useless codebase if you don't know how to piece it together

Had to change file permission on testfile.txt which web sets(need www-data:pi) then set it to use 775(possibly 755) so pi can read it.

need `home_security_photos` folder in `/Adafruit_Python_MCP3008/examples/` I set it to 775

status files will be updated when it's working

You can test by running the $python `/Adafruit_Python_MCP3008/examples/camera-check.py/` and it will go through

Ahh have to enable camera

sudo `raspi-config` then reboots

Getting close, at this time web interface works, camera states update, try to run, webhook works

no module named start_cam hmmm

simple test 2 unused module line 5

it's taking pictures now, but not uploading

damn more hard coded changes in `uploadfunction.py`

can test upload directly after having some files in home_security_photos by setting yes in batch_state.txt and then running python cloudupload.py which calls/imports functions from uploadfunction.py

There is also a difference in a file creatd with notepad vs. one created with vscode when you type yes/no into a file. It's different/python doesn't read correctly

Oohh... this feeling of defeat.
Somethings wrong with the wiring, the CPU gets super hot... I don't know what is wrong.

Couple days later...

So I bought more Pis and more ADCs. I think the ADCs are fine. I had a darwin moment when I thought I could use 2, 20pin headers as a socket and I was like "Why are all the ADC values reading as 1023" stupid(poor connection)

I got the upload working , I ended up having to use boto3 which wasn't bad and reads from the aws cli

So I will clean up/rewrite this code as it's pretty useless as it is now I realize
