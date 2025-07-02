#!/usr/bin/python
# encoding: utf-8

import sys

# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3
from utils import cacheUtil

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
    args = wf.args
    wf.clean_cache()
    # Do stuff here ...

    # Add an item to Alfred feedback
    if len(args) > 0 :
        searchStr = args[0].strip()
        if len(searchStr) > 0 :
            appInfos = wf.cached_data('$___app_'+searchStr,lambda :getAppId.getAppInfo(searchStr),max_age=86400)
            if len(appInfos) > 0:
                for appInfo in appInfos:
                    id = str(appInfo['id'])
                    if appInfo['name'] == searchStr:
                        wf.add_item(
                            title= u'\u6253\u5f00\u53d1\u5e03\u9875          '+ appInfo['name'] + '  '+appInfo['owner'],
                            subtitle=  appInfo['level'] + '  '+ appInfo['deptName'],
                            arg = 'https://cd.aone.alibaba-inc.com/ec/app/'+id+'/mix/publish',
                            autocomplete = appInfo['name'],
                            valid=True)
                        wf.add_item(
                            title= u'\u65b0\u5efa\u53d8\u66f4              ' + appInfo['name'] + '  '+appInfo['owner'],
                            subtitle=  appInfo['level'] + '  '+ appInfo['deptName'],
                            arg = 'https://cd.aone.alibaba-inc.com/ec/project/cr/index?appId='+id,
                            autocomplete = appInfo['name'],
                            valid=True)
                        wf.add_item(
                            title= u'\u6253\u5f00\u53d8\u66f4\u9875          ' +appInfo['name'] + '  '+appInfo['owner'],
                            subtitle= appInfo['level'] + '  '+ appInfo['deptName'],
                            arg = 'https://cd.aone.alibaba-inc.com/ec/app/'+id+'/app/cr/list',
                            autocomplete = appInfo['name'],
                            valid=True)
                        wf.add_item(
                            title= u'\u6253\u5f00\u6982\u8ff0\u9875          ' +appInfo['name'] + '  '+appInfo['owner'],
                            subtitle= appInfo['level'] + '  '+ appInfo['deptName'],
                            arg = 'https://app.aone.alibaba-inc.com/appcenter/app/detail?appId='+id,
                            autocomplete = appInfo['name'],
                            valid=True)
                    else :
                        wf.add_item(
                            title= appInfo['name'] + '  '+appInfo['owner'],
                            subtitle=  appInfo['level'] + '  '+ appInfo['deptName'],
                            arg = 'https://cd.aone.alibaba-inc.com/ec/app/'+id+'/mix/publish',
                            autocomplete = appInfo['name'],
                            valid=True)
            else :
                wf.add_item(
                    title='查询结果为空 😭...',
                    subtitle= '按Enter可以到Aone官网查询哦~ ',
                    arg = 'https://s.aone.alibaba-inc.com/services/search?keyword='+searchStr,
                    valid=True)
        else :
            wf.add_item('请输入应用名,支持模糊查询哦~  (搜索二方库请输入关键字a.lib)')

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