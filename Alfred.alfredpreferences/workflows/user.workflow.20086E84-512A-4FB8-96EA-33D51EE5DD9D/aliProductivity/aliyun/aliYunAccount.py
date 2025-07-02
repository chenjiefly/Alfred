
import common
from utils import cacheUtil
import getAliYunSubAccountList,getAliYunMainAccountList


def getAccount():
    mainAccounts = getAliYunMainAccountList.getAliYunAccountList()
    subAccounts = getAliYunSubAccountList.getAliYunAccountList()
    if not mainAccounts or len(mainAccounts) == 0:
        return subAccounts

    if not subAccounts or len(subAccounts) == 0:
        return subAccounts

    return mainAccounts + subAccounts

if __name__ == '__main__':
    cacheUtil.remove()
    accounts = getAccount()
    print(accounts)