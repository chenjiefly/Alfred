#!/usr/bin/python
# encoding: utf-8
import getAppId
from ..utils import LogUtil, cacheUtil

# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3
import sys

reload(sys)
sys.setdefaultencoding('utf8')


# 1. 获取数据
def getData(searchStr, wf):
    return wf.cached_data('$___app_' + searchStr, lambda: getAppId.getAppInfo(searchStr), max_age=604800)


# 2. 处理异常
def onException(searchStr=None, wf=None):
    wf.add_item(title='登录态失效，请按Enter键登录之后重试~',
                subtitle='按Enter可以到Aone官网获取登录态',
                arg='https://s.aone.alibaba-inc.com/services/search?keyword=' + searchStr,
                icon="/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns",
                valid=True)
    wf.add_item("")
    return wf


# 3. 解析数据
def parseData(searchStr, wf, data):
    if len(data) > 0:
        for appInfo in data:
            id = str(appInfo['id'])
            if appInfo['name'] == searchStr:
                wf.add_item(
                    title=u'\u6253\u5f00\u53d1\u5e03\u9875          ' + appInfo['name'] + '  ' + appInfo['owner'],
                    subtitle=appInfo['level'] + '  ' + appInfo['deptName'],
                    arg='https://cd.aone.alibaba-inc.com/ec/app/' + id + '/mix/publish',
                    autocomplete=appInfo['name'],
                    valid=True)
                wf.add_item(
                    title=u'\u65b0\u5efa\u53d8\u66f4              ' + appInfo['name'] + '  ' + appInfo['owner'],
                    subtitle=appInfo['level'] + '  ' + appInfo['deptName'],
                    arg='https://cd.aone.alibaba-inc.com/ec/project/cr/index?appId=' + id,
                    autocomplete=appInfo['name'],
                    valid=True)
                wf.add_item(
                    title=u'\u6253\u5f00\u53d8\u66f4\u9875          ' + appInfo['name'] + '  ' + appInfo['owner'],
                    subtitle=appInfo['level'] + '  ' + appInfo['deptName'],
                    arg='https://cd.aone.alibaba-inc.com/ec/app/' + id + '/app/cr/list',
                    autocomplete=appInfo['name'],
                    valid=True)
                wf.add_item(
                    title=u'\u6253\u5f00\u6982\u8ff0\u9875          ' + appInfo['name'] + '  ' + appInfo['owner'],
                    subtitle=appInfo['level'] + '  ' + appInfo['deptName'],
                    arg='https://app.aone.alibaba-inc.com/appcenter/app/detail?appId=' + id,
                    autocomplete=appInfo['name'],
                    valid=True)
            else:
                wf.add_item(
                    title=appInfo['name'] + '  ' + appInfo['owner'],
                    subtitle=appInfo['level'] + '  ' + appInfo['deptName'],
                    arg='https://cd.aone.alibaba-inc.com/ec/app/' + id + '/mix/publish',
                    autocomplete=appInfo['name'],
                    valid=True)
    else:
        wf.add_item(
            title='查询结果为空 😭...',
            subtitle='按Enter可以到Aone官网查询哦~ ',
            arg='https://s.aone.alibaba-inc.com/services/search?keyword=' + searchStr,
            icon="/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns",
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
    # args = ['cngoc']

    # Do stuff here ...

    if len(args) > 0:
        searchStr = args[0].strip().lower()
        data = []
        try:
            data = getData(searchStr, wf)
        except:
            # 异常后面有空在细化，暂时全归类成获取session失败
            LogUtil.error("appSearch exception ", {"arg": str(args)})
            wf = onException(searchStr, wf)
        else:
            if len(data) > 0:
                wf = parseData(searchStr, wf, data)
            else:
                wf.add_item('请输入应用名,支持模糊查询哦~  (搜索二方库请输入关键字lib)')
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
    sys.exit(wf.run(main))
