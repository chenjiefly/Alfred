# encoding: utf-8
import common
import json
from utils import httpUtil
from utils import LogUtil

url = 'https://n.alibaba-inc.com/api/ops/armory/host-info'
mainUrl = url

def getParams(str):
    params={}
    params['host'] = str
    return params

def getHeader(cookies):
    header = {}
    return header

def search(searchStr,isRepeat=False):
    res = httpUtil.get(url,mainUrl,params=getParams(searchStr))
    response = json.loads(res.text)
    if response['msg'] == 'success':
        try:
            data =  response['data']
            ipInfo = {}
            ipInfo['ip']=data['ip']
            ipInfo['site']=data['site']
            ipInfo['unit']=data['unit']
            ipInfo['status']=data['status']
            ipInfo['group']=data['group']
            ipInfo['cpu']=str(data['cpuCore'])
            ipInfo['memory']=str(data['memoryCapacity']/1024)
            return ipInfo
        except:
            return []


# 1. 获取数据
def getData(ip,wf):
    return  wf.cached_data('$___queryIpDetail_'+ip,lambda:search(ip),max_age=86400)

# 2. 处理异常
def onException(searchStr ,wf):
    wf.add_item(title='登录态失效，请按Enter键登录之后重试~',
                subtitle= '按Enter可以到诺曼底官网获取登录态',
                arg = 'https://n.alibaba-inc.com',
                icon = "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns",
                valid=True)
    return wf

# 3. 解析数据
def parseData(searchStr ,wf ,ipInfo):
    title = ipInfo['ip'] + '\t\t' + ipInfo['site']+ '\t' + ipInfo['group']
    subtitle =ipInfo['unit']+'  ['+ ipInfo['status']+'] [' + ipInfo['cpu']+'C' + ipInfo['memory']+'G]'
    if 'beta' in ipInfo.keys():
        subtitle += '   (BETA)'
    subtitle += '  Enter一键登入Web Terminal'
    wf.add_item(
        title= title,
        subtitle= subtitle,
        arg = 'https://sa.alibaba-inc.com/ops/terminal.html?ip='+ipInfo['ip'],
        autocomplete = ipInfo['ip'],
        icon='8A8B30E1-16CF-4C45-9CC9-0FF8DAA5D0CB.png',
        valid=True)
    wf.add_item(
        title= title,
        subtitle= '按ENTER一键申请DEBUG~',
        arg = ipInfo['ip'],
        autocomplete = ipInfo['ip'],
        icon='./icon/debug.jpeg',
        valid=True)



def resolveData(groupName , wf):
    data=[]
    try:
        data = getData(groupName,wf)
    except:
        # 异常后面有空在细化，暂时全归类成获取session失败
        LogUtil.error("normandySearch exception ",{"groupName":groupName})
        wf = onException(groupName,wf)
    else:
        parseData(groupName,wf,data)


if __name__ == '__main__':
    print(search('33.4.22.222'))

