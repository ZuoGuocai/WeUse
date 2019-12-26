# !/usr/bin/env python3 
# Author: zuoguocai@126.com
# Function：获取https证书的过期时间
#           需要先执行 pip3 install pyopenssl, pip3 install zmail,  pip3 install    netifaces

from OpenSSL import SSL
import idna
from socket import socket
from datetime import datetime
import  zmail
import netifaces


def  get_ip(interface_name):
    local_ip = netifaces.ifaddresses(interface_name)[netifaces.AF_INET][0]['addr']
    return local_ip

def get_certificate(hostname, port):
    hostname_idna = idna.encode(hostname)
    sock = socket()

    sock.connect((hostname, port))
    peername = sock.getpeername()
    ctx = SSL.Context(SSL.SSLv23_METHOD) # most compatible
    ctx.check_hostname = False
    ctx.verify_mode = SSL.VERIFY_NONE

    sock_ssl = SSL.Connection(ctx, sock)
    sock_ssl.set_connect_state()
    sock_ssl.set_tlsext_host_name(hostname_idna)
    sock_ssl.do_handshake()
    cert = sock_ssl.get_peer_certificate()
    crypto_cert = cert.to_cryptography()
    sock_ssl.close()
    sock.close()
    return crypto_cert




def  get_expire(domain,port=443):
    cert=get_certificate(domain,port)
    notbefore=cert.not_valid_before
    notafter=cert.not_valid_after
    remain_days = notafter - datetime.now()	# 用证书到期时间减去当前时间
    return """<tr>
    <td style="border:1px #9cf solid;background:#fff;padding: 1px 0 1px 0; color: #153643; font-size: 12px; font-family: Arial, sans-serif;height:28px;text-align:center">https</td>
    <td style="border:1px #9cf solid;background:#fff;padding: 1px 0 1px 0; color: #153643; font-size: 12px; font-family: Arial, sans-serif;height:28px;text-align:center">""" + str(domain) + """</td>
    <td style="border:1px #9cf solid;background:#fff;padding: 1px 0 1px 0; color: #153643; font-size: 12px; font-family: Arial, sans-serif;height:28px;text-align:center">""" + str(notbefore) + """</td>
    <td style="border:1px #9cf solid;background:#fff;padding: 1px 0 1px 0; color: #153643; font-size: 12px; font-family: Arial, sans-serif;height:28px;text-align:center">""" + str(notafter) + """</td>
    <td style="border:1px #9cf solid;background:#fff;padding: 1px 0 1px 0; color: #153643; font-size: 12px; font-family: Arial, sans-serif;height:28px;text-align:center">""" + str(remain_days.days) + """</td>
    </tr>"""


def  mail_push(content_html):
    server = zmail.server('username', 'password', smtp_host='host ip or  domain', smtp_port=25,smtp_tls=True, smtp_ssl=False)
    mail = {
        'subject': 'https证书过期时间一览',
        'content_html': content_html,
    }
    server.send_mail(['zuoguocai@126.com','zuoguocai@outlook.com'],mail)


domain_list=['www.baidu.com','www.magi.com','www.google.com','www.google.cn','www.sogou.com','cn.bing.com']

from_ip = get_ip("eth0")

all_result ="监控节点:" + from_ip + "\n" + """
<h2 style="color:#FF6600 ;display:inline;text-align: center;font-family: 微软雅黑 ">https证书过期时间一览</h2>
<table align="center" border="1" cellpadding="1" cellspacing="1" width="100%" style="border-collapse: collapse;border:1px #9cf solid;">
<tr>
<td style="border:1px #fff solid;background:#66CC66;padding: 1px 0 1px 0; color: #fff; font-size: 14px; font-weight: bold; font-family: Arial, sans-serif;height:28px;text-align:center">监控类型</td>
<td style="border:1px #fff solid;background:#66CC66;padding: 1px 0 1px 0; color: #fff; font-size: 14px; font-weight: bold; font-family: Arial, sans-serif;height:28px;text-align:center">域名</td>
<td style="border:1px #fff solid;background:#66CC66;padding: 1px 0 1px 0; color: #fff; font-size: 14px; font-weight: bold; font-family: Arial, sans-serif;height:28px;text-align:center">开始时间</td>
<td style="border:1px #fff solid;background:#66CC66;padding: 1px 0 1px 0; color: #fff; font-size: 14px; font-weight: bold; font-family: Arial, sans-serif;height:28px;text-align:center">到期时间</td>
<td style="border:1px #fff solid;background:#66CC66;padding: 1px 0 1px 0; color: #fff; font-size: 14px; font-weight: bold; font-family: Arial, sans-serif;height:28px;text-align:center">还有n天到期</td>
</tr>
"""
vpn = "vpn"
for i in  domain_list:
    if vpn in i:
      result = get_expire(i,44433)
    else:
      result = get_expire(i,443)
    all_result += result

content=all_result + "</table>"
mail_push(content)
