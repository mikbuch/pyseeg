#!/bin/bash

`sudo bash -c 'echo 9 > /sys/kernel/debug/bluetooth/hci0/conn_min_interval'`

`sudo bash -c 'echo 10 > /sys/kernel/debug/bluetooth/hci0/conn_max_interval'`
