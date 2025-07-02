#!/usr/bin/python
# encoding: utf-8
import common
from ..utils import LogUtil, cacheUtil
import aliYunAccount, getAliYunMainAccountList
import sys
import traceback
# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3
import sys

reload(sys)
sys.setdefaultencoding('utf8')


# 1. 获取数据
def getData(searchStr, wf):
    return wf.cached_data('$___AliYunAcount_', lambda: aliYunAccount.getAccount(), max_age=1)


# 2. 处理异常
def onException(searchStr, wf):
    wf.add_item(title='登录态失效，请按Enter键登录之后重试~',
                subtitle='按Enter进入诺曼底云账号管理页面',
                arg='https://n.alibaba-inc.com/cloudAccountManage/providerManageNew',
                icon="/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns",
                valid=True)
    return wf


# 3. 解析数据
def parseData(searchStr, wf, data):
    if len(data) > 0:
        for accountInfo in data:
            accountType = accountInfo['accountType']
            url = accountInfo['loginUrl']
            # if accountType == 'main':
            #     url = getAliYunMainAccountList.getLoginUrl(accountInfo['id'])
            # elif accountType == 'sub':
            #     url = accountInfo['loginUrl']
            if url and not url.isspace():
                wf.add_item(
                    title=accountInfo['name'],
                    subtitle=accountInfo['code'] + '  ' + accountInfo['type'] + '  owner:' + accountInfo['ownerName'],
                    arg=url,
                    autocomplete=accountInfo['name'],
                    valid=True)
    else:
        wf.add_item(
            title='查询结果为空 😭...',
            subtitle='按Enter进入诺曼底云账号管理页面',
            arg='https://n.alibaba-inc.com/cloudAccountManage/providerManageNew',
            valid=True)
    return wf

#
# def main(wf):
#     # The Workflow3 instance will be passed to the function
#     # you call from `Workflow3.run`.
#     # Not super useful, as the `wf` object created in
#     # the `if __name__ ...` clause below is global...
#     #
#     # Your imports go here if you want to catch import errors, which
#     # is not a bad idea, or if the modules/packages are in a directory
#     # added via `Workflow3(libraries=...)
#
#     # Get args from Workflow3, already in normalized Unicode.
#     # This is also necessary for "magic" arguments to work.
#     cacheUtil.put('wf', wf)
#     args = wf.args
#
#     # Do stuff here ...
#     data = []
#     searchStr = ''
#     try:
#         data = getData(searchStr, wf)
#     except:
#         # 异常后面有空在细化，暂时全归类成获取session失败
#         LogUtil.error(' aliYunLogin exception:')
#         wf = onException(searchStr, wf)
#     else:
#         wf = parseData(searchStr, wf, data)
#
#     # Send output to Alfred. You can only call this once.
#     # Well, you *can* call it multiple times, but subsequent calls
#     # are ignored (otherwise the JSON sent to Alfred would be invalid).
#     wf.send_feedback()
#     cacheUtil.remove()


if __name__ == '__main__':
    # Create a global `Workflow3` object
    wf = Workflow3()
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.argv.append('cnls')
    sys.exit(wf.run(main))
