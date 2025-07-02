# encoding: utf-8
import common
import requests
from bs4 import BeautifulSoup

url = 'http://mw.alibaba-inc.com/ops.html'

def getOpsInfos():
    response = requests.get(url)
    encoding = response.encoding
    data = BeautifulSoup(response.text.encode(encoding),"html.parser")
    tbodys = data.find_all('tbody')
    allOps = []
    for tbody in tbodys:
        opss = parseTbody(tbody)
        allOps += opss
    allOps.sort(key=lambda opsInfo:opsInfo['id'])
    return allOps

def parseTbody(tbody):
    trs = tbody.find_all('tr')
    allOps = []
    for tr in trs:
        opsInfo = parseTr(tr)
        allOps.append(opsInfo)
    return allOps

def parseTr(tr):
    tds = tr.find_all('td')
    opsInfo = {}
    if len(tds) == 3 :
        name = tds[1].get_text()
        div = tds[2].find('div')
        id = ''
        attrs  = div.attrs
        if 'data-spm' in div.attrs.keys():
            id = attrs['data-spm'].lower()
        aArray = tds[2].find_all('a')
        urls = []
        for a in aArray:
            url = {}
            url['href']=a.attrs['href']
            url['name']=a.get_text()
            urls.append(url)
        opsInfo['name'] = name
        opsInfo['id']= id
        opsInfo['urls']=urls
    return opsInfo