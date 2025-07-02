#!/usr/bin/python
# encoding: utf-8
import sys,os
import common
from utils import cacheUtil
from getAdict import getAdictInfo
# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3

reload(sys)
sys.setdefaultencoding('utf8')

# 1. 获取数据
def getData(searchStr, wf):
    #return wf.cached_data('$___adict_' + searchStr, lambda:getAdict.getAdictInfo(searchStr), max_age=10)
    return getAdictInfo(searchStr)

# 2. 处理异常
def onException(searchStr=None, wf=None):
    wf.add_item(title='出现异常，请检查缩写是否拼写正常',
                subtitle='点击去页面查询',
                arg='https://yida.alibaba-inc.com/alibaba/web/APP_ZXGJVX4ZRGTUBU8FFZ1O/inst/homepage',
                icon="/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns",
                valid=True)
    wf.add_item("")
    return wf


# 3. 解析数据
def parseData(wf, data, searchStr):
    if len(data) > 0:
        for adictInfo in data:
            wf.add_item(
                title=adictInfo['fullName'],
                arg='https://yida.alibaba-inc.com/alibaba/web/' + adictInfo[
                    'appType'] + '/inst/formEdit.html?formInstId=' + adictInfo['formInstanceId'] + '&formUuid=' +
                    adictInfo['formUuid'],
                subtitle = '['+adictInfo['classify']+ '-' + adictInfo['subClassify']+']  ' + str(adictInfo['lable']),
                autocomplete = adictInfo['adictName'],
                valid=True)
            wf.add_item(
                title= '   - ' +adictInfo['description'],
                arg='https://yida.alibaba-inc.com/alibaba/web/' + adictInfo[
                    'appType'] + '/inst/formEdit.html?formInstId=' + adictInfo['formInstanceId'] + '&formUuid=' +
                    adictInfo['formUuid'],
                subtitle=adictInfo.get('comment'),
                autocomplete=adictInfo['adictName'],
                valid=True)
    else:
        wf.add_item(
            title='查询结果为空 😭...',
            subtitle='按Enter可以到宜搭官网查询哦~ ',
            arg='https://yida.alibaba-inc.com/alibaba/web/APP_ZXGJVX4ZRGTUBU8FFZ1O/inst/homepage',
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
    # args = ['ae']
    # Do stuff here ...
    if len(args) > 0:
        searchStr = args[0].strip().lower()
        try:
            data = getData(searchStr, wf)
        except:
            # 异常后面有空在细化，暂时全归类成获取session失败
            # print(traceback.format_exc())
            wf = onException(searchStr, wf)
        else:
            if len(data) > 0:
                wf = parseData(wf, data)
            else:
                wf.add_item('请输入名词缩写,不支持模糊查询 ')
    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but subsequent calls
    # are ignored (otherwise the JSON sent to Alfred would be invalid).



if __name__ == '__main__':

    # Create a global `Workflow3` object
    wf = Workflow3()
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.exit(wf.run(main))


