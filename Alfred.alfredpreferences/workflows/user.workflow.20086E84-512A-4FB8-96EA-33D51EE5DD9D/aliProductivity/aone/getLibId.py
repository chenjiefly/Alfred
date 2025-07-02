# encoding: utf-8
import common
import json
from utils import httpUtil

url = 'https://aone.alibaba-inc.com/appcenter/ajax/lib/search'
#mainUrl='https://aone.alibaba-inc.com'
mainUrl= url

def getParams(searchStr):
    parmas = {
        'pageSize':10
    }
    parmas['name']=searchStr
    return parmas

def getLibInfo(searchStr):
    res = httpUtil.get(url,mainUrl,getParams(searchStr))
    list = []
    if res.status_code == 200 :
        context = json.loads(res.content,encoding='utf-8')
        if context['successful'] == True:
            object = context['object']
            dataList = object['data']
            if len(dataList) > 0 :
                for libData in dataList:
                    libInfo = {}
                    libInfo['name']=libData['libName']
                    libInfo['id']=libData['id']
                    libInfo['deptName'] = libData['regionName']
                    list.append(libInfo)
    if len(list) > 0:
        list.sort(key=lambda libData:libData['name'])
    return list

if __name__ == '__main__':
    print(getLibInfo('cnls'))