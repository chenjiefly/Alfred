#!/usr/bin/python
# encoding: utf-8
import common
import workSearch
import sys
import traceback
from utils import cacheUtil

# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3
import sys
reload(sys)
sys.setdefaultencoding('utf8')


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
    cacheUtil.put('wf',wf)
    args = wf.args
    # Add an item to Alfred feedback
    searchStr = ''
    if len(args) > 0 :
        searchStr = args[0].strip().lower()
    workSearch.resolveData(searchStr,wf)

    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but subsequent calls
    # are ignored (otherwise the JSON sent to Alfred would be invalid).
    wf.send_feedback()
    cacheUtil.remove()

def search(searchStr , list):
    if len(searchStr) <= 0 :
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
    sys.argv.append('山乘')
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.exit(wf.run(main))



