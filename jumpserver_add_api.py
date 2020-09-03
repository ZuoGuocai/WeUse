#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Description: 将机器加入到Jumpserver里，需要参数主机, ip, 操作系统类型, 节点类型, 依赖monitor.yaml配置文件
# Version: v1
import yaml
import requests
import json
import sys

Params = open("./monitor.yaml", encoding="utf-8")
monitor_info = yaml.safe_load(Params)

jmpsvr = monitor_info["jumpserver"][0]


class JumpServer(object):
    def __init__(self):
        self.url = "{}:{}/api/v1".format(jmpsvr["url"], jmpsvr["port"])

    def base_request(self, url):
        header_info = {"Authorization": "Bearer " + self.get_token()}
        response = requests.get(url, headers=header_info)
        return json.loads(response.text)

    def get_token(self):
        query_args = {"username": jmpsvr["user"], "password": jmpsvr["secret"]}
        url = self.url + "/authentication/auth/"
        response = requests.post(url, data=query_args)
        return json.loads(response.text)["token"]

    def get_user_info(self):
        url = self.url + "/users/users/"
        res = self.base_request(url)
        return res

    def get_node_label_info(self, label_name):  # 获取节点信息
        url = self.url + "/assets/nodes/"
        res = self.base_request(url)
        for nodes in res:
            if label_name in nodes["name"]:
                return nodes["id"]

    def get_admin_user(self, user="gy_root"):  # 获取管理用户信息
        url = self.url + "/assets/admin-users/"
        res = self.base_request(url)
        for it in res:
            if user in it["name"]:
                return it["id"]

    def get_platform(self, platform="Linux"):  # 获取OS的系统平台信息
        res = self.base_request(self.url + "/assets/platforms/")
        for p in res:
            if platform in p["name"]:
                return p["name"]

    def create_node(self, hostname, ipaddr, port, platform, nodes, admin_user):
        url = self.url + "/assets/assets/"
        query_args = {
            "hostname": hostname,
            "ip": ipaddr,
            "protocols": "ssh/{}".format(port),
            "platform": platform,
            "nodes": nodes,
            "is_active": 1,
            "admin_user": admin_user,
        }
        header_info = {"Authorization": "Bearer " + self.get_token()}
        response = requests.post(url, data=query_args, headers=header_info)
        return response.text


if __name__ == "__main__":
    prefix_map = {
        'physical' : '公司物理机',
        'aliyun' : '阿里云',
        'sz': '深圳机房'
    }
    node_label_key = "公司虚拟机"
    
    j = JumpServer()
    host_prefix = sys.argv[1]
    host_name = sys.argv[2]
    ipaddr = sys.argv[3]
    port = sys.argv[4]
    host = host_name
    
    if host_prefix:
        node_label_key = prefix_map[host_prefix]
        host = host_prefix + '_' + host_name
    
    if host_prefix in ('physical','sz',):
        host += '_' + ipaddr[ipaddr.rindex('.')+1:]
    
    platform = j.get_platform()
    node_label = j.get_node_label_info(node_label_key)
    admin_user = j.get_admin_user()
    print(
        "创建节点成功:",
        j.create_node(host, ipaddr, port, platform, node_label, admin_user),
    )
    #python3 api.py  physical  myhost1  172.23.249.1  22
