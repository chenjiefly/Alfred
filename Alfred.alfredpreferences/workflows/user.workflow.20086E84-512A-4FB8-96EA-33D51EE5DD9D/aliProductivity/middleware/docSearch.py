#!/usr/bin/python
# encoding: utf-8

import doc
import sys

# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3
from aliProductivity.utils import cacheUtil


# 1. 获取数据
def getData(searchStr, wf):
    data=wf.cached_data('$___doc', lambda: doc.getDocInfos, max_age=86400)()
    return search(searchStr, data)


# 2. 处理异常
def onException(searchStr, wf):
    wf.add_item(title='登录态失效，请按Enter键登录之后重试~',
                subtitle='按Enter进入Aone官网获取登录态',
                arg='https://aone.alibaba-inc.com/appcenter/lib/list',
                icon="/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns",
                valid=True)
    return wf


# 3. 解析数据
def parseData(searchStr, wf, data):
    if len(data) > 0:
        for docInfo in data:
            wf.add_item(
                title=docInfo['name'] + u'\u7684\u4e2d\u6587\u6587\u6863',
                subtitle=u'\u4e2d\u6587\u6587\u6863',
                arg=docInfo['href'],
                autocomplete=docInfo['id'],
                valid=True)
            if 'enHref' in docInfo.keys():
                wf.add_item(
                    title=docInfo['name'] + '\'s english document',
                    subtitle='English document',
                    arg=docInfo['enHref'],
                    autocomplete=docInfo['id'],
                    valid=True)
    else:
        wf.add_item(
            title='查询结果为空😂...',
            subtitle='按Enter可以到阿里中间件官网查询~',
            arg='http://mw.alibaba-inc.com/doc.html',
            valid=True)
    return wf


def search(searchStr, list):
    if len(searchStr) <= 0:
        return list

    startMatchs = []
    contains = []
    for item in list:
        if item['id'].startswith(searchStr):
            startMatchs.append(item)
        elif searchStr in item['id']:
            contains.append(item)

    return startMatchs + contains


