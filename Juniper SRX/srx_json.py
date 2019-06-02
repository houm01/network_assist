#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# github: https://github.com/houm01
# blog: https://houm01.com


import json
import xlwt
import xmltodict


def xmltojson(xmlstr):
    xmlparse = xmltodict.parse(xmlstr)
    jsonstr = json.dumps(xmlparse,indent=1)
    return jsonstr


def Get_address_book():
    with open('center_xml') as file:
        j = json.loads(xmltojson(file.read()))

    address_book_dict = {}

    address_book_raw = j['rpc-reply']['configuration']['security']['address-book']['address']

    for x in address_book_raw:
        if 'ip-prefix' in x.keys():
            address_book_dict[x['name']] = x['ip-prefix']
        else:
            address_book_dict[x['name']] = x['wildcard-address']['name']

    address_book_dict['any'] = 'any'

    return address_book_dict


def create_worksheet():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('test')
    worksheet.write(0, 0, label='from-zone')
    worksheet.write(0, 1, label='to-zone')
    worksheet.write(0, 2, label='policy-name')
    worksheet.write(0, 3, label='source-address')
    worksheet.write(0, 4, label='destination-address')
    worksheet.write(0, 5, label='application')
    worksheet.write(0, 6, label='action')

    with open('center_xml') as file:
        j = json.loads(xmltojson(file.read()))

    sheet_test = []

    for value in j['rpc-reply']['configuration']['security']['policies']['policy']:
        if isinstance(value['policy'], list):    # 如果是 list，说明该区域有多条策略

            aa = len(value['policy'])   # 使用aa和bb保证策略不乱序
            bb = 0

            while bb < aa:
                sheet_test.append((value['from-zone-name'],value['to-zone-name'],
                                   # Get_address_book()[value['policy'][bb]['match']['source-address']],
                                   value['policy'][bb]['name'],
                                   value['policy'][bb]['match']['source-address'],
                                   value['policy'][bb]['match']['destination-address'],
                                   value['policy'][bb]['match']['application'],
                                   value['policy'][bb]['then']
                                   ))
                bb += 1

        else:    # 如果是 dict，说明该区域只有一条策略
            sheet_test.append((value['from-zone-name'], value['to-zone-name'],
                               value['policy']['name'], value['policy']['match']['source-address'],
                               value['policy']['match']['destination-address'],
                               value['policy']['match']['application'],
                               value['policy']['then']))

    val = 1

    for x in sheet_test:
        print(x)
        worksheet.write(val, 0, str(x[0]))
        worksheet.write(val, 1, str(x[1]))
        worksheet.write(val, 2, str(x[2]))
        worksheet.write(val, 3, str(x[3]))
        worksheet.write(val, 4, str(x[4]))
        worksheet.write(val, 5, str(x[5]))
        worksheet.write(val, 6, str(x[6]))
        workbook.save('excel_test.xlsx')
        val += 1


if __name__ == '__main__':
    # print(Get_address_book())
    # Get_address_book()
    create_worksheet()




