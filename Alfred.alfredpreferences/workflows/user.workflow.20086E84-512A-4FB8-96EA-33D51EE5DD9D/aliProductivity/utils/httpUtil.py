# encoding: utf-8
import common
import requests
import json
from utils import cookieUtil
from utils import employeeIdCache
from utils import LogUtil
from utils import cacheUtil

def get(url,mainUrl,params={},isRepeat=False,isLoginInvalidate=None,tryLogin=None):
    res = callWithLogin(url,mainUrl,getInvock,params,None,isRepeat,isLoginInvalidate,tryLogin)
    return res

def cleanRedirectUrl(url,redirectUrl):
    if not url and not redirectUrl:
        return
    if redirectUrl.startswith('http'):
        return redirectUrl
    index = url.find('/',9)
    if index < 0:
        return url + redirectUrl

    return url[:index] + redirectUrl

def needExeRedirectUrl(redirectUrl):
    # 已经处理过的不用处理
    redirectUrls = cacheUtil.get('redirectUrls')
    if not redirectUrls:
        redirectUrls = []
        cacheUtil.put('redirectUrls',redirectUrls)

    url = redirectUrl
    if '?' in url:
        index = url.index('?')
        url = url[0:index]

    if url in redirectUrls:
        return False
    else:
        redirectUrls.append(url)
        return True


def post(url,mainUrl,params={},getHeader=None,isRepeat=False,isLoginInvalidate=None,tryLogin=None):
    return callWithLogin(url,mainUrl,postInvock,params,getHeader,isRepeat,isLoginInvalidate,tryLogin)

def callWithLogin(url,mainUrl,callMethod,params={},getHeader=None,isRepeat=False,isLoginInvalidate=None,tryLogin=None):
    res = invoke(url,mainUrl,callMethod,params,getHeader)

    if not isRepeat:
        if isLoginInvalidate and isLoginInvalidate(res) and tryLogin:
            tryLogin()
            res = invoke(url,mainUrl,callMethod,params,getHeader)
    return res

def invoke(url,mainUrl,callMethod,params={},getHeader=None,lastTry=False):
    cookies = cookieUtil.get(mainUrl)
    res = callMethod(url,cookies,params,getHeader)
    if res and res.status_code == 200 :
        return res

    if url != mainUrl:
        # 先通过mainUrl获取登录态，再调用url，获取数据
        res = invoke(mainUrl,mainUrl,callMethod)
        return callMethod(url,cookies,params,getHeader)

    if res and (res.status_code in [302,301,307] )and not lastTry:
        redirectUrl = res.headers['location']
        redirectUrl = cleanRedirectUrl(mainUrl,redirectUrl)
        LogUtil.info('redirectUrl : ' + redirectUrl)

        LogUtil.info('redirectUrl : '
                     + '\n   -------------  orgUrl : '+ url
                     + '\n   -------------  redirectUrl : ' + redirectUrl)

        if needExeRedirectUrl(redirectUrl):
            return invoke(redirectUrl,redirectUrl,callMethod,{},getHeader)
        else:
            return invoke(url,mainUrl,callMethod,params,getHeader,lastTry=True)
    return res

# 缓存工号
def cacheEmployeeId(cookies):
    if len(cookies) == 0:
        return
    try:
        if 'kos_user_id' in cookies:
            employeeId = cookies['kos_user_id']
            employeeIdCache.cache(employeeId)
    except:
        LogUtil.error("httpUtil.cacheEmployeeId exception ",{"cookies":cookies})

def getSession():
    session = cacheUtil.get('session')
    if session:
        session = requests.session
        cacheUtil.put('session',session)
    return requests.session()

# 执行post请求
def postInvock(url,cookies,params={},getHeader=None):
    header={}
    if getHeader != None:
        header = getHeader(cookies)

    return getSession().post(url,data=params,cookies=cookies,headers=header)

# 执行get请求
def getInvock(url,cookies,params={},getHeader=None):
    header={}
    if getHeader != None:
        header = getHeader(cookies)

    res = getSession().get(url,params=params, cookies=cookies,headers=header,allow_redirects=False)
    set_cookies = requests.utils.dict_from_cookiejar(res.cookies)

    if set_cookies:
        cache_set_cookies = cacheUtil.get('set_cookies')
        if not cache_set_cookies:
            cacheUtil.put('set_cookies',set_cookies)
        else :
            cache_set_cookies.update(set_cookies)
            cacheUtil.put('set_cookies',cache_set_cookies)

    return res

def isSameUrl(url1,url2):
    url1 = cleanUrl(url1)
    url2 = cleanUrl(url2)
    return url1 == url2

def cleanUrl(url):
    if '?' in url:
        index = url.index('?')
        return url[0:index]
    return url

# 尝试拿到最新的cookie，如果cookie没有更新则返回false，否则返回True
def tryGetValidateCookie(reqUrl,mainUrl,r,cookies,isLoginInvalidate,tryLogin):
    if isLoginInvalidate :
        if not isLoginInvalidate(r):
            return r
        else:
            r = tryLogin()

    nowUrl = r.url
    if isSameUrl(reqUrl,nowUrl):
        return None

    logTokenDict = getLoginToken(r,mainUrl)
    if logTokenDict :
        for key in logTokenDict.keys():
            cookies[key] = logTokenDict[key]
        cookieUtil.update(mainUrl,cookies)
        return True
    return False

def getJson(url,mainUrl,params={}):
    res = get(url,mainUrl,params)
    if res.status_code == 200 :
        return json.loads(res.text,encoding='utf-8')
    raise Exception('http call exception,url='+url+',parmas='+str(params)+',status_code='+str(res.status_code))

def getLoginToken(httpResponse,mainUrl):

    if isPreLogin(httpResponse):
        # httpResponse = get(httpResponse.url,httpResponse.url,isRepeat=True)
        httpResponse = tryAutoLogin(httpResponse)
        if mainUrl[8:] in httpResponse.url:
            requestCoockie = requests.utils.dict_from_cookiejar(httpResponse.request._cookies)
            responseCookie = requests.utils.dict_from_cookiejar(httpResponse.cookies)
            return  dict(requestCoockie.items()+responseCookie.items())
    if mainUrl[8:] in httpResponse.url:
        requestCoockie = requests.utils.dict_from_cookiejar(httpResponse.request._cookies)
        responseCookie = requests.utils.dict_from_cookiejar(httpResponse.cookies)
        return  dict(requestCoockie.items()+responseCookie.items())

    return resolveCookies(httpResponse)

def isPreLogin(response):
    url = response.url
    if 'https://login.alibaba-inc.com/preLogin2.htm' in url:
        return True
    return False

def tryAutoLogin(response):
    r = tryAutoLoginByUrl(response.url)
    if r:
        return r
    history = response.history
    history = reversed(history)
    for oldHttpResponse in history:
        url = oldHttpResponse.url
        r = tryAutoLoginByUrl(url)
        if r:
            return r
    return response


def tryAutoLoginByUrl(url):
    if 'https://login.alibaba-inc.com/ssoLogin.htm' in url:
        return get(url,url,isRepeat=True)
    elif 'https://dauth.alibaba-inc.com/sso/login.htm' in url:
        return get(url,url,isRepeat=True)
    return None

def isSSOReq(response):
    if response.is_redirect and 'sendBucSSOToken' in response.url:
        return True
    return False

def resolveCookies(response):
    cookie = resolveCookiesByResponse(response)
    if len(cookie) > 0:
        return cookie

    history = response.history
    for oldHttpResponse in history:
        cookie = resolveCookiesByResponse(oldHttpResponse)
        if len(cookie) > 0:
            return cookie

def resolveCookiesByResponse(response):
    if isSSOReq(response):
        headers = response.raw.headers
        set_cookies = headers.getlist('Set-Cookie')
        return resolveCookie(set_cookies)
    return {}

def resolveCookie(cookies):
    tokenDict = {}
    for cookie in cookies:
        item = cookie.split('=')
        key = item[0]
        value = item[1]
        index = value.index(";")
        if index > 0 :
            value = value[0:index]
        tokenDict[key] = value
    return tokenDict

def autoLogin(url):
    httpResponse = get(url,url)
    tokenDict = getLoginToken(httpResponse,url)
    print(tokenDict)
    print(httpResponse)

def autoRedirect(url):
    cookies = cookieUtil.get(url)
    res = getSession().get(url, cookies=cookies,allow_redirects=False)
    if res.status_code == 302:
        location = res.headers['location']
        print(location)
        return autoRedirect(location)
    return res

if __name__ == '__main__':
    url = 'https://dauth.alibaba-inc.com/sso/login.htm?back_url=https%3A%2F%2Feagleeye-console.alibaba-inc.com%2F&app_key=af44a416b5b54aab9542070d15ff5220' 
    a = {
        '1':'a',
        '2':'a'
        }
    b = {
        '1':'b',
        '3':'b'
        }
    a.update(b)
    print(a)
    






