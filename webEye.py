#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author : Sma11New
# @Github : https://github.com/Sma11New

import os
import re
import csv
import time
import requests
from urllib import parse
from bs4 import BeautifulSoup
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, wait
from argparse import ArgumentParser

from colorama import init
init(autoreset=True)

from wcwidth import wcswidth as ww
def rpad(s, n, c=" "):
    return s + (n - ww(s)) * c

requests.packages.urllib3.disable_warnings()    # 抑制https错误信息

class GetWebSiteTitle:
    def __init__(self):
        self.banner()
        self.args = self.parseArgs()
        self.transformPort()
        self.init()
        self.multiRun()

    def banner(self):
        logo = rf'''       
                          )                  
         (  (      (   ( /(  (   (       (   
         )\))(    ))\  )\()) )\  )\ )   ))\  
        ((_)()\  /((_)((_)\ ((_)(()/(  /((_) 
        _(()((_)(_))  | |(_)| __|)(_))(_))      Author: Sma11New
        \ V  V // -_) | '_ \| _|| || |/ -_)  
         \_/\_/ \___| |_.__/|___|\_, |\___|  
                                 |__/        '''
        msg = f"""
\033[36m+{"-" * 70}+\033[0m
\033[36m|\033[0m  1  \033[36m|\033[0m    {rpad('Port of Web Scan    Web站点存活探测', 60)}\033[36m|\033[0m
\033[36m|\033[0m  2  \033[36m|\033[0m    {rpad('Title of Web Scan   网站标题获取', 60)}\033[36m|\033[0m
\033[36m|\033[0m  3  \033[36m|\033[0m    {rpad('ICP Find and Scan   站点ICP备案查询', 60)}\033[36m|\033[0m
\033[36m+{"-" * 70}+\033[0m
        """
        print("\033[93m" + logo + "\033[0m")
        print("\033[36m" + msg + "\033[0m")

    def init(self):
        print(f"\033[36m[*]  Thread:  {self.args.thread}")
        print(f"\033[36m[*]  Timeout:  {self.args.Timeout}")
        print(f"\033[36m[*]  TestPort:  {self.args.port}")
        msg = ""
        if os.path.isfile(self.args.file):
            msg += "\033[36m[*]  Load IP file successfully"
        else:
            msg += f"\033[31m[!]  Load url file {self.args.file} failed\033[0m"
        print(msg)
        if "failed" in msg:
            print("\033[31m[!]  Init failed, Please check the environment.")
            exit(0)
        print("\033[36m[*]  Init successfully\033[0m\n")
        self.ipList = self.loadTarget()  # 所有目标
        print(f"\033[36m[*]  IP Count: {len(self.ipList)}\033[0m\n")

    def parseArgs(self):
        date = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        # portList = "80,81,88,443,8000,8080,8081,8088,8090,8888,8181,9000"
        portList = "80,81,88,443,8080,8081,8181,9000"
        parser = ArgumentParser()
        parser.add_argument("-f", "--file", required=False, type=str, default=f"./ip.txt", help=f"The IP file, default is ./ip.txt")
        parser.add_argument("-t", "--thread", required=False, type=int, default=32, help=f"Number of thread, default is 32")
        parser.add_argument("-T", "--Timeout", required=False, type=int, default=3,  help="request timeout(default 3)")
        parser.add_argument("-p", "--port", required=False, type=str, default=portList, help=f"request port(default {portList})")
        parser.add_argument("-o", "--output", required=False, type=str, default=f"title_{date}",  help="WebSite Title output file, default is ./output/{fileName}_title_{date}.csv")
        parser.add_argument("--icp", required=False, action="store_true", default=False, help="Query ICP record information of the website, default False")
        return parser.parse_args()

    # 转换端口格式
    def transformPort(self):
        try:
            self.args.port = list(map(int, str(self.args.port).split(",")))
        except:
            print(f"\033[31mPort Error.\033[0m\n")
            exit(0)

    # 获取title
    def getTitle(self, ip):
        for port in self.args.port:
            reqURL = f"http://{ip}:{port}"
            try:
                rep = requests.get(url=reqURL, verify=False, timeout=self.args.Timeout)
                if rep.status_code == 400:  # https访问
                    reqURL = f"https://{ip}:{port}"
                rep = requests.get(url=reqURL, verify=False, timeout=self.args.Timeout)
                rep.encoding = "utf-8"
                if rep.status_code == 200:
                    title = re.findall('<title>(.*)</title>', rep.text)[0].strip()
                    if self.args.icp:
                        icpData = self.findICP(rep.text)
                        icpDataList = ["", "", "", "", ""]
                        if icpData:
                            icpDataDic = self.searchICP(icpData)
                            # print(icpDataDic)
                            if icpDataDic:
                                icpDataList = list(icpDataDic.values())
                        webDataList = [reqURL, title, icpData] + icpDataList
                        # [reqURL, title, icpData, unitName, unitType, unitHost, webName, webIndex]
                        msg = f"\033[92m[+]  {rpad(webDataList[0], 30)}{rpad(webDataList[1][:11], 24)}| {rpad(webDataList[2], 22)}| {rpad(webDataList[3], 30)}| {rpad(webDataList[4], 10)}| {rpad(webDataList[5], 5)}\033[0m"
                    else:
                        webDataList = [reqURL, title]
                        msg = f"\033[32m[+]  {reqURL:<40}{title}\033[0m"
                    self.lock.acquire()
                    try:
                        self.titleList.append(webDataList)
                        print(msg)
                    finally:
                        self.lock.release()
            except:
                pass

    # 查找页面ICP
    def findICP(self, repText):
        icpIndex = repText.find("ICP备")
        if icpIndex > 0:
            start = repText.rfind(">", 0, icpIndex) + 1
            end = repText.find("<", icpIndex)
            icpData = repText[start:end]
            return icpData.strip()
        else:
            return ""

    # ICP备案查询
    def searchICP(self, msg):
        icpEncode = parse.quote(msg.encode("utf8"))
        try:
            rep = requests.get(url=f"https://icp.chinaz.com/{icpEncode}", timeout=self.args.Timeout, verify=False)
        except:
            return False
        soup = BeautifulSoup(rep.text, 'html.parser')
        data = soup.find("ul", attrs={"class": "bor-t1s IcpMain01", "id": "first"})
        # print(data.contents[11])
        resultDic = {}
        try:
            resultDic["unitName"] = str(data.contents[1])[str(data.contents[1]).find('blank">') + 7:str(data.contents[1]).find('</a>')].strip()
        except:
            resultDic["unitName"] = ""
        try:
            resultDic["unitType"] = str(data.contents[3])[str(data.contents[3]).find('fwnone">') + 8:str(data.contents[3]).find('</strong>')].strip()
        except:
            resultDic["unitType"] = ""
        try:
            resultDic["unitHost"] = str(data.contents[5])[str(data.contents[5]).find('host=') + 5:str(data.contents[5]).find('" id=')].strip()
        except:
            resultDic["unitHost"] = ""
        try:
            resultDic["webName"] = str(data.contents[7])[str(data.contents[7]).find('<p>') + 3:str(data.contents[7]).find('</p>')].strip()
        except:
            resultDic["webName"] = ""
        try:
            resultDic["webIndex"] = str(data.contents[11])[str(data.contents[11]).find('Wzno">') + 6:str(data.contents[11]).find('</p>')].strip()
        except:
            resultDic["webIndex"] = ""
        return resultDic

    # 加载ip地址、去重
    def loadTarget(self):
        targetList = []
        with open(self.args.file) as f:
            for line in f.readlines():
                line = line.strip()
                if "https://" in line:
                    line = line.replace("https://", "")
                if "http://"  in line:
                    line = line.replace("http://", "")
                try:
                    # 允许IP文件中放入带端口的数据，如127.0.0.1:8080，截取IP
                    targetList.append(line.split(":")[0])
                except:
                    targetList.append(line)
        return list(set(targetList))

    # 多线程运行
    def multiRun(self):
        self.start = time.time()
        self.titleList = []
        self.lock = Lock()
        # executor = ThreadPoolExecutor(max_workers=self.args.thread)
        # executor.map(self.getTitle, self.ipList)
        executor = ThreadPoolExecutor(max_workers=self.args.thread)
        all = [executor.submit(self.getTitle, (url)) for url in self.ipList]
        wait(all)
        self.outputResult()

    # 输出结果
    def outputResult(self):
        fileName = list(os.path.splitext(os.path.basename(self.args.file)))[0]
        self.outputFile = f"./output/{fileName}_{self.args.output}.csv"
        if not os.path.isdir(r"./output"):
            os.mkdir(r"./output")
        with open(self.outputFile, "a", encoding="gbk", newline="") as f:
            csvWrite = csv.writer(f)
            if self.args.icp:
                csvWrite.writerow(["URL", "Title", "ICP备案号", "单位名称", "单位类型", "域名", "网站名称", "网站首页"])
            else:
                csvWrite.writerow(["URL", "Title"])
            for result in self.titleList:
                csvWrite.writerow(result)
        self.end = time.time()
        print("\nTime Spent: %.2f" % (self.end - self.start))
        print(f"{'-' * 20}\nThe result has been saved in \033[36m{self.outputFile}\033[0m\n")

if __name__ == "__main__":
    GetWebSiteTitle()