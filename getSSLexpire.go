package main

import (
	"crypto/tls"
	"fmt"
	"github.com/olekukonko/tablewriter"
	"net/http"
	"os"
	"strconv"
	//    "log"
	//"strings"
)

func get_info(url string) {
	tr := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}
	client := &http.Client{Transport: tr}

	seedUrl := url
	resp, err := client.Get(seedUrl)
	defer resp.Body.Close()

	if err != nil {
		fmt.Errorf(seedUrl, " 请求失败")
		panic(err)
	}

	//fmt.Println(resp.TLS.PeerCertificates[0])
	certInfo := resp.TLS.PeerCertificates[0]
	NotBefore := certInfo.NotBefore.Format("2006-01-02 15:04:05")
	NotAfter := certInfo.NotAfter.Format("2006-01-02 15:04:05")
	aa := certInfo.NotBefore
	bb := certInfo.NotAfter
	nn := bb.Sub(aa).Hours() / 24
	mm := strconv.FormatFloat(nn, 'f', 2, 64)
	//DNSNames := strings.Join(certInfo.DNSNames,"")
	//Subject := certInfo.Subject.String()
	//Issuer := certInfo.Issuer.String()

	data := [][]string{
		[]string{"https", seedUrl, NotBefore, NotAfter, mm},
	}

	table := tablewriter.NewWriter(os.Stdout)
	table.SetHeader([]string{"监控类型", "监控URL", "开始时间", "结束时间", "还有n天到期"})

	for _, v := range data {
		table.Append(v)
	}
	table.Render() // Send output

}

func main() {
/*
	var  myurl = [...]string{"https://youtube.com", "https://baidu.com", "https://vipkid.com.cn"}
	for _, v := range myurl {
		//get_info(v)
               fmt.Println(v)

	}
*/
        get_info("https://youtube.com")
        get_info("https://baidu.com")
        get_info("https://google.com")

}
