#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author : Sma11New
# @Github : https://github.com/Sma11New

# 重写print

import os
import time

def newPrint(flag, massage, flush=False, start = "", end="\n"):
    # if not os.path.isdir('./log/'):
    #     os.mkdir('./log/')
    date = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime())
    # date = time.strftime("%H:%M:%S", time.localtime())
    if flag == "INFO":
        print(f"{start}[\033[36m{date}\033[0m]  [\033[36mINFO\033[0m]  \033[93m{massage}\033[0m", flush=flush, end=end)
    elif flag == "200":
        print(f"{start}[\033[36m{date}\033[0m]  [\033[32m200\033[0m]   \033[32m{massage}\033[0m", flush=flush, end=end)
    elif flag[:2] == "30":
        print(f"{start}[\033[36m{date}\033[0m]  [\033[93m{flag}\033[0m]    \033[93m{massage}\033[0m", flush=flush, end=end)
    elif flag[:2] == "40":
        print(f"{start}[\033[36m{date}\033[0m]  [\033[95m{flag}\033[0m]   \033[95m{massage}\033[0m", flush=flush, end=end)
    elif flag == "ERROR":
        print(f"{start}[\033[36m{date}\033[0m]  [\033[31mERRO\033[0m]  \033[31m{massage}\033[0m", flush=flush, end=end)
    else:
        pass
    # with open('./log/debug.log', "a", encoding="utf-8") as f:
    #     f.write(f"[{date}] - {flag} - {massage}\n")

if __name__ == "__main__":
    pass
