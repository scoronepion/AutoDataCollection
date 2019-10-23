# -*- coding:utf-8 -*-
import os
import io
import time
import pickle
import psycopg2
import threading
import MySQLdb
from xml.dom.minidom import Document

TXT_DATA_PATH = '../data/test.txt'
TXT_FLAG_PATH = '../data/txt_flag.b'      # 保存了上次文件读取的位置
CSV_DATA_PATH = '../data/test.csv'
CSV_FLAG_PATH = '../data/csv_flag.b'      # 保存了上次文件读取的位置
mysql_info = {
    "address": "192.168.93.132",
    "user": "root",
    "pwd": "123456",
    "database": "myblog"
}
pgsql_info = {
    "address": "192.168.1.19",
    "database": "mdcs",
    "user": "postgres",
    "pwd": "lab106",
    "port": "5432"
}

def str2xml(label, data):
    # label 为标签，data 为数据，返回 xml 字符串
    xmlBuilder = Document()
    device = xmlBuilder.createElement("deformation-processing-record")  # 创建 device 标签，这里以交大工艺变形处理数据为例进行开发
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
    return data, position

def txt2xml(filePath=None, flagPath=None, incremental_read=True):
    if filePath is None:
        filePath = TXT_DATA_PATH
    if flagPath is None:
        flagPath = TXT_FLAG_PATH

    dataString, position = read_txt_file(filePath, flagPath, incremental_read)
    # 只读一条数据
    dataList = dataString.split('\n')[0].split(",")
    # label = ["A", "B", "C", "D"]
    label = ["no", "forging-die-specifications",
            "temperature-of-mould-before-deformation",
            "temperature-of-workpiece-before-deformation",
            "deformation-time",
            "temperature-of-mould-after-deformation",
            "temperature-of-workpiece-after-deformation",
            "dimension-of-workpiece-after-deformation"]
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
    
    return label, data, position

def csv2xml(filePath=None, flagPath=None, incremental_read=True):
    if filePath is None:
        filePath = CSV_DATA_PATH
    if flagPath is None:
        flagPath = CSV_FLAG_PATH
    label, data, position = read_csv_file(filePath, flagPath, incremental_read)
    label = label.strip().split(",")
    data = data.strip().split(",")
    xmlResult = str2xml(label, data)
    return xmlResult

def read_mysql(info=None):
    if info is None:
        info = mysql_info
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

def set_pgdb_task_status(taskid=None, status=None):
    try:
        with psycopg2.connect(database=pgsql_info['database'], user=pgsql_info['user'], \
                            password=pgsql_info['pwd'], host=pgsql_info['address'], \
                            port=pgsql_info['port']) as conn:
            with conn.cursor() as cur:
                # 要查询的参数必须用单引号括起来，否则会报错。。(太坑了= =)
                cur.execute('UPDATE public."adcAutoTasks" SET status=%s WHERE taskid=%s', [status,'{taskid}'.format(taskid=taskid)])
        return True
    except Exception as e:
        print("set_pgdb_task_status ERROR! " + e)

def auto_loop_read_txt(filePath=None, flagPath=None, incremental_read=True, startid=None, endid=None):
    label = ["no", "forging-die-specifications",
            "temperature-of-mould-before-deformation",
            "temperature-of-workpiece-before-deformation",
            "deformation-time",
            "temperature-of-mould-after-deformation",
            "temperature-of-workpiece-after-deformation",
            "dimension-of-workpiece-after-deformation"]
    # 默认所有给定的 id 状态为 false，即无数据
    idStatus = {}
    for i in range(startid, endid+1):
        idStatus[i] = False
    fullxml = ""
    # 当给定的 id 范围中存在无数据的 id 时（表示此条 id 对应的实验还未完成），循环
    while False in idStatus.values():
        # 每次循环都重新读取 txt 文件
        dataString, position = read_txt_file(filePath, flagPath, incremental_read)
        dataList = dataString.split('\n')
        # 处理本次读取到的数据
        for item in dataList:
            temp = item.split(",")
            # id 在范围中，且为新数据
            if int(temp[0]) in idStatus.keys() and idStatus[int(temp[0])] == False:
                tempResult = str2xml(label, temp)
                fullxml += tempResult
                idStatus[int(item[0])] = True
        # 阻塞 10 秒，防止过于频繁的磁盘 io
        print(idStatus)
        time.sleep(10)
    print(fullxml)

def auto_txt2xml(filePath=None, flagPath=None, incremental_read=True, startid=None, endid=None, taskid=None):
    if filePath is None:
        filePath = TXT_DATA_PATH
    if flagPath is None:
        flagPath = TXT_FLAG_PATH

    # 读取设备数据前，先将数据库中相应 taskid 记录的 status 改为 1
    set_pgdb_task_status(taskid=taskid, status=1)

    # 进入采集过程，此操作需要生成新线程执行，否则会阻塞 rpc 通信
    process = threading.Thread(target=auto_loop_read_txt, args=(filePath, flagPath, incremental_read, startid, endid))
    process.start()

    return True