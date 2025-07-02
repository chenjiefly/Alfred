# -*- coding=utf-8 -*-

import requests
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import threading
import multiprocessing
import logging
import sqlite3  # 进行SQLite数据库操作
from ..utils import httpUtil

findLink = re.compile(r'href="/articles/(.*?)"')  # 链接
findTitle = re.compile(r'title="(\s*)(.*?)"')  # 标题

baseUrl = 'https://open.atatech.org'

searchUrl = "https://open.atatech.org/articles?order=goodcount&p="

coreCount = multiprocessing.cpu_count()

dbPath = 'data.db'
#2021.8.9 更新数据，586页记录5分44秒爬取完毕
pageCount = 586

threads = []


def main():
    # 1.爬取网页
    # init_db()
    multiThreadStart()


def multiThreadStart():
    gap = pageCount / coreCount
    count = pageCount % coreCount
    for i in range(0, coreCount + 1):
        if i == coreCount and count != 0:
            curThread = threading.Thread(target=getAndSaveData, name="thread-" + str(i), args=(i * gap + 1, count,))
        else:
            curThread = threading.Thread(target=getAndSaveData, name="thread-" + str(i), args=(i * gap + 1, gap,))
        curThread.start()
        threads.append(curThread)
    for t in threads:
        t.join()
        print "当前执行完毕"


def getAndSaveData(start, count):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    datalist = []
    try:
        for i in range(count):
            url = searchUrl + str(start + i)
            html = askURL(url)
            if html == None:
                continue
            encoding = html.encoding
            # 2.解析数据
            soup = BeautifulSoup(html.text.encode(encoding), 'html.parser')
            for item in soup.find_all('a', attrs={'class': 'article-title-weight'}):
                data = []
                item = str(item)
                titles = re.findall(findTitle, item)
                if len(titles)>0:
                    data.append(titles[0])
                    link = re.findall(findLink, item)[0]
                    data.append(int(link))
                    datalist.append(data)
        savaDataDB(datalist, conn)
    finally:
        conn.close()


# 得到指定一个URL的网页内容
def askURL(url):
    response = None
    try:
        response = httpUtil.get(url, baseUrl)
    except Exception as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        print e.message
    return response


# 保存数据到数据库
def savaDataDB(datalist, conn):
    # init_db(dbpath)
    cur = conn.cursor()
    if len(datalist) > 1:
        for data in datalist:
            sql = '''insert  into   testArt(title,url)values(?,?);'''
            try:
                cur.execute(sql, (data[0][1], data[1]))
                conn.commit()
            except sqlite3.IntegrityError as e:
                print '重复文章'+str(data[1])

# 创建一个数据库,一个表
def init_db():
    sql = '''
        create  table   testArt 
        (
            id integer primary key autoincrement,
            title   key text,
            url    integer  
        )
    '''
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

def del_db():
    sql = '''
        drop  table  testArt
    '''
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

def sql_db():
    sql = '''
        select count(distinct(url)) from   testArt
    '''
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    res=cursor.execute(sql)
    print res.fetchall()
    conn.commit()
    conn.close()
