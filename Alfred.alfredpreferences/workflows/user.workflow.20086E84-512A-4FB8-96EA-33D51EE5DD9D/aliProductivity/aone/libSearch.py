#!/usr/bin/python
# encoding: utf-8

import getLibId
import traceback

# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3

from aliProductivity.utils import cacheUtil
import sys

reload(sys)
sys.setdefaultencoding('utf8')


# 1. 获取数据
def getData(searchStr, wf):
    return wf.cached_data('$___lib_' + searchStr, lambda: getLibId.getLibInfo(searchStr), max_age=1000)


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
        for libInfo in data:
            id = str(libInfo['id'])
            if libInfo['name'] == searchStr:
                wf.add_item(
                    title=u'\u6253\u5f00\u53d1\u5e03\u9875 ' + libInfo['name'],
                    subtitle=u'\u005b\u4e8c\u65b9\u5e93\u005d    ' + libInfo['deptName'],
                    arg='https://cd.aone.alibaba-inc.com/ec/app/' + id + '/lib/mix/publish',
                    autocomplete=libInfo['name'],
                    valid=True)
                wf.add_item(
                    title=u'\u65b0\u5efa\u53d8\u66f4   ' + libInfo['name'],
                    subtitle=u'\u005b\u4e8c\u65b9\u5e93\u005d    ' + libInfo['deptName'],
                    arg='https://cd.aone.alibaba-inc.com/ec/project/cr/index?type=LIB&appId=' + id,
                    autocomplete=libInfo['name'],
                    valid=True)
                wf.add_item(
                    title=u'\u6253\u5f00\u53d8\u66f4\u9875  ' + libInfo['name'],
                    subtitle=u'\u005b\u4e8c\u65b9\u5e93\u005d    ' + libInfo['deptName'],
                    arg='https://cd.aone.alibaba-inc.com/ec/app/' + id + '/lib/cr/list',
                    autocomplete=libInfo['name'],
                    valid=True)
                wf.add_item(
                    title=u'\u6253\u5f00\u6982\u8ff0\u9875  ' + libInfo['name'],
                    subtitle=u'\u005b\u4e8c\u65b9\u5e93\u005d    ' + libInfo['deptName'],
                    arg='https://app.aone.alibaba-inc.com/appcenter/lib/detail?libId=' + id,
                    autocomplete=libInfo['name'],
                    valid=True)
            else:
                wf.add_item(
                    title=libInfo['name'],
                    subtitle=u'\u005b\u4e8c\u65b9\u5e93\u005d    ' + libInfo['deptName'],
                    arg='https://cd.aone.alibaba-inc.com/ec/app/' + id + '/lib/mix/publish',
                    autocomplete=libInfo['name'],
                    valid=True)
    else:
        wf.add_item(
            title='查询结果为空 😭...',
            subtitle='按Enter可以到Aone官网查询哦~ ',
            arg='https://aone.alibaba-inc.com/appcenter/lib/list',
            valid=True)
    return wf


def main(wf):
    # The Workflow3 instance will be passed to the function
    # you call from `Workflow3.run`.
    # Not super useful, as the `wf` object created in
    # the `if __name__ ...` clause below is global...
    #
    # Your imports go here if you want to catch import errors, which
    # is not a bad idea, or if the modules/packages are in a directory
    # added via `Workflow3(libraries=...)

    # Get args from Workflow3, already in normalized Unicode.
    # This is also necessary for "magic" arguments to work.
    cacheUtil.put('wf', wf)
    args = wf.args

    # Do stuff here ...

    if len(args) > 0:
        searchStr = args[0].strip().lower()
        try:
            data = getData(searchStr, wf)
        except:
            # 异常后面有空在细化，暂时全归类成获取session失败
            print(traceback.format_exc())
            wf = onException(searchStr, wf)
        else:
            if len(searchStr) > 0:
                wf = parseData(searchStr, wf, data)
            else:
                wf.add_item('请输入应用名,支持模糊查询哦~  (搜索应用请输入关键字a)')

    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but subsequent calls
    # are ignored (otherwise the JSON sent to Alfred would be invalid).
    wf.send_feedback()
    cacheUtil.remove()


if __name__ == '__main__':
    # Create a global `Workflow3` object
    wf = Workflow3()
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.argv.append('cnls')
    sys.exit(wf.run(main))
