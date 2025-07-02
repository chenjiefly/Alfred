# encoding: utf-8
import json
from utils import httpUtil
from utils import LogUtil

def getQueryIpByGroupUrl(appName):
    return 'https://n.alibaba-inc.com/api/ops/app/'+appName+'/res/SERVER'

def getParams(searchStr):
    parmas = {
        "isCategory":"true",
        "pageSize":"20"
    }
    parmas['nodeGroup']=searchStr
    return parmas

def queryIpByGroup(groupInfo):
    if groupInfo == None:
        raise Exception('groupInfo is None')
    groupName = groupInfo['name']
    appName = groupInfo['appName']
    url = getQueryIpByGroupUrl(appName)
    response = httpUtil.getJson(url,url,getParams(groupName))
    betaData = []
    publishData = []
    if response['code'] == 200:
        data = response['data']
        betaStack = getBetaStack(data)
        dataList = data['list']
        if dataList != None:
            for item in dataList:
                ipInfo = {}
                ipInfo['ip']=item['ip']
                ipInfo['health']=item['monitorHealth']
                ipInfo['site']=item['site']
                ipInfo['unit']=item['unit']
                ipInfo['status']=item['status']
                ipInfo['group']=item['group']
                ipInfo['cpu']=str(item['cpuCore'])
                ipInfo['memory']=str(item['memoryCapacity']/1024)
                stackIds = item['stackId']
                if betaStack != None  and betaStack in stackIds:
                    ipInfo['beta'] = 'beta'
                    betaData.append(ipInfo)
                else:
                    publishData.append(ipInfo)
        else:
            raise Exception('call api exception,groupName='+groupName+',msg='+response['msg'])
    return betaData + publishData

def getBetaStack(data):
    envNameMap = data['envNameMap']
    if envNameMap == None:
        return None
    for stack in envNameMap.keys():
        if envNameMap[stack] == 'beta':
            return stack
    return None

groupInfoUrl = 'https://n.alibaba-inc.com/api/ops/armory/group-info'
def queryGroupInfo(groupName):
    params = {'nodeGroup':groupName}
    response =httpUtil.getJson(groupInfoUrl,groupInfoUrl,params)
    if response['msg'] == 'success':
        return response['data']
    raise Exception('call api exception,groupName='+groupName+',msg='+response['msg'])

# 1. 获取数据
def getDatas(groupName,wf):
    groupInfo = wf.cached_data('$___queryGroupInfo_'+groupName,lambda:queryGroupInfo(groupName),max_age=2592000)
    return wf.cached_data('$___queryIpByGroup_'+groupName,lambda :queryIpByGroup(groupInfo),max_age=86400)

# 2. 处理异常
def onException(searchStr ,wf):
    wf.add_item(title='登录态失效，请按Enter键登录之后重试~',
                subtitle= '按Enter可以到诺曼底官网获取登录态',
                arg = 'https://n.alibaba-inc.com',
                icon = "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns",
                valid=True)
    return wf

# 3. 解析数据
def parseData(searchStr ,wf ,datas):
    for ipInfo in datas:
        title = ipInfo['ip'] + '\t\t' + ipInfo['site']+ '\t' + ipInfo['group']
        subtitle =ipInfo['unit']+'  ['+ ipInfo['status']+']  ['+ipInfo['health'] +  ']  [' + ipInfo['cpu']+'C' + ipInfo['memory']+'G]'
        if 'beta' in ipInfo.keys():
            subtitle += '   (BETA)'
        wf.add_item(
            title= title,
            subtitle= subtitle,
            arg = 'https://sa.alibaba-inc.com/ops/terminal.html?ip='+ipInfo['ip'],
            autocomplete = ipInfo['ip'],
            icon='8A8B30E1-16CF-4C45-9CC9-0FF8DAA5D0CB.png',
            valid=True)


def resolveData(groupName , wf):
    data=[]
    try:
        data = getDatas(groupName,wf)
    except:
        # 异常后面有空在细化，暂时全归类成获取session失败
        LogUtil.error("normandySearch exception ",{"groupName":groupName})
        wf = onException(groupName,wf)
    else:
        parseData(groupName,wf,data)

