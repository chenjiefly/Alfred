# encoding: utf-8
import common
import requests
from bs4 import BeautifulSoup

url = 'http://mw.alibaba-inc.com/doc.html'

def getDocInfos():
    response = requests.get(url)
    encoding = response.encoding
    data = BeautifulSoup(response.text.encode(encoding),'html.parser')
    iboxContents = data.find_all('div',attrs={'class':'ibox-content'})
    allDoc = []
    for iboxContent in iboxContents:
        docs = parseIboxContent(iboxContent)
        allDoc += docs
    allDoc.sort(key=lambda docInfo:docInfo['id'])
    return allDoc

def parseIboxContent(tbody):
    spans = tbody.find_all('span')
    allDoc = []
    for span in spans:
        docInfo = parseSpan(span)
        allDoc.append(docInfo)
    return allDoc

def parseSpan(span):
    aArray = span.find_all('a')
    docInfo = {}

    docInfo['name'] = aArray[0].get_text()
    docInfo['id'] = aArray[0].get_text().lower()
    docInfo['href'] = 'http://mw.alibaba-inc.com'+ aArray[0].attrs['href']
    if len(aArray) > 1:
        docInfo['enHref'] = 'http://mw.alibaba-inc.com' + aArray[1].attrs['href']
    return docInfo