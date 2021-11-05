import csv
import json
import os
import re
import sys
import time

import MyCode

csv_file = './data/test.csv'


def ReadFromCSV():
    with open(csv_file, encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        print(header)
        for row in reader:
            print(row)


def Write2CSV():
    header = ['name', 'password', 'status']

    data = [
        ['abc', '123456', 'PASS'],
        ['张五', '123#456', 'PASS'],
        ['张#abc123\n123', '123456', 'PASS'],
        ['666', '123456', 'PASS'],
        ['a b', '123456', 'PASS']
    ]

    with open(csv_file, 'a+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def PortScan2CSV():
    header = ['IP', '端口', '主机端口', '协议', 'state', '服务']

    data = []


    with open(csv_file, 'a+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

if __name__ == '__main__':
    Write2CSV()
