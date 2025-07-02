# encoding: utf-8

import json
import common
from pycookiecheat import chrome_cookies
from workflow import Workflow3
from utils import cacheUtil,LogUtil

def get(url):
    cookies = get_from_cache(url)
    if not cookies:
        cookies = get_from_chrome(url)
    cookies = fillCookies(cookies)
    #print(cookies)
    LogUtil.info('getCookies: '
                 + '\n   -------------  url : '+ url
                 + '\n   -------------  cookies: ' + json.dumps(cookies))
    return cookies

def fillCookies(cookies):
    cookiesNotEmpty = cookies and len(cookies) > 0
    setCookies = cacheUtil.get('set_cookies')
    setCookiesNotEmpty = setCookies and len(setCookies) > 0
    if cookiesNotEmpty and setCookiesNotEmpty:
        cookies.update(setCookies)
        return cookies

    if cookiesNotEmpty and not setCookiesNotEmpty:
        return cookies

    if not cookiesNotEmpty and  setCookiesNotEmpty:
        return setCookiesNotEmpty

    return {}

def appendIfNotExist(cookies , addCookies):
    if cookies and addCookies:
        for key in addCookies:
            if key not in cookies:
                cookies[key] = addCookies[key]

def update(url,cookies):
    wf = cacheUtil.get('wf')
    if wf:
        return wf.cached_data(cacheKey(url),lambda :cookies,max_age=600)

def get_from_chrome(url):
    return chrome_cookies(url)

def get_from_cache(url):
    wf = cacheUtil.get('wf')
    if wf:
        return wf.cached_data(cacheKey(url),max_age=600)

def cacheKey(url):
    if '?' in url:
        index = url.index('?')
        url = url[0:index]
    url = url.replace('/','#')
    return '$___cookie_'+url

if __name__ == '__main__':
    url='https://eagleeye-console.alibaba-inc.com/sendBucSSOToken.do?SSO_TOKEN=5e4c6e0bbcdd4778ad3a8b27db83130010b1f200&BACK_URL=https%3A%2F%2Feagleeye-console.alibaba-inc.com%2F:'
    
