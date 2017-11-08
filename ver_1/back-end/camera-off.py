f = open('/home/pi/Adafruit_Python_MCP3008/examples/testfile.txt', 'w')
f.write('camera off')  # python will convert \n to os.linesep
f.close()
f = open('/home/pi/Adafruit_Python_MCP3008/examples/second-state.txt', 'w')
f.write('')  # python will convert \n to os.linesep
f.close()