#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author : Sma11New
# @Github : https://github.com/Sma11New

import re
from IPy import IP

# 支持的格式：
#       192.168.1.1/24
#       192.168.1.1-20
#       192.168.1.*
#       192.168.1-6.*

def IPSplitStar(ipData):  # 192.168.1.*
    ip1 = ipData.split(".")[-4]
    ip2 = ipData.split(".")[-3]
    ip3 = ipData.split(".")[-2]
    ipTo = []
    for i in range(1, 256):
        ipResult = ip1 + "." + ip2 + "." + ip3 + "." + str(i)
        ipTo.append(ipResult)
    return ipTo

def IPSplit_Star(ipData):  # 192.168.1-10.*
    ip1 = ipData.split("-")[-2].split(".")[-3]
    ip2 = ipData.split("-")[-2].split(".")[-2]
    ip3 = ipData.split("-")[-2].split(".")[-1]  # 1
    ipLast = ipData.split("-")[-1]  # 10
    ipLast1 = ipLast.split(".")[-2]
    ip3p = []
    for i in range(int(ip3), int(ipLast1) + 1):
        for j in range(1, 256):
            ip3p.append(ip1 + "." + ip2 + "." + str(i) + "." + str(j))
    return ip3p

def ipParse(ipDataList):
    ipResultList = []
    for ipData in ipDataList:
        data = ipData
        ips = re.search(r"((2[0-4]\d|25[0-5]|[01]{0,1}\d{0,1}\d)\.){3}(2[0-4]\d|25[0-5]|[01]{0,1}\d{0,1}\d)[-/]", ipData)  # Select the network segment type
        if (ips != None):
            ips = re.search(r"((2[0-4]\d|25[0-5]|[01]{0,1}\d{0,1}\d)\.){3}(2[0-4]\d|25[0-5]|[01]{0,1}\d{0,1}\d)[/]", ipData)  # Separate/type and -type
            # Processing/type
            if (ips != None):
                mask = int(data.split("/")[1])
                ipTmpList = data.split("/")[0].split(".")
                for i in range(4, int(mask / 8), -1):
                    ipTmpList[int(i) - 1] = "0"
                ipDataTmp = ".".join(ipTmpList) + f"/{mask}"
                ipList = IP(ipDataTmp)
                for i in ipList:
                    ipResultList.append(str(i))
            # process-type
            else:
                ip1 = ipData.split("-")[-2].split(".")[-4]
                ip2 = ipData.split("-")[-2].split(".")[-3]
                ip3 = ipData.split("-")[-2].split(".")[-2]
                ip4 = ipData.split("-")[-2].split(".")[-1]
                ipLast = ipData.split("-")[-1]
                ipLast.strip()
                ipLen = int(ipLast) - int(ip4) + 1
                for i in range(ipLen):
                    ipLast = int(ip4) + i
                    ipResult = ip1 + "." + ip2 + "." + ip3 + "." + str(ipLast)
                    ipResultList.append(ipResult)
        else:
            if "*" in ipData and "-" in ipData:
                ipResultList = ipResultList + IPSplit_Star(ipData)
            elif "*" in ipData:
                ipResultList = ipResultList + IPSplitStar(ipData)
            else:
                ipResultList.append(ipData)
    # return sorted(list(set(ipResultList)))  # 去重排序
    return list(set(ipResultList))  # 去重

if __name__ == "__main__":
    inputList = ["192.168.1.1/24", "192.168.2-3.*"]
    ipResultList = ipParse(inputList)
    print(ipResultList)
    print(len(ipResultList))

