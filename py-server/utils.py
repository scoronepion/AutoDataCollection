# -*- coding:utf-8 -*-
import os
import io
import re
import time
import json
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
    # 从数据库中获取 task status
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

def get_pgdb_template():
    # 从数据库中获取模板 xml 字符串
    try:
        with psycopg2.connect(database=pgsql_info['database'], user=pgsql_info['user'], \
                            password=pgsql_info['pwd'], host=pgsql_info['address'], \
                            port=pgsql_info['port']) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT content FROM public."adcXmlTemplates" WHERE name=%s', ['sjtu-demo'])
                rows = cur.fetchall()
                return rows[0][0]
    except Exception as e:
        print("set_pgdb_task_status ERROR! " + e)

def save_xml_to_pgdb(taskid=None, xmlstring=None):
    # 从数据库获取当前的 xmlContents , 并将 xmlstring 插入其中，存回数据库中
    try:
        with psycopg2.connect(database=pgsql_info['database'], user=pgsql_info['user'], \
                            password=pgsql_info['pwd'], host=pgsql_info['address'], \
                            port=pgsql_info['port']) as conn:
            with conn.cursor() as cur:
                # pgsql 行名不识别大小写，统一转换为小写查询，要想识别大小写，必须加引号将列名括起来
                cur.execute('SELECT xmlcontents FROM public."adcAutoTasks" WHERE taskid=%s', ['{taskid}'.format(taskid=taskid)])
                rows = cur.fetchall()
                current_xml_data = rows[0][0]
                current_xml_data['deformation-processing'] = xmlstring
                jsonObj = json.dumps(current_xml_data)
                cur.execute('UPDATE public."adcAutoTasks" SET xmlcontents=%s WHERE taskid=%s', \
                            [jsonObj,'{taskid}'.format(taskid=taskid)])
                print("xml 字符串上传成功")

        # with psycopg2.connect(database=pgsql_info['database'], user=pgsql_info['user'], \
        #                     password=pgsql_info['pwd'], host=pgsql_info['address'], \
        #                     port=pgsql_info['port']) as conn:
        #     with conn.cursor() as cur:
        #         # pgsql 行名不识别大小写，统一转换为小写查询，要想识别大小写，必须加引号将列名括起来
        #         cur.execute('UPDATE public."adcAutoTasks" SET "xmlContents"=%s WHERE taskid=%s', \
        #                     [xmlObj,'{taskid}'.format(taskid=taskid)])
        return True
    except Exception as e:
        print("save_xml_to_pgdb ERROR! " + e)

def auto_loop_read_txt(filePath=None, flagPath=None, incremental_read=True, startid=None, endid=None, taskid=None):
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
        time.sleep(10)
    # 以下代码原本用于在服务器端拼接字符串，然后上传至 MDCS 中，现已改为网站统计上传
    # template = get_pgdb_template()
    # matchObj = re.match(r'(.*<deformation-processing>)(</deformation-processing>.*)', template)
    # finalxml = matchObj.group(1) + fullxml + matchObj.group(2)

    # 将 finalxml 存入数据库中
    save_xml_to_pgdb(taskid=taskid, xmlstring=fullxml)
    # print(fullxml)

def auto_txt2xml(filePath=None, flagPath=None, incremental_read=True, startid=None, endid=None, taskid=None):
    if filePath is None:
        filePath = TXT_DATA_PATH
    if flagPath is None:
        flagPath = TXT_FLAG_PATH

    # TODO: 待修改，status 已变为 json
    # 读取设备数据前，先将数据库中相应 taskid 记录的 status 改为 1
    # set_pgdb_task_status(taskid=taskid, status=1)

    # 进入采集过程，此操作需要生成新线程执行，否则会阻塞 rpc 通信
    process = threading.Thread(target=auto_loop_read_txt, args=(filePath, flagPath, incremental_read, startid, endid, taskid))
    process.start()

    return True