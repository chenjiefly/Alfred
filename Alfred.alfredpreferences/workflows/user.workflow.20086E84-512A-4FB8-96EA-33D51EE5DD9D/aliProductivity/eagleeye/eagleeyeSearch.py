import common
import json
from ..utils import httpUtil,cacheUtil

url = 'https://eagleeye-console.alibaba-inc.com/api/index.json?action=TraceAction&eventSubmitDoAppSearch=1'
mainUrl = 'https://eagleeye-console.alibaba-inc.com'
#mainUrl = url

def getParams(str):
    params={}
    params['param'] = str
    return params

def getHeader(cookies):
    header = {}

    cookies['dauth_proxy_token_name'] = 'SSO_TOKEN'
    cookies['dauth_proxy_uri_patterns'] = 'sendBucSSOToken.do%2CbucSSOLogout.do'
    cookies['dauth_proxy_back_name'] = 'BACK_URL'

    if 'XSRF-TOKEN' in cookies:
        header['x-xsrf-token']=cookies['XSRF-TOKEN']
    header['origin']='https://eagleeye-console.alibaba-inc.com'
    header['referer']='https://eagleeye-console.alibaba-inc.com/trace?pid=cngoc:cngochost&regionId=cn-hangzhou'
    header['x-forwarded-aliyunregionid']='cn-hangzhou'

    return header

def isLoginInvalidate(res):
    response = json.loads(res.text)
    if 'code' in response.keys():
        if response['code'] == 'ConsoleNeedLogin':
            return True
    return False

def tryLogin():
    return httpUtil.get(mainUrl,mainUrl,isRepeat=True)

def search(searchStr,isRepeat=False):
    res = httpUtil.post(url,mainUrl,params=getParams(searchStr),getHeader = getHeader,isLoginInvalidate=isLoginInvalidate,tryLogin = tryLogin)
    if isLoginInvalidate(res):
        print('login failure')
        return
    response = json.loads(res.text)
    if response['success'] == True:
        try:
            return response['data']['data']['result']
        except:
            return []

if __name__ == '__main__':
    #search('cngcp')
    # res = httpUtil.get(url1,url1,isRepeat=True)
    # print(res.text)
    # res = httpUtil.get(url2,url2,isRepeat=True)
    # print(res.text)
    # res = httpUtil.get(url3,url3,isRepeat=True)
    # print(res.text)

    #print(tryLogin())
    cacheUtil.remove()
    print(search('cngcp'))