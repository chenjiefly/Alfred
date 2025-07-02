# encoding: utf-8
from aliProductivity.utils import LogUtil
import common
import time
import sys, os
# from ..utils import httpUtil
from utils import httpUtil
import json
reload(sys)
sys.setdefaultencoding('utf8')

url = 'https://yida.alibaba-inc.com/alibaba/web/APP_ZXGJVX4ZRGTUBU8FFZ1O/query/formProcInstData/getInstanceDatas.json'
mainUrl = 'https://yida.alibaba-inc.com/s/adict'

class searchParam:
    def __init__(self, key, value, type, componentName):
        self.key = key
        self.value = value
        self.type = type
        self.componentName = componentName


def param_to_json(obj):
    return {
        "key": obj.key,
        "value": obj.value,
        "type": obj.type,
        "componentName": obj.componentName
    }

def isLoginInvalidate(res):
    response = json.loads(res.text)
    if 'errorCode' in response.keys():
        # LogUtil.info('getAdictInfo.loginInvalidate , Check whether login failed...')
        if response['errorCode'] == '302':
            LogUtil.info('getAdictInfo.loginInvalidate :'+ str(response))
            return True
    return False

def tryLogin():
    res = httpUtil.get(mainUrl,mainUrl,isRepeat=True)
    LogUtil.info('getAdictInfo.tryLogin:  ' + str(res))

def getAdictInfo(searchStr):
    params = {}
    searchParams = []
    searchParams.append(searchParam('textField_5bj0iyk', searchStr, 'TEXT', 'TextField'))
    searchJson = json.dumps(searchParams, default=param_to_json)
    params['__api'] = 'nattyFetch'
    params['__stamp'] = int(round(time.time() * 1000))
    params['searchField'] = searchJson
    params['page'] = 1
    params['currentPage'] = 1
    params['pageSize'] = 50
    params['limit'] = 50
    params['formUuid'] = 'FORM-NC866F81S44P2GED5GO50CZLFTI23NL0II8NK91'
    params['manageUuid'] = 'FORM-VFYJ4QZUPI2PZYXFZQ313WZV4W3W1J7B8J8NK35'
    res = httpUtil.get(url, mainUrl, params,isLoginInvalidate=isLoginInvalidate,tryLogin=tryLogin)
    list = []

    if res.status_code == 200:
        context = json.loads(res.content, encoding='utf-8')
        # LogUtil.info('getAdictInfo('+searchStr+'),response = ' + str(context))
        if context['success'] == True:
            object = context['content']
            if (object.get('values') == None):
                return list
            else:
                dataList = object['values']
                if len(dataList) > 0:
                    index = 0
                    for adictData in dataList:
                        adictDataMap = adictData['dataMap']
                        adictInfo = {}
                        adictInfo['formInstanceId'] = adictData['formInstanceId']
                        adictInfo['formUuid'] = adictData['formUuid']
                        adictInfo['appType'] = adictData['appType']
                        adictInfo['adictName'] =getValue(adictDataMap,'textField_5bj0iyk')
                        adictInfo['fullName'] =getValue(adictDataMap,'textField_6wsyt0j')
                        adictInfo['description'] =getValue(adictDataMap,'textField_tka2fg3')
                        adictInfo['comment'] =getValue(adictDataMap,'textAreaField_qdf02gh')
                        adictInfo['lable'] =getValue(adictDataMap,'tagSelectField_kn8l82ib')
                        adictInfo['subClassify'] =getValue(adictDataMap,'textField_kn8l82ic')
                        adictInfo['classify'] =getValue(adictDataMap,'selectField_kn8mnmfj')
                        list.append(adictInfo)
                        index += 1
                        if index >= 20:
                            break
    return list

def getValue(adictData,key):
    if key in adictData:
        return adictData[key]
    return ''


if __name__ == '__main__':

    # Create a global `Workflow3` object
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    getAdictInfo('CN')