

import json
import logging
import os
import re
import sys
import time

import csv_save as cs

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s',
    # format='[%(asctime)s - %(filename)s line %(lineno)d] - %(levelname)s: %(message)s',
    # datefmt='%a, %d %b %Y %H:%M:%S',
)

os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))

if not os.path.exists('./data'):
    os.mkdir('./data')

csv_name = (time.strftime("%Y-%m-%d", time.localtime()))
csv_file = './'+ csv_name +'.csv'
header = ['IP', '端口', '主机端口', '协议', 'state', '服务']
data = [
    ['127.0.0.1', '22', '127.0.0.1:22', 'tcp', 'closed', '1234'],
]
cs.Write2CSV(csv_file, header, data)
