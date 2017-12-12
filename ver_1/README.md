### Note

This is using the bad way to interface with Amazon S3 regarding hard-coded credentials
This is also not cleaned up/paths setup, this is what is currently click-button-works at this time.

### Thanks

Thanks to Adafruit's library and tutorial on interfacing with the ADC MCP3008, note how this code was pretty much built around that library/directory.

Expanding on this:

In my configuration, the directory path is ```~/Adafruit_Python_MCP3008/examples/```
So I installed Adafruit's MCP3008 library as per their instructions using commands noted on the first part of their GitHub page:

https://github.com/adafruit/Adafruit_Python_MCP3008

Then followed their tutorial on how to wire the ADC to the pi
https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008

# Introduction

This is a web-triggered, motion-based, home security system using the Raspberry Pi and a PIR sensor. It's only using the local web (home WiFi) to turn the system on/off (arming). It has a public web connection but it's one directional (to Amazon S3) and to Slack (to let me know it's armed before I leave my apartment and that files uploaded(photos were taken)). I have a cat so this can happen.

The photos are not accessible online unless you set that up. I have to log into Amazon S3 to view the photos and they're not easily displayed eg. tiles to my knowledge just a list of files.

# How does it work?

Here's a visual flow chart on how the code works:

![Alt text](https://raw.githubusercontent.com/jdc-cunningham/raspi-home-security-cam/master/ver_1/correct-path.png "Raspberry Pi Home Security Camera PIR Motion Sensor Using PHP+Python and Amazon S3")

Use case, you browse the Raspberry Pi's local IP 192.168.###.### and assuming you have that setup as a web server (I used Apache) that hosts the front-end code. Provided your file permissions are correct, simply click on, wait a minute (or less depending on CRON time) and the three processes will be started: raspistill, PIR-motion sensor polling(simpletest2.py), and the cloud upload to S3 (cloudupload.py)

# Physical build

![Alt text](https://raw.githubusercontent.com/jdc-cunningham/raspi-home-security-cam/master/concept.jpg "Raspberry Pi Home Security Camera PIR Motion Sensor Using PHP+Python and Amazon S3")

Yeah it is pretty ugly. I can't fabricate boards yet at this time or have them be built by somebody. This is pretty basic just has the MCP3008 ADC and a voltage divider. I did see that there are solderable-breadboards that might be my next step up. I also ended up using a little 1W LED for visual calibration of the PIR sensor (easier to see it flash = on)

## Wiring diagram

Here is a wiring diagram, the ADC to Pi GPIO bridge is not great haha, took me a couple of orientation attempts to figure out how to best illustrate. If you're unsure, refer to the Adafruit guide for the MCP3008 ADC: https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008

One thing to note about Adafruit's ADC page, their ADC channel/pinout diagram is good, but the text below that may be misleading with regard to order of the pin list compared to the photo.

![Alt text](https://raw.githubusercontent.com/jdc-cunningham/raspi-home-security-cam/master/ver_1/pi-zero-w-pir-1w-led-wiring.png "Raspberry Pi With 12V PIR Sensor ADC MCP3008 1W LED")

Note the PIR represented here is only showing the output positive and negative leads and not the wires coming from the wall into the PIR.

### How the PIR part works:

This particular PIR when it detects motion, it outputs the same voltage that it gets in, since it's powered by a 12V 3A supply, it outputs 12V. The ADC I believe has a maximum voltage of 5.5V or so, this is where the voltage divider comes in to drop the 12V to something like 3V - 4V due to the 1W LED wired in parallel.

The PIR can be calibrated to stay on for a while or stay on very briefly, that's the setup here, a pulse. The PIR sampling poll is at about 300ms and I believe the Raspberry Pi + Camera can capture at about 200ms per photo using the signal method. It might be possible to go even faster with smaller photos or just do video.

Then it's pretty much, if the ADC input spikes, trigger the photo. The ADC works by multiplying the reference voltage in this case 3.3V from the Pi by the analog input from the ADC which ranges from 0 to 1024. Anyway on average it's between 700 - 800 on my setup. So I added a debouncer (in case of false positives) and a max-setting as the PIR sometimes changes where at rest it's normally outputting 0, but sometimes the base line is above 150 but the peak is normally around 700 - 800.

# Code

I can't go too indepth into the code right now, would like to write a full blog about it, but don't have that setup yet. This is also not that great of a build. I'm just starting to use Python and in general I'm still not great at laying out code architecurally where it makes sense eg. not importing libraries more than once.

I also mentioned I'm not using the method of interfacing with Amazon's S3 service where the credentials are hard-coded. I had the AWSCLI method working as well but the profile wasn't being read right. I imagine it's another permission problem.

# Permissions

In general folders have 755 and files have 644

This was one major source of headache for me, I will list out the files and their permissions:

Folder (front-end) owned by www-data:www-data (Apache)
* index.html (pi or www-data)
* check-text.php (www-data)
* php-to-python.php (www-data)

Folder (back-end) owned by root:root
* camera-check.py (root)
* simpletest2.py (root)
* cloudupload.py (root)
* uploadfunction.py (root)
* camera-on.py, camera-off.py (www-data)
* take_photo.py (root)
* all .txt files except testfile.txt and second-state.txt (root)

It's possible some of these don't need to be owned by root because CRON starts the main process under sudo

# CRON

The crontab to use is sudo crontab as this needs to run as root

# Problems

Right now the main problem is that broken/bad files are uploaded to S3 I think because the code is trying to upload empty stuff. The actual files are uploaded fully but this extra garbage comes along sometimes. Thankfully I'm still in the free tier of AWS services haha.

Edit: Actually they are log files, I just never set the prefix, it was just undefined, can turn logging off in your bucket

# Updates

This will need a restart script when WiFi is down. I tried to get something working but none of the commands would bring WiFi back up. Maybe I was too impatient (need to wait longer than a second). Or maybe not try to call it from Python, rather outside of Python. I noticed it was not connected to the WiFi today but I was home so that was lucky. I updated the firmware maybe that will help.

Will still look into adding that, it needs to set the state to off and then restart again, will probably need a restart_requested state somewhere.
