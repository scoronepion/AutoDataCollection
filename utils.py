import os
import io
import pickle
from xml.dom.minidom import Document

DATA_PATH = './data/test.txt'
FLAG_PATH = './data/flag.b'      # 保存了上次文件读取的位置

def readFile(filePath=None, flagPath=None, incremental_read=True):
    if filePath is None:
        filePath = DATA_PATH
    if flagPath is None:
        flagPath = FLAG_PATH

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
    with open(filePath, 'r') as f:
        f.seek(position, 0)
        data = f.read()
        # 记录当前访问位置
        position = f.tell()
        with open(flagPath, 'wb') as fll:
            pickle.dump(position, fll)
    return data

def txt2xml(filePath=None, flagPath=None, incremental_read=True):
    if filePath is None:
        filePath = DATA_PATH
    if flagPath is None:
        flagPath = FLAG_PATH

    dataString = readFile(filePath, flagPath, incremental_read)
    dataList = dataString.strip().split(",")

    xmlBuilder = Document()
    device = xmlBuilder.createElement("device")  # 创建 device 标签
    xmlBuilder.appendChild(device)
    
    dataA = xmlBuilder.createElement("DataA")    # 创建 DataA 标签
    dataAContent = xmlBuilder.createTextNode(dataList[0])
    dataA.appendChild(dataAContent)
    device.appendChild(dataA)

    dataB = xmlBuilder.createElement("DataB")    # 创建 DataB 标签
    dataBContent = xmlBuilder.createTextNode(dataList[1])
    dataB.appendChild(dataBContent)
    device.appendChild(dataB)

    dataC = xmlBuilder.createElement("DataC")    # 创建 DataC 标签
    dataCContent = xmlBuilder.createTextNode(dataList[2])
    dataC.appendChild(dataCContent)
    device.appendChild(dataC)

    dataD = xmlBuilder.createElement("DataD")    # 创建 DataD 标签
    dataDContent = xmlBuilder.createTextNode(dataList[3])
    dataD.appendChild(dataDContent)
    device.appendChild(dataD)

    xmlIO = io.StringIO()
    xmlBuilder.writexml(xmlIO, encoding='utf-8')
    xmlResult = xmlIO.getvalue().split("?>")[1]     # 去除 xml 头标记
    xmlIO.close()
    return xmlResult