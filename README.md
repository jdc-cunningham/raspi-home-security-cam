# Raspberry Pi Home Security Cam

## Update
I created version 1 (see /ver_1/)
I decided against the night vision camera as the footage was always bad even with light. The particular camera I chose was strictly an IR camera. I don't mind having a light on for the camera.

### Update
I forgot to attach the new photos, I decided to put it in this Raspberry Pi case I stole it from another full sized pi. I used a solder-able breadboard that I cut apart to fit in here with the camera, and a voltage divider 10K and 5K using 3.3V reference.

![Alt text](https://raw.githubusercontent.com/jdc-cunningham/raspi-home-security-cam/master/ver_1/pi-cam-external-using-raspberry-pi-case.jpg "Raspberry Pi Zero with 8MP V2 Cam Full Sized Pi Case with 1W LED and PIR sensor outside at the bottom")

![Alt text](https://raw.githubusercontent.com/jdc-cunningham/raspi-home-security-cam/master/ver_1/pi-cam-guts.jpg "The guts, including 10K 5K voltage divider with 3.3V reference, pi zero wireless and 8MP v2 camera")

## Features
- Night vision camera
- Upload to cloud
- Motion triggered

## Initial Thoughts
Well I'm going to be living alone soon and I don't like the idea of my home being unattended without any sort of assurance that if someone where to waltz in and take my stuff, I'd have proof/know who it was. Potentially it will act as a deterrent as well like "Hey buddy, see this camera, you've already been uploaded to the cloud" sort of deal.

Anyway, more over it's a fun project, more hardware interfacing and another excuse to connect something to the web. I'll also use Amazon's S3 service for the first time to store these photos.

## Main Objectives

- Get photo from Raspberry Pi Camera

- Setup some sort of polling event (my thought at this time) to wait for input from PIR

- Upload the photo to S3 with notification

- Setup some sort of "everything is okay clean/flush files"
