### Note

This is using the bad way to interface with Amazon S3 regarding hard-coded credentials
This is also not cleaned up/paths setup, this is what is currently click-button-works at this time.

### Thanks

Thanks to Adafruit's library and tutorial on interfacing with the ADC MCP3008, note how this code was pretty much built around that library/directory.

# Introduction

This is a web-triggered, motion-based, home security system using the Raspberry Pi and a PIR sensor. It's only using the local web (home WiFi) to turn the system on/off (arming). It has a public web connection but it's one directional (to Amazon S3) and to Slack (to let me know it's armed before I leave my apartment and that files uploaded(photos were taken)). I have a cat so this can happen.

The photos are not accessible online unless you set that up. I have to log into Amazon S3 to view the photos and they're not easily displayed eg. tiles to my knowledge just a list of files.

# How does it work?

Here's a visual flow chart on how the code works:

![Alt text](https://raw.githubusercontent.com/jdc-cunningham/raspi-home-security-cam/master/raspberry-pi-home-security-motion-camera-to-amazon-s3-event-flowchart.png "Raspberry Pi Home Security Camera PIR Motion Sensor Using PHP+Python and Amazon S3")

Use case, you browse the Raspberry Pi's local IP 192.168.###.### and assuming you have that setup as a web server (I used Apache) that hosts the front-end code. Provided your file permissions are correct, simply click on, wait a minute (or less depending on CRON time) and the three processes will be started: raspistill, PIR-motion sensor polling(simpletest2.py), and the cloud upload to S3 (cloudupload.py)

# Physical build

![Alt text](https://raw.githubusercontent.com/jdc-cunningham/raspi-home-security-cam/master/concept.jpg "Raspberry Pi Home Security Camera PIR Motion Sensor Using PHP+Python and Amazon S3")

Yeah it is pretty ugly. I can't fabricate boards yet at this time or have them be built by somebody. This is pretty basic just has the MCP3008 ADC and a voltage divider. I did see that there are solderable-breadboards that might be my next step up. I also ended up using a little 1W LED for visual calibration of the PIR sensor (easier to see it flash = on)

# Code

I can't go too indepth into the code right now, would like to write a full blog about it, but don't have that setup yet. This is also not that great of a build. I'm just starting to use Python and in general I'm still not great at laying out code architecurally where it makes sense eg. not importing libraries more than once.

I also mentioned I'm not using the method of interfacing with Amazon's S3 service where the credentials are hard-coded. I had the AWSCLI method working as well but the profile wasn't being read right. I imagine it's another permission problem.

# Problems

Right now the main problem is that broken/bad files are uploaded to S3 I think because the code is trying to upload empty stuff. The actual files are uploaded fully but this extra garbage comes along sometimes. Thankfully I'm still in the free tier of AWS services haha.

