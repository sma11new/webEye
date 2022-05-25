#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author : Sma11New
# @Github : https://github.com/Sma11New

import os
import re
import csv
import time
import requests
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, wait
from module.ipParse import ipParse
from module.portParse import portParse
from module.banner import banner
from module.argsParse import parseArgs
from module.newPrint import newPrint

from colorama import init
init(autoreset=True)

requests.packages.urllib3.disable_warnings()    # 抑制https错误信息

class webEye:
    statusCodeList = [200, 301, 302, 401, 403, 404]
    def __init__(self):
        banner()
        self.argsClass = parseArgs()
        self.args = self.argsClass.parse_args()
        self.initEnvironment()
        self.multiRun()

    # 初始化环境
    def initEnvironment(self):
        newPrint("INFO", "Start Init Environment For webEye")
        if not self.args.file and not self.args.ip:
            self.argsClass.print_help()
            exit()
        if self.args.file:
            if os.path.isfile(self.args.file):
                newPrint("INFO", "Load ip file successfully")
            else:
                newPrint("ERROR", f"Load ip file {self.args.file} failed")
                exit(0)
        # newPrint("INFO", f"Init environment successfully")
        try:
            self.ipList = self.loadTargetIP()  # 所有目标
        except:
            newPrint("ERROR", f"Parse ip \"{self.args.ip}\" failed")
            exit(0)
        try:
            self.portList = portParse(list(self.args.port.split(",")))
            self.portList[0]
        except:
            newPrint("ERROR", f"Parse port \"{self.args.port}\" failed")
            exit(0)
        newPrint("INFO", f"【Thread: {self.args.thread}】 【Timeout: {self.args.Timeout}】")
        # 输出文件相关
        self.hasWriteTitle = False
        if self.args.file:
            fileName = list(os.path.splitext(os.path.basename(self.args.file)))[0]
        else:
            fileName = ""
        self.outputFile = f"./output/{fileName}_{self.args.output}.csv"
        if not os.path.isdir(r"./output"):
            os.mkdir(r"./output")
        # 生成任务列表相关
        self.targetList = []
        for ip in self.ipList:
            for port in self.portList:
                self.targetList.append([ip, port])
        self.taskCount = len(self.targetList)
        newPrint("INFO", f"【IP Count: {len(self.ipList)}】 【Task Count：{self.taskCount}】")
        newPrint("INFO", f"【TestPort: {self.args.port}】")
        newPrint("INFO", f"Init environment successfully")

    # 获取title
    def getTitle(self, ip_port):
        hasPrint = False
        reqURL = f"http://{ip_port[0]}:{ip_port[1]}"
        try:
            rep = requests.get(url=reqURL, verify=False, timeout=self.args.Timeout)
            if rep.status_code == 400:  # https访问
                reqURL = f"https://{ip_port[0]}:{ip_port[1]}"
            rep = requests.get(url=reqURL, verify=False, timeout=self.args.Timeout)
            rep.encoding = "utf-8"
            if rep.status_code in self.statusCodeList:
                try:
                    title = re.findall('<title>(.*)</title>', rep.text)[0].strip()
                except:
                    title = ""
                webDataList = [reqURL, rep.status_code, title]
                self.lock.acquire()
                try:
                    self.titleList.append(webDataList)
                    newPrint(str(rep.status_code), f"[{reqURL}][{title}]\033[0m", start="\r")
                    hasPrint = True
                    if len(self.titleList) % 20 == 0:
                        self.outputToFile(self.titleList)
                        self.titleList = []
                finally:
                    self.lock.release()
        except:
            pass
        if not hasPrint:
            self.lock.acquire()
            try:
                self.taskNum += 1
                newPrint("INFO", f"【{self.taskNum}/{self.taskCount}】  【{((self.taskNum / self.taskCount) * 100):.2f}%】", flush=True, start="\r", end="")
            finally:
                self.lock.release()

    # 加载ip地址、去重
    def loadTargetIP(self):
        targetList = []
        if self.args.ip:
            targetList = ipParse([self.args.ip])
        elif self.args.file:
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
            targetList = ipParse(targetList)
        return list(set(targetList))

    # 多线程运行
    def multiRun(self):
        self.start = time.time()
        self.titleList = []
        self.lock = Lock()
        self.taskNum = 0
        executor = ThreadPoolExecutor(max_workers=self.args.thread)
        all = [executor.submit(self.getTitle, (ip_port)) for ip_port in self.targetList]
        wait(all)
        self.end = time.time()
        print("\n\nTime Spent: %.2f" % (self.end - self.start))
        print(f"{'-' * 20}\nThe result has been saved in \033[36m{self.outputFile}\033[0m\n")

    # 输出至文件
    def outputToFile(self, resultList):
        with open(self.outputFile, "a", encoding="gbk", newline="") as f:
            csvWrite = csv.writer(f)
            if not self.hasWriteTitle:
                csvWrite.writerow(["URL", "Code", "Title"])
                self.hasWriteTitle = True
            for result in resultList:
                csvWrite.writerow(result)

if __name__ == "__main__":
    webEye()
