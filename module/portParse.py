#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author : Sma11New
# @Github : https://github.com/Sma11New

def portParse(portDataList):
    portList = []
    for portData in portDataList:
        if "-" in str(portData):
            # 1-100
            rangeMin, rangeMax = int(portData.split("-")[0]), int(portData.split("-")[1])
            if rangeMin >= 0 and rangeMax <= 65536 and rangeMin < rangeMax:
                for i in range(rangeMin, rangeMax + 1):
                    portList.append(i)
            else:
                return False
        elif "," in str(portData):
            # 1,2,3,4,5,9
            try:
                portList = list(map(lambda x: int(x), portData.split(",")))
            except:
                return False
        elif str(portData).isdigit():
            # 3306
            if 0 <= int(portData) and 65536>= int(portData):
                portList.append(int(portData))
            else:
                return False
        else:
            return False
    return list(set(portList))

if __name__ == "__main__":
    ls = ["1","10-20","2"]
    for i in portParse(ls):
        print(i)
