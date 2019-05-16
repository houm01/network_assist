#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# github: https://github.com/houm01
# blog: https://houm01.com

import re
import os
import psycopg2


def get_tech_info(raw_tech_info):
    with open(raw_tech_info,'r') as f:
        raw_text = f.read()
        hostname = re.search('hostname (.*)',raw_text).groups()[0]
        mgt_ip = re.search('ip address(.*)255.255.255',raw_text).groups()[0]
        model = (([x for x in (''.join(re.search('\*(.*)', raw_text).groups())).split(' ') if x != '']))
        # print(model)
        version = (([x for x in (''.join(re.search('\*(.*)', raw_text).groups())).split(' ') if x != '']))
        # print(version)

        if model == 'WS-C3850-24S':
            # global sw_image
            sw_image = (([x for x in (''.join(re.search('\*(.*)', raw_text).groups())).split(' ') if x != ''])[-2])
        else:
            sw_image = (([x for x in (''.join(re.search('\*(.*)', raw_text).groups())).split(' ') if x != ''])[-1])

        uptime = re.search('uptime is(.*)',raw_text).groups()[0]
        try:
            global sn
            global memory_per
            sn = re.search('System serial number            : (.*)',raw_text).groups()[0]
            memory_total = (
            ([x for x in (''.join(re.search('Processor Pool Total:(.*)', raw_text).groups())).split(' ') if x != ''])[
                0])
            memory_usage = (([x for x in (''.join(re.search('Processor Pool Total:(.*)', raw_text).groups())).split(' ') if x != ''])[2])
            memory_per = '%.2f%%' %(int(memory_usage)/int(memory_total))
        except AttributeError:
            pass
        running_config = raw_text[raw_text.find('Building configuration'):raw_text.find('show stacks')]
        cpu_usage = re.search('five minutes: (.*)',raw_text).groups()[0]
        show_logging = raw_text[raw_text.find('show logging')-20:raw_text.find('show env all')]
        port_channel = raw_text[raw_text.find('show etherchannel summary')-20:raw_text.find('show ipc nodes')]
        swith_detail = raw_text[raw_text.find('show switch detail')-20:raw_text.find('remote command all show vtp status')]
        inventory = raw_text[raw_text.find('show inventory')-20:raw_text.find('show region')]

    return hostname,mgt_ip,model,version,sw_image,uptime,sn,running_config,cpu_usage,memory_per,show_logging,port_channel,swith_detail,inventory


def write_tech_todb():
    conn = psycopg2.connect(dbname="pyxnetdb", user="pyxnetuser", password="JoMCHnp4UT", host="10.1.1.8",
                               port="5432")

    cur = conn.cursor()
    # cur.execute("CREATE TABLE if not exists hlgh_sw "
    #             "(id serial PRIMARY KEY,"
    #             "hostname varchar,"
    #             "model varchar,"
    #             "version varchar,"
    #             "sw_image varchar,"
    #             "uptime varchar,"
    #             "sn varchar,"
    #             "running_config varchar,"
    #             "cpu_usage varchar,"
    #             "memory_per varchar,"
    #             "show_logging varchar,"
    #             "port_channel varchar,"
    #             "swith_detail varchar,"
    #             "inventory varchar);")

    file_raw = os.listdir()
    for x in file_raw:
        if 'AC' in x:
            cur.execute("INSERT INTO customers_data_assist_2019q1_hldl_device (hostname,mgt_ip,model,version,sw_image,uptime,sn,running_config,cpu_usage,memory_per,"
                "show_logging,port_channel,switch_detail,inventory) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (get_tech_info(x)))
    # cur.commit()

    # cur.execute("SELECT * FROM hlgh_sw;")
    conn.commit()
    cur.close()
    conn.close()


# if __name__ == '__main__':
    # file_raw = os.listdir()
    # for x in file_raw:
    #     if 'PLAZA' in x:
    #         get_tech_info(x)

    # write_tech_todb()



