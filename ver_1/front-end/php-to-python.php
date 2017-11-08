<?php

    error_log(exec('whoami'));

    if ($_SERVER['REQUEST_METHOD'] === 'POST') {

        // get requested state
        $camera_state = $_POST['camera_state'];

        if ($camera_state == 'on') {

            error_log('home security camera poll started');
            exec('/usr/bin/python /home/pi/Adafruit_Python_MCP3008/examples/camera-on.py');

        }
        else if ($camera_state == 'off') {

            error_log('home security camera turned off');
            exec('/usr/bin/python /home/pi/Adafruit_Python_MCP3008/examples/camera-off.py');
            exec('pkill -f simpletest2.py');

        }

    }