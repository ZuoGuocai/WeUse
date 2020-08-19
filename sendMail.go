package main

import (
        "crypto/tls"
        "github.com/go-gomail/gomail"

)

func main() {
        m := gomail.NewMessage()
        m.SetHeader("From", "Admin@zuoguocai.com.cn")
        m.SetHeader("To", "zuoguocai@zuoguocai.com.cn","zuoguocai@126.com")
        // m.SetAddressHeader("Cc", "zuoguocai@zuoguocai.com.cn", "Dan") //抄送
        m.SetHeader("Subject", "测试") // 邮件标题
        m.SetBody("text/html", "this is 测试") // 邮件内容
        // m.Attach("/home/Alex/lolcat.jpg") //附件

        d := gomail.NewDialer("relay.zuoguocai.com.cn", 25, "IT_ZabbixAdmin@zuoguocai.com.cn", "0HUxreG")
        d.TLSConfig = &tls.Config{InsecureSkipVerify: true}
        if err := d.DialAndSend(m); err != nil {
        panic(err)
    }
}
