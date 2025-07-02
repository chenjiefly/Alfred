# encoding: utf-8
import common
from utils import httpUtil
import json
from utils import employeeIdCache

url = 'https://ca.alibaba-inc.com/pageContent/account/provider/queryProvider?queryTag=true&pageNum=1&pageSize=100'
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
                    accountInfo['code'] = accountData['code']
                    accountInfo['name'] = accountData['name']
                    accountInfo['type'] = accountData['type']
                    accountInfo['ownerName'] = accountData['ownerName']
                    accountInfo['accountType'] = 'main'
                    accountInfo['loginUrl'] = getLoginUrl(accountInfo['id'])
                    list.append(accountInfo)
    return list

loginUrl = 'https://ca.alibaba-inc.com/pageContent/account/provider/getAutoLoginUrl?_input_charset=utf-8'
def getLoginUrl(id):
    # employeeId = employeeIdCache.get()
    # params ={}
    # params['providerId'] = id
    # params['operator'] = employeeId
    # res = httpUtil.get(loginUrl,loginUrl,params=params)
    # if res.status_code == 200 :
    #     content = res.content.strip('\'')
    #     context = json.loads(content,encoding='utf-8')
    #     if context['success'] == True:
    #         return context['data']
    employeeId = employeeIdCache.get()
    return loginUrl + '&providerId='+str(id)+'&operator='+ str(employeeId)

if __name__ == '__main__':
    list = getAliYunAccountList()
    print(list)