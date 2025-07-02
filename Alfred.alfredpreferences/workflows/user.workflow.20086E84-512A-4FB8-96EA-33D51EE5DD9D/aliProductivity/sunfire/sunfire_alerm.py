# encoding: utf-8
# 复制成秒级大盘
from requests import models
from requests.api import patch
from sunfireRepository import parseUrl
from sunfireRepository import queryPlugins
from sunfireRepository import getFileByPluginInfo
from sunfireRepository import updateByQueryData

import json

fallToZeroAlermName = u'[P0][国际标准-勿删]流量跌零防控'
fallToZeroAlerm = json.loads('{"alarmMsgLevel":"urgent","andor":"and","dimFilters":null,"name":"[P0][国际标准-勿删]流量跌零防控","timeFilter":null,"triggers":[{"N":10,"compare":">","comparePercent":"下跌超过","mergeMethod":null,"metric":null,"noneExistKeyAsZero":false,"threshold":{"critical":null,"urgent":null,"warning":null},"thresholdValue":99.9,"type":"20","unit":" ","valueField":"总量","valueIndex":0,"valueIsPercent":true},{"N":10,"compare":">","comparePercent":"下跌超过","mergeMethod":null,"metric":null,"noneExistKeyAsZero":false,"threshold":{"critical":null,"urgent":null,"warning":null},"thresholdValue":99.9,"type":"30","unit":" ","valueField":"总量","valueIndex":0,"valueIsPercent":true},{"N":10,"compare":">","comparePercent":"下跌超过","mergeMethod":null,"metric":null,"noneExistKeyAsZero":false,"threshold":{"critical":null,"urgent":null,"warning":null},"thresholdValue":99.9,"type":"50","unit":" ","valueField":"总量","valueIndex":0,"valueIsPercent":true}]}')

successRateAlermName = u'[P0][国际标准-勿删]成功率-兜底'
successRateAlerm = json.loads('{"alarmMsgLevel":"urgent","andor":"and","dimFilters":null,"name":"[P0][国际标准预警-勿删]成功率-兜底","timeFilter":null,"triggers":[{"N":10,"compare":"<","comparePercent":"上涨超过","mergeMethod":null,"metric":null,"noneExistKeyAsZero":false,"threshold":{"critical":null,"urgent":null,"warning":null},"thresholdValue":50,"type":"10","unit":" ","valueField":"成功率","valueIndex":2,"valueIsPercent":false}]}')

rtAlermName = u'[P0][国际标准-勿删]RT大幅上涨'
rtAlerm = json.loads('{"alarmMsgLevel":"urgent","andor":"and","dimFilters":null,"name":"[P0][国际标准-勿删]RT大幅上涨","timeFilter":null,"triggers":[{"N":5,"compare":">","comparePercent":"上涨超过","mergeMethod":null,"metric":null,"noneExistKeyAsZero":false,"threshold":{"critical":null,"urgent":null,"warning":null},"thresholdValue":50,"type":"20","unit":" ","valueField":"耗时","valueIndex":3,"valueIsPercent":true},{"N":5,"compare":">","comparePercent":"上涨超过","mergeMethod":null,"metric":null,"noneExistKeyAsZero":false,"threshold":{"critical":null,"urgent":null,"warning":null},"thresholdValue":3000,"type":"10","unit":" ","valueField":"耗时","valueIndex":3,"valueIsPercent":false}]}')

# 优化告警
def fixAlermConfig(alarmRules):
    hasFallToZero = False
    hasSuccessRate = False
    hasRt = False

    for rule in alarmRules:
        if rule["name"] == fallToZeroAlermName :
            hasFallToZero = True
        if rule["name"] == successRateAlermName :
            hasSuccessRate = True
        if rule["name"] == rtAlermName :
            hasRt = True
    if not hasFallToZero:
        fallToZeroAlerm["name"]=fallToZeroAlermName
        alarmRules.append(fallToZeroAlerm)
    if not hasSuccessRate:
        successRateAlerm["name"]=successRateAlermName
        alarmRules.append(successRateAlerm)
    if not hasRt:
        rtAlerm["name"]=rtAlermName
        alarmRules.append(rtAlerm)
    return not hasFallToZero or not hasSuccessRate or not hasRt

def getDefaultAlerm():
    alarmRules = []
    fallToZeroAlerm["name"]=fallToZeroAlermName
    alarmRules.append(fallToZeroAlerm)
    successRateAlerm["name"]=successRateAlermName
    alarmRules.append(successRateAlerm)
    rtAlerm["name"]=rtAlermName
    alarmRules.append(rtAlerm)


# 获取监控路径
def getPluginPath(tenantId,pluginType,pluginId):
    pluginInfo = getFileByPluginInfo(pluginId,pluginType,tenantId)
    if pluginInfo["success"]:
        return pluginInfo["data"]["parent"]
    else :
        print("call getPluginPath fail. pluginId="+pluginId +",pluginType="+pluginType+",response="+pluginInfo)

# 检查并优化监控预警配置
def checkAlerm(sunfireUrl):
    print("start checkAlerm : " + sunfireUrl)
    urlInfo = parseUrl(sunfireUrl)
    tenantId = urlInfo["tenantId"]
    pluginType = urlInfo["pluginType"]
    pluginId = urlInfo["pluginId"]

    if pluginType != "spm":
        print("end checkAlerm,pluginType not match , url : " + sunfireUrl)
        return

    response = queryPlugins(pluginType,pluginId,tenantId)
    if not response['success']:
        print(" SunfireToolsError : queryPlugins Error. url = "+ sunfireUrl + ", response:"+ json.dumps(response))
        return

    data = response["data"][0]
    alarmInfos = data["alarm"]

    if "model" not in alarmInfos.keys():
        alarmInfos["model"] = {}

    if "rules" not in alarmInfos["model"].keys():
        alarmInfos["model"]["rules"] = []

    alarmRules = alarmInfos["model"]["rules"]

    if fixAlermConfig(alarmRules):
        path = getPluginPath(tenantId,pluginType,pluginId)
        if path is not None:
            updateByQueryData(data,tenantId,pluginType,path)
            print("end checkAlerm,update plugin , url : " + sunfireUrl)
            return
    print("end checkAlerm,no need update plugin , url : " + sunfireUrl)



urls = [
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2934",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2214",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5523",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4587",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5517",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3322",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2250",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5525",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3295",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4408",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4292",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3407",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4849",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/1718",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4850",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2977",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4278",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3999",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5119",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3296",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4845",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3152",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4846",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/1876",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/1960",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2051",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2656",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/1196",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/1411",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/1823",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/1884",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/1890",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2185",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2188",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2229",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2248",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2253",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2283",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2287",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2321",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2367",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2378",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2576",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2854",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2871",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2873",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2879",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2890",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2905",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2921",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2982",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2994",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3126",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3133",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3134",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3137",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3138",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3139",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3148",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3150",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3153",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3195",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3467",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3499",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3500",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3505",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3551",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3556",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3562",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3798",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3799",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3861",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4097",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4098",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4665",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4847",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5050",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5089",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5161",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5187",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5188",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5198",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5205",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5300",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5301",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5342",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5487",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5507",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5546",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5751",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/6041",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/766",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/1822",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/1882",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/1885",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2184",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2186",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2187",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2219",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2223",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2224",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2255",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2281",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2282",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2286",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2288",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2292",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2295",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2315",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2319",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2368",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2381",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2801",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2802",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2803",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2813",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2814",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2847",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2850",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2851",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2852",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2853",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2857",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2886",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2889",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2896",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2919",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2935",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/2942",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3061",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3078",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3106",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3107",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3127",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3128",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3129",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3130",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3131",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3132",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3135",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3136",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3140",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3143",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3199",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3298",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3385",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3408",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3501",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3502",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3503",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3504",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3506",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3509",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/3942",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4188",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4255",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4277",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4293",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4295",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4363",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4543",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4848",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4851",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4909",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4979",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/4981",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5051",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5227",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5339",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5345",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5350",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5509",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5531",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5534",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5535",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5545",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5548",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5551",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5624",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/5788",
    "https://x.alibaba-inc.com/custom/12/product/preview/spm/6524"
]

for url in urls :
    checkAlerm(url)