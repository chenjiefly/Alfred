#!/usr/bin/python
# encoding: utf-8
import common
import debugApply
import re
from utils import cacheUtil
from utils import LogUtil
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3

# 1. 执行命令
pattern = '^(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])$'
def execute(ip,wf):
    match = re.match(pattern,ip)
    if match:
        return debugApply.apply(ip)
    else:
        return {'msg':'invalidateIp'}

# 2. 处理异常
def onException(ip ,wf):
    wf.add_item(title='获取登录态失败，请按Enter键手动申请~',
        subtitle= '按Enter可以到诺曼底官网手动申请Debug',
        arg = 'https://n.alibaba-inc.com/ops/action/debug/java?spm=a1znmd.11230159.page.9.25162889eC7sl5',
        icon = "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns",
        valid=True)
    return wf

# 3. 解析数据
def parseData(ip ,wf ,result):
    msg = result['msg']
    if msg == 'invalidateIp':
        wf.add_item(title='请输入正确的IP地址~',
            valid=False)
    elif msg == 'autoLoginFail':
        wf.add_item(title='获取登录态失败，请按Enter键手动申请~',
            subtitle= '按Enter可以到诺曼底官网手动申请Debug',
            arg = 'https://n.alibaba-inc.com/ops/action/debug/java?spm=a1znmd.11230159.page.9.25162889eC7sl5',
            icon = "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns",
            valid=True)
    elif msg == 'applyDebugFail':
        wf.add_item(title='申请Debug失败,原因: '+result['message'],
            subtitle= '按Enter可以到诺曼底官网手动申请Debug',
            arg = 'https://n.alibaba-inc.com/ops/action/debug/java?spm=a1znmd.11230159.page.9.25162889eC7sl5',
            icon = "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns",
            valid=True)
    elif msg == 'success':
        wf.add_item(title='申请成功，查看任务状态~',
            subtitle= '恭喜您，Debug申请成功，按Enter键，进行下一步~',
            arg = 'https://npsp.alibaba-inc.com/paas/onlinedebug/detail.htm?id='+str(result['taskId']),
            valid=True)
        wf.add_item(title='申请成功，进入邮箱获取分配地址~',
            subtitle= '恭喜您，Debug申请成功，按Enter键，进行下一步~',
            arg = 'https://mail.alibaba-inc.com/alimail/',
            icon='./icon/mail.png',
            valid=True)

def main(wf):
    # The Workflow3 instance will be passed to the function
    # you call from `Workflow3.run`.
    # Not super useful, as the `wf` object created in
    # the `if __name__ ...` clause below is global...
    #
    # Your imports go here if you want to catch import errors, which
    # is not a bad idea, or if the modules/packages are in a directory
    # added via `Workflow3(libraries=...)`

    # Get args from Workflow3, already in normalized Unicode.
    # This is also necessary for "magic" arguments to work.
    cacheUtil.remove()
    args = wf.args
    # Add an item to Alfred feedback
    if len(args) > 0 and not args[0].isspace():
        cacheUtil.put('wf',wf)
        ip = args[0].strip().lower()
        result = {}
        try:
            result = execute(ip,wf)
        except:
            LogUtil.error("debugApply exception ",{"ip":ip})
            wf = onException(ip,wf)
        else:
            parseData(ip,wf,result)

    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but subsequent calls
    # are ignored (otherwise the JSON sent to Alfred would be invalid).
    wf.send_feedback()
    cacheUtil.remove()

if __name__ == '__main__':
    # Create a global `Workflow3` object
    wf = Workflow3()
    sys.argv.append('33.4.22.222.123')
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.exit(wf.run(main))



