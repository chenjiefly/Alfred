import common
import json
from utils import httpUtil,cacheUtil

url = 'https://npsp.alibaba-inc.com/paas/onlinedebug/submit.json'
mainUrl = 'https://n.alibaba-inc.com/ops/action/debug/java'
mainUrl = url

def getParams(ip):
    params={}
    params['description'] = ip
    params['deadline'] = 1
    params['prehosts'] = '[{"ip":"'+ip+'","port":"8000"}]'
    params['host'] = '["'+ip+'"]'
    return params

def getHeader(cookies):
    header = {}
    return header

def isLoginInvalidate(res):
    try:
        text = res.text
        response = json.loads(text)
        return False
    except ValueError:
        return True
    return True

def tryLogin():
    return httpUtil.get(mainUrl,mainUrl,isRepeat=True)

def apply(ip,isRepeat=False):
    res = httpUtil.post(url,mainUrl,params=getParams(ip),getHeader = getHeader,isLoginInvalidate=isLoginInvalidate,tryLogin = tryLogin)

    if isLoginInvalidate(res):
        if not isRepeat:
            tryLogin()
            return apply(ip,True)
        else:
            return {'msg':'autoLoginFail'}
    result = {}
    msg = ''
    response = json.loads(res.text)
    if response['success'] == True:
        msg = 'success'
        result['taskId'] = response['data']
    else:
        msg = 'applyDebugFail'
        result['message'] = response['message']
    result['msg'] = msg
    return result

if __name__ == '__main__':
    cacheUtil.remove()
    print(apply('12.12.12.12'))