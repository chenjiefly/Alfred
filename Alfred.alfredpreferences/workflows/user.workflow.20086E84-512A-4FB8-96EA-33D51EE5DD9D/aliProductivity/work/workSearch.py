# encoding: utf-8
from utils import httpUtil
import json
import workPersonInfo
import traceback
from utils import LogUtil

url = 'https://work.alibaba-inc.com/xservice/suggestionSearch.json?'
mainUrl = 'https://work.alibaba-inc.com'

def getWorkSearchData(searchStr):
    params = {
        "_csrf_token":"",
        "itemNumbers":"5",
        "historyNumbers":"10"
    }
    params['condition']=searchStr
    res = httpUtil.get(url,mainUrl,params,isLoginInvalidate=isLoginInvalidate,tryLogin=tryLogin)
    if res.status_code == 200 :
        response = json.loads(res.content,encoding='utf-8')
        if response['success'] == True:
            content = response['content']
            if 'items' in content.keys():
                return content['items']
    return {}

def tryLogin():
    return httpUtil.get(mainUrl,mainUrl,isRepeat=True)

def isLoginInvalidate(res):
    response = json.loads(res.content,encoding='utf-8')
    if 'errors' in response.keys():
        if 'SSOException' == response['errors'][0]['field']:
            return True
    return False


# 1. 获取数据
def getData(searchStr,wf):
    return wf.cached_data('$___work_'+searchStr,lambda :getWorkSearchData(searchStr),max_age=86400)

# 2. 处理异常
def onException(searchStr ,wf):
    wf.add_item(title='登录态失效，请按Enter键登录之后重试~',
                subtitle= '按Enter可以到官网获取登录态',
                arg = mainUrl,
                icon = "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns",
                valid=True)
    return wf

# 3. 解析数据
def parseData(searchStr ,wf ,data):
    if 'all_results' in data.keys():
        results = data['all_results']
        parseWebData(searchStr,wf,parseResults(results,u'web.\u5bfc\u822a'))
        parsePersonData(searchStr,wf,parseResults(results,'person'))
        #parseWebData(searchStr,wf,parseResults(results,'link'))
        #parseWordData(searchStr,wf,parseResults(results,'word'))
        parseHistoryData(searchStr,wf,parseResults(results,'history'))
        parseHotwordData(searchStr,wf,parseResults(results,'hotword'))
    lastResult(searchStr,wf)

def lastResult(searchStr,wf):
    if len(searchStr) > 0:
        wf.add_item(title= u'\u76f4\u63a5\u641c\u7d22\u5173\u952e\u5b57: '+searchStr,
            subtitle= u'\u6309\u0045\u004e\u0054\u0045\u0052\u952e\uff0c\u5230\u963f\u91cc\u5185\u5916\u641c\u7d22:'+searchStr,
            arg = 'https://work.alibaba-inc.com/nwpipe/search?type=all&keywords='+searchStr,
            valid=True)

def parseResults(results,key):
    if key in results.keys():
        if 'results' in results[key]:
            return results[key]['results']
    return []

def parseWebData(searchStr,wf,data):
    for item in data :
        wf.add_item(title=u'[\u5bfc\u822a] '+item['title'],
            subtitle= 'tag:'+item['tag'] + '\t\t\t' + 'description:'+item['description'],
            arg = item['url'],
            autocomplete = item['title'],
            valid=True)

def parsePersonData(searchStr,wf,data):
    for item in data :
        if searchStr == item['lastName']  or searchStr == item['chineseNickname']:
            workPersonInfo.resolve(item,wf)
        else:
            hm = item['chineseNickname'].strip()
            if len(hm) == 0:
                hm = item['lastName']
            wf.add_item(title=hm+'\t['+item['lastName']+']\t'+'('+item['emplId']+')',
                subtitle= item['deptDesc'],
                arg = 'https://work.alibaba-inc.com/nwpipe/u/'+item['emplId'],
                autocomplete = hm,
                valid=True)

#def parseLinkData(searchStr,wf,data):
#def parseWordData(searchStr,wf,data):
def parseHistoryData(searchStr,wf,data):
    i = 0
    for item in data:
        wf.add_item(title= u'[\u5386\u53f2\u641c\u7d22]\t' + item['keyword'],
            subtitle= u'\u6309\u0054\u0041\u0042\u952e\uff0c\u5c55\u5f00\u8be6\u7ec6\u641c\u7d22\u5185\u5bb9\uff08\u0050\u0053\u003a\u60f3\u641c\u7d22\u5176\u4ed6\u4fe1\u606f\u8bf7\u8f93\u5165\u0020\u7a7a\u683c\u002b\u5173\u952e\u5b57\u0029',
            arg = 'https://work.alibaba-inc.com/nwpipe/search?type=all&keywords='+item['keyword'],
            autocomplete = item['keyword'],
            valid=True)
        i += 1
        if i > 3:
            return

def parseHotwordData(searchStr,wf,data):
    i = 0
    for item in data:
        wf.add_item(title= u'[\u70ed\u641c]\t' + item['word'],
            subtitle= u'\u6309\u0054\u0041\u0042\u952e\uff0c\u5c55\u5f00\u8be6\u7ec6\u641c\u7d22\u5185\u5bb9\uff08\u0050\u0053\u003a\u60f3\u641c\u7d22\u5176\u4ed6\u4fe1\u606f\u8bf7\u8f93\u5165\u0020\u7a7a\u683c\u002b\u5173\u952e\u5b57\u0029',
            arg = 'https://work.alibaba-inc.com/nwpipe/search?type=all&keywords='+item['word'],
            autocomplete = item['word'],
            valid=True)
        i += 1
        if i > 10:
            return

def resolveData(searchStr , wf):
    data={}
    try:
        data = getData(searchStr,wf)
    except:
        # 异常后面有空在细化，暂时全归类成获取session失败
        LogUtil.error("workSearch.resolveData exception ",{"searchStr":searchStr})
        wf = onException(searchStr,wf)
    else:
        if data is not None:
            parseData(searchStr,wf,data)
        else:
            print('data is null')