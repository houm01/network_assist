#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# github: https://github.com/houm01
# blog: https://houm01.com


from netmiko import Netmiko


def run_config():
    my_device = {
        "host": '10.1.1.44',
        "username": 'cisco',
        "password": 'cisco123',
        'secret': 'cisco123',
        "device_type": "cisco_ios",
    }
    net_connect = Netmiko(**my_device)

    net_connect.enable()

    running_config = net_connect.send_command("show run")
    print(running_config)


run_config()