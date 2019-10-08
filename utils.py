# -*- coding:utf-8 -*-
import os
import io
import pickle
import MySQLdb
from xml.dom.minidom import Document

TXT_DATA_PATH = './data/test.txt'
TXT_FLAG_PATH = './data/txt_flag.b'      # 保存了上次文件读取的位置
CSV_DATA_PATH = './data/test.csv'
CSV_FLAG_PATH = './data/csv_flag.b'      # 保存了上次文件读取的位置
dbInfo = {
    "address": "192.168.93.132",
    "user": "root",
    "pwd": "123456",
    "database": "myblog"
}

def str2xml(label, data):
    # label 为标签，data 为数据，返回 xml 字符串
    xmlBuilder = Document()
    device = xmlBuilder.createElement("device")  # 创建 device 标签
    xmlBuilder.appendChild(device)

    for i in range(0, len(label)):
        temp = xmlBuilder.createElement(str(label[i]))
        content = xmlBuilder.createTextNode(str(data[i]))
        temp.appendChild(content)
        device.appendChild(temp)
    
    xmlIO = io.StringIO()
    xmlBuilder.writexml(xmlIO, encoding='utf-8')
    xmlResult = xmlIO.getvalue().split("?>")[1]     # 去除 xml 头标记
    xmlIO.close()
    return xmlResult

def read_txt_file(filePath=None, flagPath=None, incremental_read=True):
    if filePath is None:
        filePath = TXT_DATA_PATH
    if flagPath is None:
        flagPath = TXT_FLAG_PATH

    if incremental_read:
        # 首次访问文件，文件访问记录不存在
        if not os.path.exists(flagPath):
            with open(flagPath, 'wb') as f:
                line = 0
                pickle.dump(line, f)
        # 载入文件访问位置
        with open(flagPath, 'rb') as f:
            position = pickle.load(f)
    else:
        position = 0

    # 大文件增量读取
    with open(filePath, 'r', encoding='utf-8') as f:
        f.seek(position, 0)
        data = f.read()
        # 记录当前访问位置
        position = f.tell()
        with open(flagPath, 'wb') as fll:
            pickle.dump(position, fll)
    return data

def txt2xml(filePath=None, flagPath=None, incremental_read=True):
    if filePath is None:
        filePath = TXT_DATA_PATH
    if flagPath is None:
        flagPath = TXT_FLAG_PATH

    dataString = read_txt_file(filePath, flagPath, incremental_read)
    dataList = dataString.strip().split(",")
    label = ["A", "B", "C", "D"]
    xmlResult = str2xml(label, dataList)
    return xmlResult

def read_csv_file(filePath=None, flagPath=None, incremental_read=True):
    if filePath is None:
        filePath = CSV_DATA_PATH
    if flagPath is None:
        flagPath = CSV_FLAG_PATH

    if incremental_read:
        # 首次访问文件，文件访问记录不存在，则先读取 label，随后记录读取位置
        if not os.path.exists(flagPath):
            with open(filePath, 'r', encoding='utf-8') as f:
                label = f.readline()
                position = f.tell()
                with open(flagPath, 'wb') as flag:
                    line = 0
                    pickle.dump(line, flag)
        # 载入文件访问位置
        with open(flagPath, 'rb') as f:
            position = pickle.load(f)
    else:
        with open(filePath, 'r', encoding='utf-8') as f:
            label = f.readline()
            position = f.tell()

    # 大文件增量读取
    with open(filePath, 'r', encoding='utf-8') as f:
        f.seek(position, 0)
        data = f.read()
        # 记录当前访问位置
        position = f.tell()
        with open(flagPath, 'wb') as flag:
            pickle.dump(position, flag)
    
    return label, data

def csv2xml(filePath=None, flagPath=None, incremental_read=True):
    if filePath is None:
        filePath = CSV_DATA_PATH
    if flagPath is None:
        flagPath = CSV_FLAG_PATH
    label, data = read_csv_file(filePath, flagPath, incremental_read)
    label = label.strip().split(",")
    data = data.strip().split(",")
    xmlResult = str2xml(label, data)
    return xmlResult

def read_mysql(info=None):
    if info is None:
        info = dbInfo
    db = MySQLdb.connect(info['address'], info['user'], info['pwd'], info['database'], charset='utf8')
    cursor = db.cursor()
    cursor.execute("select * from pyTest")
    results = cursor.fetchall()
    db.close()
    for row in results:
        id = row[0] if row[0]!=None else ''
        name = row[1] if row[1]!=None else ''
        age = row[2] if row[2]!=None else ''
        university = row[3] if row[3]!=None else ''
        major = row[4] if row[4]!=None else ''
    label = ['id', 'name', 'age', 'university', 'major']
    data = [id, name, age, university, major]
    xmlResult = str2xml(label, data)
    print(xmlResult)
    return xmlResult