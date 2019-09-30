import os
import pickle

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