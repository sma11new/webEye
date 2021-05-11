#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2021/03/26

import os
import re
import csv
import time
import requests
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from argparse import ArgumentParser

class GetWebSiteTitle:
    def __init__(self):
        self.banner()
        self.args = self.parseArgs()
        self.transformPort()
        self.init()
        self.ipList = self.loadTarget()  # 所有目标
        self.multiRun()
        self.start = time.time()

    def banner(self):
        logo = r"""
    _____      ___          __  _     _____ _ _    _______ _ _   _      
   / ____|    | \ \        / / | |   / ____(_) |  |__   __(_) | | |     
  | |  __  ___| |\ \  /\  / /__| |__| (___  _| |_ ___| |   _| |_| | ___ 
  | | |_ |/ _ \ __\ \/  \/ / _ \ '_ \\___ \| | __/ _ \ |  | | __| |/ _ \
  | |__| |  __/ |_ \  /\  /  __/ |_) |___) | | ||  __/ |  | | |_| |  __/
   \_____|\___|\__| \/  \/ \___|_.__/_____/|_|\__\___|_|  |_|\__|_|\___|
                                                                
                                                                Author: Cr4y0n
        """
        msg = "Get Website Title.\n"
        print("\033[91m" + logo + "\033[0m")
        print(msg)

    def init(self):
        print("thread:", self.args.Thread)
        print("timeout:", self.args.timeout)
        print("testPort:", self.args.port)

        msg = ""
        if os.path.isfile(self.args.file):
            msg += "Load IP file successfully\n"
        else:
            msg += f"\033[31mLoad url file {self.args.file} failed\033[0m\n"
        print(msg)
        if "failed" in msg:
            print("Init failed, Please check the environment.")
            os._exit(0)
        print("Init successfully")

    def parseArgs(self):
        date = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        parser = ArgumentParser()
        parser.add_argument("-f", "--file", required=False, type=str, default=f"./ip.txt", help=f"The IP file, default is ./ip.txt")
        parser.add_argument("-T", "--Thread", required=False, type=int, default=32, help=f"Number of thread, default is 32")
        parser.add_argument("-t", "--timeout", required=False, type=int, default=3,  help="request timeout(default 3)")
        parser.add_argument("-p", "--port", required=False, type=str, default="80,81,88,443,8080,8081", help=f"request port(default 80,81,88,443,8080,8081)")
        parser.add_argument("-o", "--output", required=False, type=str, default=f"title_{date}",  help=f"WebSite Title output file, default is ./output/title_{date}.csv")
        return parser.parse_args()

    # 转换端口格式
    def transformPort(self):
        try:
            self.args.port = list(map(int, self.args.port.split(",")))
        except:
            print(f"\033[31mPort Error.\033[0m\n")
            exit(0)

    # 获取title
    def getTitle(self, ip):
        requests.packages.urllib3.disable_warnings()    # 抑制https错误信息
        for port in self.args.port:
            reqURL = f"http://{ip}:{port}"
            try:
                rep = requests.get(url=reqURL, verify=False, timeout=self.args.timeout)
                if rep.status_code == 400:  # https访问
                    reqURL = f"https://{ip}:{port}"
                rep = requests.get(url=reqURL, verify=False, timeout=self.args.timeout)
                rep.encoding = "utf-8"
                if rep.status_code == 200:
                    title = re.findall('<title>(.*)</title>', rep.text)[0].strip()
                    msg = f"{reqURL:<40}{title}"
                    self.lock.acquire()
                    try:
                        self.titleList.append([reqURL, title])
                        print(f"\033[32m[+] {msg}\033[0m")
                    finally:
                        self.lock.release()
            except:
                pass

    # 加载ip地址
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
        return targetList

    # 多线程运行
    def multiRun(self):
        # self.findCount = 0
        self.titleList = []
        self.lock = Lock()
        executor = ThreadPoolExecutor(max_workers=self.args.Thread)
        executor.map(self.getTitle, self.ipList)

    # 输出到文件
    def output(self):
        self.outputFile = f"./output/{self.args.output}.csv"
        if not os.path.isdir(r"./output"):
            os.mkdir(r"./output")
        with open(self.outputFile, "a", encoding="gbk", newline="") as f:
            csvWrite = csv.writer(f)
            csvWrite.writerow(["URL","Title"])
            for result in self.titleList:
                csvWrite.writerow(result)

    def __del__(self):
        try:
            self.end = time.time()
            timeSpent = self.end - self.start
            print("\n", "-" * 20)
            print("Time Spent: %.2f" % (timeSpent))
            self.output()
            print(f"\nThe result has been saved in {self.outputFile}\n")
        except:
            pass

if __name__ == "__main__":
    GetWebSiteTitle()