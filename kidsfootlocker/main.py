import requests
import json

with open('orders.json') as json_file:
    orders = json.load(json_file)

def checkOrder(orderNum, customerNum, importantCookie):
    print("checking status of " + orderNum)
    session = requests.Session()

    sessionHeaders = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "content-type": "application/json"
    }

    cookies = {
        '_abck':importantCookie
    }

    s = session.get('https://www.kidsfootlocker.com/api/session', headers=sessionHeaders, cookies=cookies)
    loadedData = json.loads(s.text)
    csrfToken = loadedData['data']['csrfToken']

    headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
    "accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "content-type": "application/json",
    "x-csrf-token":csrfToken
    }

    payload = {
        "code":orderNum,
        "customerNumber":customerNum
    }


    checkReq = session.post('https://www.kidsfootlocker.com/api/users/orders/status', headers=headers, json=payload, cookies=cookies)

    if 200 == checkReq.status_code:
        jsonStatus = json.loads(checkReq.text)
        orderStatus1 = jsonStatus['orderStatus']
        orderStatus2 = jsonStatus['lineItems'][0]['itemStatus']

        print("status of " + orderNum + " is " + orderStatus1 + " and " + orderStatus2)
    elif "match" in checkReq.text:
        print("error with order numbers or/and customer numbers, please check order numbers or/and customer numbers")
        exit()
    else:
        print("cookie expired! please get a new cookie")
        importantCookie = input("please paste cookie here: ")
        checkOrder(orderNum, cusNum, importantCookie)

def getCookie():
    global importantCookie 
    importantCookie = input("please paste cookie here: ")
getCookie()


for i in orders["orders"]:
    orderNum = i['orderNum']
    cusNum = i['customerNum']
    checkOrder(orderNum, cusNum, importantCookie)




