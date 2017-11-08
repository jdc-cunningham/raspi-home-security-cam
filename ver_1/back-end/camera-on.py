f = open('/home/pi/Adafruit_Python_MCP3008/examples/testfile.txt', 'w')
f.write('camera on')  # python will convert \n to os.linesep
f.close()