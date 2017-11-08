Skip to content
This repository
Search
Pull requests
Issues
Marketplace
Explore
 @jdc-cunningham
 Sign out
 Unwatch 1
  Star 0  Fork 0 jdc-cunningham/raspi-home-security-cam
 Code  Issues 0  Pull requests 0  Projects 0  Wiki  Insights  Settings
raspi-home-security-cam/ 
README.md
   or cancel
    
 Edit file    Preview changes
1
# Raspberry Pi Home Security Cam With CV (Future)
2
​
3
## Update
4
​
5
I created version 1 (see /ver_1/)
6
I decided against the night vision camera as the footage was always bad even with light. The particular camera I chose was strictly an IR camera. I don't mind having a light on for the camera.
7
​
8
## Features
9
- Night vision camera
10
- Upload to cloud
11
- Motion triggered
12
- CV to distinguish between regular user (owner) and new humans
13
​
14
## Initial Thoughts
15
​
16
Well I'm going to be living alone soon and I don't like the idea of my home being unattended without any sort of assurance that if someone where to waltz in and take my stuff, I'd have proof/know who it was. Potentially it will act as a deterrent as well like "Hey buddy, see this camera, you've already been uploaded to the cloud" sort of deal.
17
​
18
Anyway, more over it's a fun project, more hardware interfacing and another excuse to connect something to the web. I'll also use Amazon's S3 service for the first time to store these photos.
19
​
20
The future CV aspect will be to have the system be able to distinguish between me (normal operation) and a new human body. The other thing is I have a cat and don't want my cat to trigger it. This also lowers notifications as that's how I figure I will set it up, show me the "highlights" or whenever the motion sensor (PIR) was triggered.
21
​
22
## Main Objectives
23
​
24
- Get photo from Raspberry Pi Camera
25
- Setup some sort of polling event (my thought at this time) to wait for input from PIR
26
- Upload the photo to S3 with notification
27
- Setup some sort of "everything is okay clean/flush files"
28
- Implement the CV aspect
29
​
@jdc-cunningham
Commit changes

Update README.md

Add an optional extended description…
  Commit directly to the master branch.
  Create a new branch for this commit and start a pull request. Learn more about pull requests.
Commit changes  Cancel
© 2017 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
API
Training
Shop
Blog
About
