<?php

    // get current URL
    $page_url = (isset($_SERVER['HTTPS']) ? "https" : "http") . "://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";

    $camera_command = explode('&', explode('?camera_on=', $page_url)[1])[0]; // could just use query
    $url_key = explode('&key=', $page_url)[1];

    $expected_key = 'your-key';

    if ($url_key == $expected_key) {

        // read file and see if not on already
        $camera_state_file = "obscure-string-2.txt";
        $file_val = file_get_contents($camera_state_file);

        if ($camera_command == 'yes') {

            if (strpos($file_val, 'off') !== false) {
                // camera currently set to off, turn on
                file_put_contents($camera_state_file, 'camera on');
            }

        }
        else if ($camera_command == 'no') {

            if (strpos($file_val, 'on') !== false) {
                // camera currently set to off, turn on
                file_put_contents($camera_state_file, 'camera off');
            }

        }

    }
    
    $camera_state_file = "obscure-string-2.txt";
    $cur_val = file_get_contents($camera_state_file);
    echo $cur_val;
