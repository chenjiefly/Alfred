# encoding: utf-8
from utils import httpUtil
from bs4 import BeautifulSoup
import json
import traceback
from utils import LogUtil

url = 'https://work.alibaba-inc.com/nwpipe/u/'
mainUrl = 'https://work.alibaba-inc.com'

def getWorkPersonData(emplId):
    personUrl = url + str(emplId)
    response = httpUtil.get(personUrl,mainUrl)
    encoding = response.encoding
    if response.status_code == 200 :
        data = BeautifulSoup(response.text.encode(encoding),'html.parser')
        personInfo = {}
        return resolveResponse(personInfo,data)
    return None

def resolveResponse(personInfo,data):
    scripts = data.find_all('script')
    #print(len(scripts))
    personInfo={}
    token = getToken(data)
    if token is not None :
        personInfo['token'] = token
    for script in scripts:
        text = script.get_text()
        if 'window.canaryData.pageletData["nw-profile2020"]' in text :
            index = text.index('["nw-profile2020"]["props"]')
            dataStr = text[126:index-31]
            data = json.loads(dataStr)
            if data['success']:
                if 'content' in data.keys():
                    content = data['content']
                    personInfo['phone']=getPhone(content)
                    personInfo['ding']=getDing(content)
                    personInfo['jobName']=getJobName(content)
                    personInfo['supervisor']=getSupervisor(content)
                    #personInfo['jobResponsibility']=getJobResponsibility(content)
                    personInfo['annual']=str(getAnnual(content))
                    return personInfo
    #print('没有查到数据')
    return None

def getToken(data):
    try:
        tokens = data.find_all('input')
        token = tokens[0]['value']
        return token
    except:
        LogUtil.error("workPersonInfo.getToken exception ",{"data":data})
        return None

def getPhone(content):
    try:
        mobile =  content['dataSource']['StaffContactInfo']['contactMobile']
        monileZone = mobile['mobileZone'].strip()
        number = mobile['number'].strip()
        if len(number) == 0 :
            return ''
        if len(monileZone) > 0:
            return '(+'+monileZone+')'+number
        else:
            return number
    except:
        LogUtil.error("workPersonInfo.getPhone exception ",{"content":content})
        return ''

def getDing(content):
    try:
        return  content['dataSource']['StaffContactInfo']['dingtalkId']
    except:
        LogUtil.error("workPersonInfo.getDing exception ",{"content":content})
        return ''

def getJobName(content):
    try:
        return  content['dataSource']['ActiveStaffJobs'][0]['jobName']
    except:
        LogUtil.error("workPersonInfo.getJobName exception ",{"content":content})
        return ''

def getJobResponsibility(content):
    try:
        return  content['dataSource']['ActiveStaffJobs'][0]['jobResponsibility']
    except:
        LogUtil.error("workPersonInfo.getJobResponsibility exception ",{"content":content})
        return ''

def getSupervisor(content):
    try:
        return  content['dataSource']['ActiveStaffJobs'][0]['supervisorList'][0]['nickName']
    except:
        LogUtil.error("workPersonInfo.getSupervisor exception ",{"content":content})
        return ''


def getAnnual(content):
    try:
        return  content['dataSource']['StaffAnnualDay']['wishInfoAnnualDay']['number']
    except:
        LogUtil.error("workPersonInfo.getAnnual exception ",{"content":content})
        return ''

# 1. 获取数据
def getDatas(searchStr,wf):
    return wf.cached_data('$___work_'+searchStr,lambda :getWorkPersonData(searchStr),max_age=60)

# 2. 处理异常
def onException(personInfo ,wf):
    hm = personInfo['chineseNickname'].strip()
    if len(hm) == 0:
        hm = personInfo['lastName']
    wf.add_item(title=hm+'\t['+personInfo['lastName']+']\t'+'('+personInfo['emplId']+')',
        subtitle= personInfo['deptDesc'],
        arg = 'https://work.alibaba-inc.com/nwpipe/u/'+personInfo['emplId'],
        autocomplete = hm,
        valid=True)
    return wf

# 3. 解析数据
def parseData(personInfo ,wf ,addedInfo):
    hm = personInfo['chineseNickname'].strip()
    if len(hm) == 0:
        hm = personInfo['lastName']
    subtitle = personInfo['deptDesc']
    if 'supervisor' in addedInfo:
        subtitle = addedInfo['supervisor'] +' \t'+ subtitle
    if 'annual' in addedInfo:
        subtitle = '['+addedInfo['annual']+u'\u5e74] \t'+ subtitle
        title = hm+'\t['+personInfo['lastName']+']\t'+'('+personInfo['emplId']+')' +'\t'+ addedInfo['jobName']

    wf.add_item(title=title,
        subtitle=subtitle,
        arg = 'https://work.alibaba-inc.com/nwpipe/u/'+personInfo['emplId'],
        autocomplete = hm,
        largetext=title +'\n  ' + subtitle,
        valid=True)

    if 'ding' in addedInfo:
        wf.add_item(title = u'\u6253\u5f00 '+hm+'['+personInfo['lastName']+']('+personInfo['emplId']+u')  \u7684\u9489\u9489',
            subtitle= '按ENTER键打开钉钉',
            arg = 'dingtalk://dingtalkclient/action/sendmsg?dingtalk_id='+addedInfo['ding'],
            autocomplete = hm,
            icon = './ding.png',
            valid=True)

    wf.add_item(title = u'\u901a\u8fc7\u624b\u673a\u547c\u53eb: '+hm+'['+personInfo['lastName']+']('+personInfo['emplId']+u')',
        subtitle= '按ENTER键拨打手机电话',
        arg = getCallUrl(addedInfo['token'],personInfo['emplId'],'phone'),
        autocomplete = hm,
        icon = './callphone.png',
        valid=True)
    wf.add_item(title = u'\u901a\u8fc7\u963f\u91cc\u90ce\u547c\u53eb: '+hm+'['+personInfo['lastName']+']('+personInfo['emplId']+u')',
        subtitle= '按ENTER键拨打阿里郎电话',
        arg = getCallUrl(addedInfo['token'],personInfo['emplId'],'extension'),
        autocomplete = hm,
        icon = './alilang.png',
        valid=True)


callApi = 'https://work.alibaba-inc.com/xservice/makeWorkPhoneCallNoNumber.json?_api=Profile.makeWorkPhoneCallNoNumber&_moc1k=false&toType=phone&numberType=contactMobile'

def getCallUrl(token , userId, type):
    return callApi + '&_csrf_token='+token+'&toUserId='+userId+'&fromType='+type


def resolve(personInfo , wf):
    data={}
    try:
        data = getDatas(personInfo['emplId'],wf)
    except:
        # 异常后面有空在细化，暂时全归类成获取session失败
        LogUtil.error("workPersonInfo.resolve exception ",{"personInfo":personInfo})
        wf = onException(personInfo,wf)
    else:
        if data is not None:
            parseData(personInfo,wf,data)
        else:
            print('data is null')