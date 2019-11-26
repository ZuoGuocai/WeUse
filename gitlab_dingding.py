#!/usr/bin/env python3
# Author: zuoguocai@126.com
# function: 通过gitlab api  获取项目id，再通过项目id 获取分支信息，通过钉钉接口，推送给群消息
import requests
import logging
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def send_dingtalk_message(sendtext):
    logger = logging.getLogger(__name__)
    DINGDING_API_URL="https://oapi.dingtalk.com/robot/send?access_token=xxx"
    data = {
        'msgtype': 'markdown',
        "markdown": {
            "title": "^_^备份通知",
            "text": "### <font color=#66CDAA size=7  face='黑体'>备份通知</font> \n\n" +
                     " *** \n\n" +
                     sendtext +
                     " *** \n\n" +
                    "<font color=#FF0000 size=7  face='黑体'>备份请登录查看: https://mygitlab.com</font> \n\n"
        }
    }
    resp = requests.post(
        DINGDING_API_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'}
    )
    if resp.status_code != 200:
        logging.exception('[REQUESTS DINGTALK API ERROR]%s' % resp.text)






def get_gitlab():
    header_info = {  "PRIVATE-TOKEN": "5BxTRtkBzxKKwjxwWyhz" }
    url1="https://mygitlab.com/api/v4/projects"
    response = requests.get(url1,headers=header_info,verify=False)
    result=json.loads(response.text)
    project_list=[]
    sendtext=""

    for i in result:
        project_id=i["id"]
        project_list.append(project_id)
    try:
        for  j in project_list:
            url2="https://mygitlab.com/api/v4/projects/" + str(j) + "/repository/branches"
            response2 = requests.get(url2,headers=header_info,verify=False)
            result2=json.loads(response2.text)
            for k in result2:
                name=[k][0]["name"]
                timesp=[k][0]["commit"]["committed_date"]
                textlog=" 项目名:" + name +"\n\n" + "> 最后备份时间:" + timesp +"\n\n" 
                print(textlog)
                sendtext += textlog
                print(sendtext)
        send_dingtalk_message(sendtext)
    except:
        print("error")

if __name__ == '__main__':      
    get_gitlab()
