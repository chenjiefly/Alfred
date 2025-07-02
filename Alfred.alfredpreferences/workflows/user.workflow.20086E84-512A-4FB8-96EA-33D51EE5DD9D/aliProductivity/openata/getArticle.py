# -*- coding=utf-8 -*-

import sqlite3


def search(searchData):
    sql = '''
        select title,url from  article
        where title like ?
    '''
    datalist=[]
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    res = cursor.execute(sql,(buffer('%'+searchData+'%'),))
    for i in res.fetchall():
        print i[1]
        data=[i[0],i[1]]
        datalist.append(data)
    conn.commit()
    conn.close()
    return datalist
