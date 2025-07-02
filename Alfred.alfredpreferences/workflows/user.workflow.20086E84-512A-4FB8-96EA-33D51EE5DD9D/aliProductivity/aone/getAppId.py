# encoding: utf-8
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
import json
from utils import httpUtil

url = 'https://cd.aone.alibaba-inc.com/ec/ajax/switch/queryAppList'
#mainUrl = 'https://aone.alibaba-inc.com'
mainUrl=url

def getAppInfo(searchStr):
    params = {}
    params['name']=searchStr
    res = httpUtil.get(url,mainUrl,params)
    list = []
    if res.status_code == 200 :
        context = json.loads(res.content,encoding='utf-8')
        if context['successful'] == True:
            object = context['object']
            dataList = object['dataList']
            if len(dataList) > 0 :
                index = 0
                for appData in dataList:
                    appInfo = {}
                    appInfo['name']=appData['name']
                    appInfo['id']=appData['id']
                    if 'level' in appData.keys():
                        appInfo['level']=appData['level']
                    else:
                        appInfo['level']='['+appData['status']+']'
                    ownersName = appData['ownersName']
                    if len(ownersName) > 0:
                        appInfo['owner']=appData['ownersName'][0]['atFullName']
                        appInfo['deptName']=appData['ownersName'][0]['deptName']
                    else:
                        appInfo['owner']=u'\u5947\u602a\u002c\u6ca1\u6709\u67e5\u5230'
                        appInfo['deptName']=appData['regionName']
                    list.append(appInfo)
                    index += 1
                    if index >= 20 :
                        break
    return list

if __name__ == '__main__':
    print(getAppInfo('cngoc'))