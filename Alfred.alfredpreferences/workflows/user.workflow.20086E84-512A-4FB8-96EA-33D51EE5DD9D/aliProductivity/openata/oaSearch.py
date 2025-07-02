#!/usr/bin/python
# encoding: utf-8
import sys,os
from ..utils import cacheUtil
import getArticle
# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3

reload(sys)
sys.setdefaultencoding('utf8')
baseUrl = 'https://open.atatech.org/articles/'
# 1. 获取数据
def getData(searchStr, wf):
    return wf.cached_data('$___oa_' + searchStr, lambda: getArticle.search(searchStr), max_age=60)

# 2. 处理异常
def onException(searchStr=None, wf=None):
    wf.add_item(title='出现异常，请检查参数是否拼写正常',
                subtitle='点击去openAta页面',
                arg='https://open.atatech.org/',
                icon="/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns",
                valid=True)
    wf.add_item("")
    return wf


# 3. 解析数据
def parseData(wf, data, searchStr):
    if len(data) > 0:
        for article in data:
            wf.add_item(
                title=article[0],
                arg=baseUrl+str(article[1]),
                subtitle='请按回车以查看详情',
                valid=True)
    else:
        wf.add_item(
            title='查询结果为空 😭...',
            subtitle='按Enter可以到openAta页面~ ',
            arg='https://open.atatech.org/',
            icon="/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns",
            valid=True)
    return wf


