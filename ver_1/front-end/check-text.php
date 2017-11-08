<?php

    // check file contents

    $cam_state['cam_state'] = file_get_contents('/home/pi/Adafruit_Python_MCP3008/examples/testfile.txt', true);

    echo json_encode($cam_state);