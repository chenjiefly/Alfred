#!/usr/bin/python
# encoding: utf-8
import common
from logging import NullHandler
import normandySearch
import normandySearchIpByGroup, ipDetail
import sys
import traceback
from aliProductivity.utils import cacheUtil
from aliProductivity.utils import LogUtil
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3


# 1. 获取数据
def getData(searchStr, wf):
    return wf.cached_data('$___normandy_' + searchStr, lambda: normandySearch.search(searchStr), max_age=1)


# 2. 处理异常
def onException(searchStr, wf):
    wf.add_item(title='登录态失效，请按Enter键登录之后重试~',
                subtitle='按Enter可以到诺曼底官网获取登录态',
                arg='https://n.alibaba-inc.com',
                icon="/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns",
                valid=True)
    return wf


# 3. 解析数据
def parseData(searchStr, wf, data):
    if len(data) <= 0:
        wf.add_item(
            title='未查询到数据',
            subtitle='请检查搜索关键字，或者按ENTER进入官网查询',
            arg='https://n.alibaba-inc.com',
            valid=True)

    for d in data:
        type = d['type']
        if type == u'\u5206\u7ec4':
            groupName = d['name']
            if groupName == searchStr:
                normandySearchIpByGroup.resolveData(groupName, wf)
            else:
                wf.add_item(
                    title=d['name'],
                    subtitle='按ENTER键,打开分组详情,按TAB键搜索分组下IP',
                    arg='https://n.alibaba-inc.com' + d['detailUrl'],
                    autocomplete=d['name'],
                    valid=True)
        elif type == u'\u4e3b\u673a':
            ip = d['name']
            if ip:
                ipDetail.resolveData(ip, wf)
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


if __name__ == '__main__':
    # Create a global `Workflow3` object
    wf = Workflow3()
    sys.argv.append('33.4.22.222')
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.exit(wf.run(main))
