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
    # added via `Workflow3(libraries=...)`


    # Get args from Workflow3, already in normalized Unicode.
    # This is also necessary for "magic" arguments to work.
    args = wf.args

    # Do stuff here ...

    # Add an item to Alfred feedback
    if len(args) > 0 :
        id = args[0].strip()
        if len(id) > 0 :
            wf.add_item(title='新建变更',subtitle='新建一个变更',arg = 'https://cd.aone.alibaba-inc.com/ec/project/cr/index?_app_id_='+id,valid=True)
            wf.add_item(title='变更页面',subtitle='Aone 变更页面',arg = 'https://cd.aone.alibaba-inc.com/ec/app/'+id+'/app/cr/list',valid=True)
            wf.add_item(title='发布页面',subtitle='Aone 发布页面',arg = 'https://cd.aone.alibaba-inc.com/ec/app/'+id+'/mix/publish',valid=True)
            wf.add_item(title='概述页面',subtitle='Aone 概述页面',arg = 'https://app.aone.alibaba-inc.com/appcenter/app/detail?appId=145044'+id,valid=True)
        else :
            wf.add_item('请输入完整的应用AoneID')
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