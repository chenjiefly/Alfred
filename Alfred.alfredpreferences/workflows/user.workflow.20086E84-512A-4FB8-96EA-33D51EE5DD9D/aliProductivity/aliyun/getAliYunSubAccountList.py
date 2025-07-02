# encoding: utf-8

import common
from utils import LogUtil
from utils import httpUtil
import json
from utils import employeeIdCache

url = 'https://ca.alibaba-inc.com/pageContent/account/ramUser/listRamUsersByPage?_input_charset=utf-8&pageNum=1&pageSize=100&queryTag=true&notInRamUserTypes=ADMIN%2CRAM'
#mainUrl = "https://n.alibaba-inc.com/api/searcher"
mainUrl = url

def cacheEmployeeId():
    res = httpUtil.get(url,mainUrl)
    if res.status_code == 200 :
        content = res.content.strip('\'') 
        context = json.loads(content,encoding='utf-8')
        object = context['data']
        dataList = object['list']
        if len(dataList) > 0:
            employeeId = dataList[0]['owner']
            employeeIdCache.cache(employeeId)
            return employeeId

def getAliYunAccountList():
    employeeId = employeeIdCache.get()
    if not employeeId or employeeId.isspace():
        employeeId = cacheEmployeeId()
    if not employeeId or employeeId.isspace():
        return []

    params = {'operateUser':employeeId}
    res = httpUtil.get(url,mainUrl,params)
    list = []
    if res.status_code == 200 :
        context = json.loads(res.content,encoding='utf-8')
        if context['success'] == True:
            object = context['data']
            dataList = object['list']
            if len(dataList) > 0 :
                for accountData in dataList:
                    accountInfo = {}
                    accountInfo['id'] = accountData['id']
                    accountInfo['code'] = accountData['providerCode']
                    accountInfo['name'] = accountData['name']
                    accountInfo['type'] = accountData['type']
                    accountInfo['ownerName'] = accountData['providerOwnerName']
                    accountInfo['providerIdkp'] = accountData['providerIdkp']
                    accountInfo['accountType'] = 'sub'
                    accountInfo['loginUrl'] = getLoginUrl(accountInfo['name'],accountInfo['providerIdkp'])
                    list.append(accountInfo)
    return list


loginUrl = 'https://ca.alibaba-inc.com/pageContent/account/idp/resolve.html?tryLogin=true&_input_charset=utf-8'
def getLoginUrl(name,providerIdkp):
    return loginUrl + '&ramUserName='+name+'&idkp='+providerIdkp

if __name__ == '__main__':
    list = getAliYunAccountList()
    print(list)
