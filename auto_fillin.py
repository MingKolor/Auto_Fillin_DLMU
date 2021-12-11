import requests
import json
import sys

# 指示是否成功
flag = True
# 指示是否成功发送填报数据并获取返回值
filled = False
# 服务器返回的状态信息
state = "1"
# 服务器返回的错误信息
error = ""
students = [['张鹏程', '1120190314'],['孙世明', '1120190304']]
webhook = "https://oapi.dingtalk.com/robot/send?access_token=79e6f2ea83a3b28f4444178691f1a05b2f523f6f6380ba20aad1d3d940237670"
try:
    url = 'https://www.informationofdum.com/DMU_WEB/student_5/info/'
    for student in students:
        fillinData = {
            'jsonnumber': student[1],
            'jsonname': student[0],
            'jsonclass': "2019级硕士研究生中队",
            'morning': 35.8,
            'afternoon': 35.8,
            'night': 35.8,
            'jsonbody': 1,
            'jsonbodychangeinfo': '',
            'textarea': "学校",
            'textprople': "同学",
            'jsontouch': 1,
            'jsontouchchangeinfo': 0,
            'jsonisolate': 1,
            'jsonisolatechangeinfo': 0,
            'latitude': 38.868449,
            'longitude': 121.515136
        }
        # 121.537823,38.88503
        requests.packages.urllib3.disable_warnings()
        result = requests.post(url, data=fillinData, headers={}, verify=False)
        print(result.text)
        dict = json.loads(result.text)
        state = dict["status"]
        filled = True
        if state != "1":
            flag = False
            error = dict['message']
except:
    flag = False  # 设置状态为失败

# 打印信息
if flag:
    print("填报成功")
else:
    print("填报失败")
    if filled:
        print("错误码：" + str(state))
        print("错误信息：" + error)
# 发送钉钉通知
if len(webhook) != 0:
    message = "【疫情自动填报】"
    if flag:
        message += "填报成功\n:" + str(dict)

    elif filled:
        message += "填报失败\n错误码：" + str(state) + "\n错误信息：" + error
    else:
        message += "填报失败"
    # 要发送的数据
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        },
        "at": {
            "isAtAll": not flag
        }
    }
    response = requests.post(webhook, data=json.dumps(data), headers={"Content-Type": "application/json"})
