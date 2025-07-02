# encoding: utf-8

import os

filePath = './cache/employeeId.txt'

def cache(employeeId):
    if len(employeeId) == 0:
        return
    if employeeId.isspace():
        return
    with open(filePath,"w+") as f:
        f.write(employeeId)

def get():
    if os.path.exists(filePath):
        with open(filePath,"r") as f:
            for line in f.readlines():
                line = line.strip('\n')  #去掉列表中每一个元素的换行符
                return line
    return  ''


if __name__ == '__main__':
    cache('160531')
    print(get())