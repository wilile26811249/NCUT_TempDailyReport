import requests
import json
import time
from configparser import ConfigParser
import datetime
from termcolor import colored, cprint
import getpass

DEBUG = False
WEEKS_STR = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
backDay = 7

class requestLib():
    def __init__(self):
        self.URL = 'https://epidemicapi.ncut.edu.tw/api/'
        self.SESSION = requests.Session()
        self.SESSION.headers.clear()
        self.SESSION.headers.update({
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://epidemic.ncut.edu.tw',
            'referer': 'https://epidemic.ncut.edu.tw/bodyTemp'
        })

    def __request(self, method, node='', **kwargs):
        resp = self.SESSION.request(method, self.URL + node, **kwargs)
        if DEBUG:
            try:
                print(resp)
                print(resp.text)
            except (UnicodeDecodeError, UnicodeDecodeError, UnicodeError):
                print('[WARNING] Unknow unicode error from response')
        return resp

    #------------------------------------------------------------------------------------
    # Function Zone
    #------------------------------------------------------------------------------------

    def login(self, account, password , remember=False):
        data = {
            'userId': account,
            'password': password,
            'remember': remember
        }
        self.SESSION.headers.update({'referer': 'https://epidemic.ncut.edu.tw/login'})
        resp = self.__request('post', 'login', json=data)
        respJson = json.loads(resp.text)
        return respJson

    def getToken(self, account, password):
        resp = self.login(account, password)
        token = resp['token']
        return token

    def checkPosted(self, token, userId, date):
        resp = self.get_tempData(token, userId, date)
        if len(resp.text) == 0:
            print('[Info] {userId}-{date} 尚未填寫'.format(userId=userId, date=date))
            return False
        else:
            print('[Info] {userId}-{date} 已經填寫'.format(userId=userId, date=date))
            return True

    #-------------------------------------------------------------------------------------

    def get_departments(self, token):
        self.SESSION.headers.update({'authorization': 'Bearer %s' % token})
        resp = self.__request('get', 'departments')
        return resp.json()

    def get_tempData(self, token, userId, date):
        self.SESSION.headers.update({'authorization': 'Bearer %s' % token})
        resp = self.SESSION.request('get', 'https://epidemicapi.ncut.edu.tw/api/temperatureSurveys/c?mode=2&date=2020-{date}'.format(date=date))
        respJson = json.loads(resp.text)
        attribute = ['id', 'userId', 'morningActivity', 'noonActivity', 'nightActivity']
        if len(respJson) != 0:
            for attr in attribute:
                cprint('{attr} = {value}'.format(attr = attr, value = respJson[0]['state'][attr]), 'green')
        return resp

    def print_department_info(self, token):
        resp = Lib.get_departments(userToken)
        parmentDict = {}
        for index in range(len(resp)):
            parmentDict[resp[index]['departmentId']] = resp[index]['departmentName']
        cprint("Data Format is 'DepartmentID' : 'DepartmentName'", 'yellow')
        cprint(json.dumps(parmentDict, indent=4,ensure_ascii=False), 'green')
        return parmentDict
    
    def post_tempData(self, token, userId, departmentId, departmentName, className, date,
        morningTemp=34, morningActivity='',
        noonTemp=37.5, noonActivity='',
        nightTemp=34, nightActivity='',
        method='post'):
        self.SESSION.headers.update({'authorization': 'Bearer %s' % token})
        data = {
            "id": userId + "-undefined",
            "saveDate": date,
            "morningTemp": morningTemp,
            "noonTemp": noonTemp,
            "nightTemp": nightTemp,
            "isValid": False,
            "morningManner": 0,
            "noonManner": 0,
            "nightManner": 0,
            "isMorningFever": None,
            "isNoonFever": False,
            "isNightFever": None,
            "morningActivity": morningActivity,
            "noonActivity": noonActivity,
            "nightActivity": nightActivity,
            "measureTime": "18:00",
            "userId": userId,
            "departmentId": departmentId,
            "className": className,
            "departmentName": departmentName,
            "type": "1"
        }
        resp = self.__request(method, 'temperatureSurveys', json=data)
        if resp.status_code == 200:
            respJson = json.loads(resp.text)
            return respJson
        elif resp.status_code == 500:
            respJson = {
                "success": False,
                "messages": [
                    "[Error] {userId}-{date} 當天體溫已回報".format(userId=userId, date=date)
                ]
            }
            return respJson
        else:
            resp.raise_for_status()

if __name__ == "__main__":
    Lib = requestLib()

    user = ConfigParser()
    user.read('user.ini', encoding='utf-8-sig')

    envId = user['env']['departmentId']
    envName = user['env']['departmentName']
    className = user['env']['className']

    myAccount = user['user']['account']
    myPassword = user['user']['password']
    if myAccount.find('(') == 0 or myPassword.find('(') == 0:
        cprint('[WARNING] Please input user data in user.ini', 'red')
        myAccount = input('學號:')
        myPassword = getpass.getpass('密碼:')
        user.set('user', 'account', myAccount)
        user.set('user', 'password', myPassword)
        with open('user.ini', 'w') as configfile:
            user.write(configfile)

    userToken = Lib.getToken(myAccount, myPassword)
            
    if envId.find('(') == 0 or envName.find('(') == 0 or className.find('(') == 0:
        parmentDict = Lib.print_department_info(userToken)
        cprint('[WARNING] Please input department and class data in user.ini', 'red')
        envId = input('DepartmentID:')
        print("DepartmentName:", parmentDict[envId])
        className = input('ClassName:')
        user.set('env', 'departmentid', envId)
        user.set('env', 'departmentname', parmentDict[envId])
        user.set('env', 'classname', className)
        with open('user.ini', 'w') as configfile:
            user.write(configfile)

    nowDate = datetime.date.today()
    nowWeek = nowDate.weekday()   

    template = ConfigParser()
    template.read('template.ini', encoding='utf-8-sig')
    morningDo = template[WEEKS_STR[nowWeek]]['morning']
    noonDo = template[WEEKS_STR[nowWeek]]['noon']
    nightDo = template[WEEKS_STR[nowWeek]]['night']
    
    
    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(backDay)]
    for date in date_list:
        posted = Lib.checkPosted(userToken, myAccount, date.strftime("%m-%d"))
        backWeek = date.weekday()
        if posted == False:
            Lib.get_tempData(userToken, myAccount, date.strftime("%m-%d"))
            morningDo = template[WEEKS_STR[backWeek]]['morning']
            noonDo = template[WEEKS_STR[backWeek]]['noon']
            nightDo = template[WEEKS_STR[backWeek]]['night']
            res = Lib.post_tempData(userToken, myAccount, envId, envName, className, date.strftime("%m-%d"),
                morningActivity=morningDo, noonActivity=noonDo, nightActivity=nightDo)
            if res['success'] == False:
                print('[Error] {msg}'.format(msg=res['messages'][0]))
