# 追加内容,判断header是否为空

import csv
import logging
import os
import sys
import time
import re
import json
import MyCode

import csv_find as cf
import csv_delete as cd


def ReadCSV(*args):
    '''
    :param:
    csv_file,
    :return:
    True,CSVdatalist
    False
    '''
    data_list = []

    try:
        csv_file = args[0]
        with open(csv_file, encoding='utf-8') as f:
            try:
                reader = csv.reader(f)
                header = next(reader)
            except StopIteration as e:
                header_flag = False     # 无header
                return False, ''            # 无数据
            else:
                data_list.append(header)
                for row in reader:
                    data_list.append(row)
                header_flag = True
                return header_flag, data_list
    except FileNotFoundError as e:
        open(csv_file, 'w+')
        pass

    # print (len(csv_file))
    # print (len(header))
    # csv_len = len(csv_file)/len(header)
    # print (int(csv_len))


def Write2CSV(*args):
    '''
    param:
    csv_file,header,data
    入参:二维数组,

    '''

    csv_file = args[0]
    header = args[1]
    data = args[2]
    delete_list = []

    cfs = cf.Solution()

    flag = ReadCSV(csv_file)[0]
    csv_data = ReadCSV(csv_file)[1]
    csv_line = len(csv_data)
    logging.debug('header {}, data length {}'.format(flag, csv_line))

    # 二维数组遍历取第三个字段
    for a in data:
        target = a[2]
        find = cfs.Find(target, csv_data)
        logging.debug('find {}, type {}, result {}'.format(
            target, type(target), find))
        if find[0] == True:
            # 删除函数中pd读取csv不计算header,行数-1
            for x in find[1]:
                x = x-1
                delete_list.append(x)
        else:
            break
    try:
        logging.debug('Delete list {}'.format(delete_list))
        cd.CSVDelete(csv_file, delete_list)
        logging.debug('write into CSV')
    except:
        pass

    if flag == True:
        with open(csv_file, 'a+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            # 写入二维数组
            writer.writerows(data)
        pass

    if flag == False:
        with open(csv_file, 'a+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            # 写入二维数组
            writer.writerows(data)


# if __name__ == "__main__":
#     csv_file = './data/test.csv'
#     header = ['name', 'password', 'status']
#     data = [
#         ['abc', '123456', 'PASS'],
#         ['张五', '123#456', 'PASS'],
#         ['张#abc123', '123456', 'PASS'],
#         ['666', '123456', 'PASS'],
#         ['a b', '123456', 'PASS']
#     ]
#     Write2CSV(csv_file,header,data)
    # tmp = ReadCSV(csv_file)
    # csv_data = tmp[1]
    # for a in csv_data:
    #     # print (a)
    #     pass
    # # check
