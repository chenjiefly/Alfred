# encoding: utf-8
import sunfireRepository
from sunfireRepository import parseUrl
from sunfireRepository import queryPlugins
from sunfireRepository import addPlugins

data = {"tenantId":"12","parent":"菜鸟国际限流","plugin":"generalComp","body":{"clusterFilter":{"env":{"values":["PRE_PUBLISH"],"type":"black"},"group":None,"idc":None,"ip":None,"unit":None},"pluginType":"generalComp","name":"限流指标-CNGCS","sourceType":"LOG","log":{"apps":["cngcs"],"path":"/home/admin/logs/csp/sentinel-block.log","charset":"UTF-8","lineBreaker":None,"logParseType":"DEFAULT"},"status":{"computeClose":None,"createTime":1585062193905,"creater":"shancheng.wsj","degradeOperator":None,"degradeReason":None,"degradeTime":None,"operator":"shancheng.wsj","updateTime":1603458714126},"logColDescMappingId":234,"tt":{"topic":"","subId":"","accessKey":"","queueSize":None,"charset":"UTF-8"},"sls":{"accessId":"","accessKey":"","endpoint":"","logstore":"","project":"","simple":False},"whiteFilters":[],"blackFilters":[],"maxGroupBy":1000,"groupBy":[{"dim":{"dimExtra":None,"end":None,"left":"|","leftIndex":1,"maxLength":0,"metricKey":None,"metricKeyType":None,"name":"resource","nameType":"result","right":",","start":None,"translate":None},"sampleAlgorithm":None,"values":["*"]},{"dim":{"dimExtra":None,"end":None,"left":",","leftIndex":0,"maxLength":0,"metricKey":None,"metricKeyType":None,"name":"exception","nameType":"result","right":",","start":None,"translate":None},"sampleAlgorithm":None,"values":["*"]},{"dim":{"dimExtra":None,"end":None,"left":",","leftIndex":1,"maxLength":0,"metricKey":None,"metricKeyType":None,"name":"targetApp","nameType":"result","right":",","start":None,"translate":None},"sampleAlgorithm":None,"values":["*"]},{"dim":{"dimExtra":None,"end":None,"left":",","leftIndex":2,"maxLength":0,"metricKey":None,"metricKeyType":None,"name":"limitApp","nameType":"result","right":"|","start":None,"translate":None},"sampleAlgorithm":None,"values":["*"]}],"opsGroupBy":{"idc":False,"app":False,"appGroup":False,"ldc":False,"server":False,"extra":None},"cal":{"val":None,"valBak":None,"fun":None,"hide":False,"reverseTop":False,"topn":0,"weight":0},"keyIndex":True,"statsCols":[{"fun":"sum","hide":False,"reverseTop":False,"topn":0,"val":{"dimExtra":None,"end":None,"left":"|","leftIndex":2,"maxLength":0,"metricKey":None,"metricKeyType":None,"name":"限流次数","nameType":None,"right":",","start":None,"translate":None},"valBak":None,"weight":500}],"customStatsCols":[],"alarm":{"timeZoneCustom":True,"timeZone":"Asia/Shanghai","baseline":False,"frequency":10,"level":None,"model":{"grayRules":[],"rules":[{"alarmMsgLevel":"critical","name":"第1条规则","dimFilters":[{"dimIndex":0,"whiteNames":["*"]},{"dimIndex":1,"whiteNames":["*"]},{"dimIndex":2,"whiteNames":["*"]},{"dimIndex":3,"whiteNames":["*"]}],"timeFilter":None,"triggers":[{"N":3,"compare":">","comparePercent":"上涨超过","mergeMethod":None,"metric":None,"noneExistKeyAsZero":False,"threshold":{"critical":None,"urgent":None,"warning":None},"thresholdValue":500,"type":"10","unit":" ","valueField":"限流次数","valueIndex":0,"valueIsPercent":False}],"andor":"and"}]}},"groupByOps":False,"importantLevel":0,"logColDescId":234,"push":False,"samples":None,"samplingRate":0,"saveSchema":None,"sortWhenMax":False,"spm":None,"tenant":None,"topAlarm":None,"useLogColDesc":False,"logColDescs":[{"dim":{"dimExtra":None,"end":None,"left":"|","leftIndex":1,"maxLength":0,"metricKey":None,"metricKeyType":None,"name":"resource","nameType":"result","right":",","start":None,"translate":None}},{"dim":{"dimExtra":None,"end":None,"left":",","leftIndex":0,"maxLength":0,"metricKey":None,"metricKeyType":None,"name":"exception","nameType":"result","right":",","start":None,"translate":None}},{"dim":{"dimExtra":None,"end":None,"left":",","leftIndex":1,"maxLength":0,"metricKey":None,"metricKeyType":None,"name":"targetApp","nameType":"result","right":",","start":None,"translate":None}},{"dim":{"dimExtra":None,"end":None,"left":",","leftIndex":2,"maxLength":0,"metricKey":None,"metricKeyType":None,"name":"limitApp","nameType":"result","right":"|","start":None,"translate":None}},{"dim":{"dimExtra":None,"end":None,"left":"|","leftIndex":2,"maxLength":0,"metricKey":None,"metricKeyType":None,"name":"limitTimes","nameType":"result","right":",","start":None,"translate":None}}]}}


def createLimit(appName):
    name = "限流指标-"+appName
    data["body"]["name"]=name
    data["body"]["log"]["apps"][0]=appName
    response = addPlugins(data,12)
    print(response)

apps = {
"cndcp",
"cncbp",
"cncbf",
"track",
"cnopkr",
"customsgateway",
"gtc",
"ae-delivery-server",
"cngpp",
"cnctp",
"pickuppoint-fulfil",
"cniwb",
"gccs",
"gcbs",
"rse",
"gcts",
"cnimf",
"idms",
"cnctp-face",
"iwis",
"cneos",
"cnpce",
"cngdata",
"cngpp-sop",
"gcss",
"gwms-inbound",
"gwms-oss",
"gwms-pick",
"gsc-service",
"rw-hub",
"gwms-auto",
"cnglm",
"gwms-intel",
"gwms-shipping",
"gwms-packing",
"haitao-oms-system",
"haitao-finance",
"haitao-storage-compose",
"haitao-logistics",
"basic-location-compose",
"logistics-tms-system",
"logistics-settlement-system",
"sc-titan-wms",
"cnglp",
"cngrc",
"cngfc",
"cngdf",
"global-lnp-networkserver"
}
for appName in apps:
    createLimit(appName)


