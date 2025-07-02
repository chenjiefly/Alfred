# -*- coding: utf-8 -*-
import sys, os

reload(sys)
sys.setdefaultencoding('utf8')
from workflow import Workflow3
from aliProductivity import allException
from aliProductivity.utils import cacheUtil,LogUtil

params=str.split(sys.argv[1],".")
m = __import__("aliProductivity."+params[0],fromlist=[params[1]])




def entrance(wf):
    # Create a global `Workflow3` object
    # Do stuff here ...
    try:
        cacheUtil.put('wf', wf)
        args = wf.args[1:]
        if len(args) > 0:
            searchStr = args[0].strip().lower()
            try:
                module = getattr(m, params[1])
                data = module.getData(searchStr=searchStr, wf=wf)
            except allException.FuncException as e:
                LogUtil.error('main.exception: '+str(wf.args))
                wf.add_item(title='业务异常', subtitle= str(type(e))+':'+e.message)
                m.onException(searchStr=searchStr, wf=wf)
            except BaseException as e:
                LogUtil.error('main.exception: '+str(wf.args))
                wf.add_item(title='系统异常', subtitle= str(type(e))+':'+e.message)
            else:
                if len(data) > 0:
                    module.parseData(wf=wf, data=data, searchStr=searchStr)
                else:
                    wf.add_item(title='查询结果为空，请保证输入有效')
    except Exception as e:
        LogUtil.error('main.exception: '+str(wf.args))
        wf.add_item(title='请检查配置是否正确',  subtitle= str(type(e))+':'+e.message)
    finally:
        wf.send_feedback()
        cacheUtil.remove()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(entrance))
