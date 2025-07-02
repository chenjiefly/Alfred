# encoding: utf-8
from pycookiecheat import chrome_cookies
import json
import requests

mainUrl = "https://x.alibaba-inc.com"

def post(url,params={}):
    cookies = chrome_cookies(mainUrl)
    url = url + cookies['csrfToken']
    header={}
    return requests.post(url,data=params,cookies=cookies,headers=header)

def get(url,params={}):
    cookies = chrome_cookies(mainUrl)
    params["_csrf"] = cookies['csrfToken']
    return requests.get(url,params=params, cookies=cookies)


addPluginUrl = 'https://x.alibaba-inc.com/web/config/addPlugin.do?_input_charset=utf-8&_csrf='
def addPlugins(param,tenantId=12):
    data = {
        "param":json.dumps(param),
        "tenantId":tenantId
    }
    response =  post(addPluginUrl,data)
    if response.status_code == 200 :
        content = response.content
        return json.loads(content)

queryPluginsUrl = 'https://x.alibaba-inc.com/web/config/queryPlugins.do?_input_charset=utf-8'
def queryPlugins(pluginType,pluginId,tenantId=12):
    data = {
        "plugin":pluginType,
        "pluginId":pluginId,
        "tenantId":tenantId
    }
    response = get(queryPluginsUrl,data)
    if response.status_code == 200 :
        content = response.content
        return json.loads(content)

updatePluginUrl = 'https://x.alibaba-inc.com/web/config/updatePlugin.do?_input_charset=utf-8&_csrf='
def updatePlugin(param,tenantId=12):
    paramStr = json.dumps(param)
    data = {
        "param":paramStr,
        "tenantId":tenantId
    }
    response = post(updatePluginUrl,data)
    if response.status_code == 200 :
        content = response.content
        return json.loads(content)

def parseUrl(sunfireUrl):
    splits = sunfireUrl.split("/")
    if (len(splits) == 9):
        data = {
            "tenantId":splits[4],
            "pluginType":splits[7],
            "pluginId":splits[8]
        }
        return data
    return {}

getFileByPluginInfoUrl = 'https://x.alibaba-inc.com/web/folder/getFileByPluginInfo.do'
# 获取文件信息
def getFileByPluginInfo(pluginId,pluginType,tenantId):
    data = {
        "pluginType":pluginType,
        "pluginId":pluginId,
        "tenantId":tenantId,
        "_input_charset":"utf-8"
    }
    response = get(getFileByPluginInfoUrl,data)
    if response.status_code == 200 :
        content = response.content
        return json.loads(content)

# 更新监控配置
def updateByQueryData(data,tenantId,pluginType,path):
    updateData = {
        "tenantId":tenantId,
        "parent":path,
        "plugin":pluginType,
        "body":data
    }
    data["pluginType"]=pluginType
    response = updatePlugin(updateData,tenantId)
    print(json.dumps(response))

