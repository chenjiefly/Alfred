# encoding: utf-8
import common
import json
from utils import httpUtil

url = "https://n.alibaba-inc.com/api/searcher"

def getParams(searchStr):
    parmas = {}
    parmas['value']=searchStr
    return parmas

def search(searchStr):
    res = httpUtil.get(url,url,getParams(searchStr))
    if res.status_code == 200 :
        context = json.loads(res.text,encoding='utf-8')
        if context['code'] == 200:
            data = context['data']
            if data != None:
                data.sort(key=lambda libData:libData['name'])
                return data
    return []

if __name__ == '__main__':
    print(search('33.4.22.222'))