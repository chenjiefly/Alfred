#!/usr/bin/python
# encoding: utf-8
import common
import eagleeyeSearch
import sys
from aliProductivity.utils import cacheUtil,LogUtil
reload(sys)
sys.setdefaultencoding('utf8')

# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3

# 1. 获取数据
def getData(searchStr,wf):
    return wf.cached_data('$___eagleeye_'+searchStr,lambda :eagleeyeSearch.search(searchStr),max_age=604800)

# 2. 处理异常
def onException(searchStr ,wf):
    wf.add_item(title='登录态失效，请按Enter键登录之后重试~',
                subtitle= '按Enter可以到鹰眼官网获取登录态',
                arg = 'https://eagleeye-console.alibaba-inc.com/',
                icon = "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns",
                valid=True)
    wf.add_item("")
    return wf

# 3. 解析数据
def parseData(searchStr ,wf ,data):
    if len(data) > 0:
        for apphost in data:
            wf.add_item(
                title=apphost,
                subtitle= '按Enter键打开新版鹰眼',
                arg = 'https://eagleeye-console.alibaba-inc.com/trace?pid='+apphost,
                autocomplete = apphost,
                valid=True)
    else :
        wf.add_item(
                title='查询结果为空😿...',
                subtitle= '按Enter可以到鹰眼官网查询~',
                arg = 'https://eagleeye-console.alibaba-inc.com/',
                icon = "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns",
                valid=True)
    return wf


def search(searchStr , list):
    if len(searchStr) <= 0 :
        return list

    startMatchs = []
    contains = []
    for item in list:
        if item['id'].startswith(searchStr):
            startMatchs.append(item)
        elif searchStr in item['id']:
            contains.append(item)

    return startMatchs + contains





