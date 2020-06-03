#!/usr/bin/env python3
##########################################
# author: zuoguocai@126.com
# description: 
# 通过 groupname 获取 groupid
# 通过 groupid   获取 hostid ,hostname
# 通过 hostid    获取 interface ip
##########################################
import json
import requests
import urllib3
from openpyxl import Workbook
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

  
class zabbix_api:

        def __init__(self):
            self.url = 'https://zabbix.xxx.com/api_jsonrpc.php' #修改URL


        def export_excel(self,data):
            wb = Workbook()
            # ws = wb.active
            ws = wb.worksheets[0]
            ws.append(['ID','SN','IP'])

            for r in data:
                ws.append(r)

            wb.save("zabbix.xlsx")
              
              
        def user_login(self):
            data = json.dumps({
                               "jsonrpc": "2.0",
                               "method": "user.login",
                               "params": {
                                          "user": "username", #web页面登录用户名
                                          "password": "password" #web页面登录密码
                                          },
                               "id": 0
                               })
 
          
            try:
                resp = requests.post(self.url, data,headers={'Content-Type': 'application/json'},verify = False)
            except requests.exceptions.ConnectionError:
                print("\033[041m 用户认证失败，请检查 !\033[0m")
            else:
                response = resp.json()
                self.authID = response['result']
                return self.authID

        def hostgroup_get(self, hostgroupName=''):
            data = json.dumps({
                               "jsonrpc":"2.0",
                               "method":"hostgroup.get",
                               "params":{
                                         "output": "extend",
                                         "filter": {
                                                    "name": hostgroupName
                                                    }
                                         },
                               "auth":self.user_login(),
                               "id":1,
                               })
              
                   
            try:
                resp = requests.post(self.url, data,headers={'Content-Type': 'application/json'},verify = False)
            except requests.exceptions.ConnectionError as e:
                print("Error as ", e)
            else:
                response = resp.json()
                for group in response['result']:
                        if  len(hostgroupName)==0:
                                print("hostgroup:  \033[31m%s\033[0m \tgroupid : %s" %(group['name'],group['groupid']))
                        else:
                                print("hostgroup:  \033[31m%s\033[0m\tgroupid : %s" %(group['name'],group['groupid']))
                                self.hostgroupID = group['groupid']
                                return group['groupid']




        def hostinterface_get(self, hostids=''):
            data = json.dumps({
                               "jsonrpc":"2.0",
                               "method":"hostinterface.get",
                               "params":{
                                         "hostids":hostids,
                                         },
                               "auth":self.user_login(),
                               "id":1,
                               })

            try:
                resp = requests.post(self.url, data,headers={'Content-Type': 'application/json'},verify = False)
            except requests.exceptions.ConnectionError as e:
                print("Error as ", e)
            else:
                response = resp.json()
                for interface in response['result']:
                    return interface['ip']


              
        def host_get(self,groupids=''):
            server_list = []
            data=json.dumps({
                    "jsonrpc": "2.0",
                    "method": "host.get",
                    "params": {
                              "groupids":groupids,
                              },
                    "auth": self.user_login(),
                    "id": 1
                    })
                  
            try:
                resp = requests.post(self.url, data,headers={'Content-Type': 'application/json'},verify = False)
            except requests.exceptions.ConnectionError as e:
                print("Error as ", e)
            else:
                response = resp.json()
                for host in response['result']:
                    ip = self.hostinterface_get(host["hostid"])
                    server_list.append([host["hostid"],host["name"],ip])
                return server_list



if __name__ == "__main__":
        zabbix = zabbix_api()
        group_id = zabbix.hostgroup_get("服务器硬件")
        host_id = zabbix.host_get(group_id)
        zabbix.export_excel(host_id)
