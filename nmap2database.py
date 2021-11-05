#!/uer/bin/env python3
# encoding: utf-8

# 扫描结果保存至CSV,结果累加

import csv
import datetime
import json
import logging
import os
import re
import sys
import threading
import time

import nmap
import xlrd
import xlwt


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s - %(filename)s line %(lineno)d] - %(levelname)s: %(message)s',
    # datefmt='%a, %d %b %Y %H:%M:%S',
    datefmt='%Y-%m-%d %H:%M:%S',
)
os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))

if not os.path.exists('./data'):
    os.mkdir('./data')

cachefile = './data/cache.txt'
ip_txt = './data/ip_port.txt'
result_lixt = './result_list.txt'
csv_name = (time.strftime("%Y-%m-%d", time.localtime()))
result_file = './'+ csv_name +'.csv'
scan_raw_result = {}
header = ['IP', '端口', '主机端口', '协议', 'state', '服务']

def Clear():
    open(cachefile, 'w', encoding='utf-8').write('')
    open(ip_txt, 'w', encoding='utf-8').write('')
    if not os.path.exists(result_file):
        print ('Create',result_file)
        open(result_file,'w',encoding='utf-8').write('')


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
                return False,''            # 无数据
            else:
                data_list.append(header)
                for row in reader:
                    data_list.append(row)
                header_flag = True
                return header_flag, data_list
    except FileNotFoundError as e:
        open(csv_file,'w+')
        pass

def Write2CSV(*args):
    '''
    param:
    csv_file,header,data
    '''
    data = args[0]
    # csv header判断
    csv_file = result_file
    flag = ReadCSV(csv_file)[0]
    logging.debug(csv_file)
    logging.debug(flag)
    if flag == True:
        with open(csv_file, 'a+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows([data])
        pass

    if flag == False:
        with open(csv_file, 'a+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows([data])

def Write_log(data):
    open(result_lixt, 'a+', encoding='utf-8').write(data)


def nmap1(host, portlist, t_numb):
    t_numb.acquire()
    Nmap = nmap.PortScanner()  # 生成nmap
    print(host, portlist)
    np = Nmap.scan(hosts=host, ports=portlist, arguments='-n -Pn')
    for host, values in np['scan'].items():
        scan_raw_result[host] = values
    t_numb.release()


def write_file(what_file, file_name):          # 写文件到excel
    flag = 1
    try:
        for ip in what_file:
            for name, vars in scan_raw_result[ip].items():
                if "tcp" in name:                          # tcp协议
                    for port, tvalues in scan_raw_result[ip]['tcp'].items():
                        # ip
                        # port
                        ip_port = str(ip) + ':' + str(port)
                        agree = 'tcp'
                        port_status = tvalues['state']
                        server_name = tvalues['name']
                        # CSV
                        if tvalues['name'] == '':
                            server_name = 'unknown'
                        # else:
                        #     server_name == tvalues['name']
                        tmp_data = [ip, port, ip_port, agree,
                                    port_status, server_name]
                        Write2CSV(tmp_data)

                if "udp" in name:                          # udp协议
                    for port, tvalues in scan_raw_result[ip]['udp'].items():
                        # ip
                        # port
                        ip_port = ip + ':' + port
                        agree = 'udp'
                        port_status = tvalues['state']
                        server_name = tvalues['name']
                        # CSV
                        if tvalues['name'] == '':
                            server_name = 'unknown'
                        # else:
                        #     server_name == tvalues['name']
                        tmp_data = [ip, port, ip_port, agree,
                                    port_status, server_name]
                        Write2CSV(tmp_data)
            flag += 1
        print(file_name+'写入完成，ojbk，共' + str(flag-1) + '条数据')
    except Exception as e:
        raise
        print(e)


def DataFormat(*args):

    dir = {}
    data = []
    t_list = []

    file = open(readfile, encoding='utf-8')
   # ip_port=file.read()
    data = file.readlines()
    t_numb = threading.Semaphore(20)
   # host=ip_port.split("\n")

    for line in data:
        line_num = data.index(line)
        data_num = len(data)
        load_percentage = (line_num / data_num)*100

        print('%'+'%.2f' % load_percentage, end='\r')
        # 添加数据格式判断
        pattern = r'\-|\(|\)|<|\"'
        pattern_ip_port = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{0,5}'

        result = re.findall(pattern, line)
        result2 = re.findall(pattern_ip_port, line)
        if result:
            Wirte2File(line, 'cache')
            continue
            pass
        if len(result2) == 0:
            Wirte2File(line, 'cache')
            continue
        line = line.strip()
        ip_port = line.split(":")

        if ip_port[0] not in dir:
            dir[ip_port[0]] = []

        if ip_port[1] not in dir[ip_port[0]]:
            dir[ip_port[0]].append(ip_port[1])
        line = line + '\n'
        Wirte2File(line, 'data')
        # print ('Data format yes!')

    for ip, value in dir.items():
        ports = ','.join(str(port) for port in value)
        t = threading.Thread(target=nmap1, args=(ip, ports, t_numb,))
        t_list.append(t)

    for t in t_list:
        t.start()

    for t in t_list:
        t.join()
    pass
    key1 = list(set(scan_raw_result.keys()))

    write_file(key1, "主机")


def Wirte2File(*args):
    if args[1] == 'cache':
        open(cachefile, 'a+', encoding='utf-8').write(args[0])
    if args[1] == 'data':
        open(ip_txt, 'a+', encoding='utf-8').write(args[0])

    pass


if __name__ == '__main__':
    params = sys.argv
    if len(params) == 1:
        readfile = './ip.txt'
    if len(params) == 2:
        readfile = params[1]

    Clear()
    DataFormat(readfile)
    print("ojbk")
