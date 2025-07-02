# encoding: utf-8
# 复制成秒级大盘
import sunfireRepository
from sunfireRepository import parseUrl
from sunfireRepository import queryPlugins
from sunfireRepository import addPlugins

def copy(orgUrl,path,name= None):
    urlInfo = parseUrl(orgUrl)
    orgPlutinType = urlInfo['pluginType']
    if( orgPlutinType != 'spm' and orgPlutinType != 'multiMinute'):
        print(' SunfireToolsError : plutinType not match. url = '+ orgUrl)
        return
    pluginType = ''
    if(orgPlutinType == 'spm'):
        pluginType = 'spmSecond'
        #pluginType = 'spm'
    if(orgPlutinType == 'multiMinute'):
        #pluginType = 'multiSecond'
        pluginType = 'multiMinute'
    tenantId = urlInfo['tenantId']
    pluginId = urlInfo['pluginId']
    parent =  path

    newPluginInfo ={
        "tenantId":tenantId,
        "parent":parent,
        "plugin":pluginType
    }

    orgPluginReponse = queryPlugins(orgPlutinType,pluginId,tenantId)
    if not orgPluginReponse['success']:
        print(' SunfireToolsError : queryPlugins Error. url = '+ url + ', response:'+ orgPluginReponse)
        return

    orgDataInfo = orgPluginReponse["data"][0]
    if name is None :
        name = orgDataInfo["name"]+ u'-\u79d2\u7ea7'
    data = {
        "clusterFilter":orgDataInfo["clusterFilter"],
        "cal":orgDataInfo["cal"],
        "sourceType":orgDataInfo["sourceType"],
        "log":orgDataInfo["log"],
        "status":orgDataInfo["status"],
        "logColDescMappingId":orgDataInfo["logColDescMappingId"],
        "tt":orgDataInfo["tt"],
        "sls":orgDataInfo["sls"],
        "whiteFilters":orgDataInfo["whiteFilters"],
        "blackFilters":orgDataInfo["blackFilters"],
        "opsGroupBy":orgDataInfo["opsGroupBy"],
        "groupBy":orgDataInfo["groupBy"],
        "keyIndex":orgDataInfo["keyIndex"],
        "sortWhenMax":orgDataInfo["sortWhenMax"],
        "useLogColDesc":orgDataInfo["useLogColDesc"],
        "maxGroupBy":1000,
        "name":name,
        "pluginType":pluginType
    }
    if orgPlutinType == "spm":
        data["spm"]=orgDataInfo["spm"]
    newPluginInfo["body"]=data

    return addPlugins(newPluginInfo,tenantId)

def batchCopy(reqs):
    for req in reqs:
        orgUrl = req["orgUrl"]
        path = req["path"]
        print(copy(orgUrl,path))

reqs = [
{
    "orgUrl":"https://x.alibaba-inc.com/custom/12/product/preview/spm/5161","path":"国际出口/拆合包引擎/2_🔥系统监控"
}
]
batchCopy(reqs)


