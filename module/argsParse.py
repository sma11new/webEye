#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author : Sma11New
# @Github : https://github.com/Sma11New

import time
from argparse import ArgumentParser

defaultPort = "80,81,88,443,4430,8080,8081,8181,8443,9000"
defaultThread = 512
defaultTimeout = 3

def parseArgs():
    date = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    parser = ArgumentParser()
    parser.add_argument("-i", "--ip", required=False, type=str, help=f"Target ip, eg:127.0.0.1/24")
    parser.add_argument("-f", "--file", required=False, type=str, help=f"Target ip list file")
    parser.add_argument("-p", "--port", required=False, type=str, default=defaultPort, help=f"request port (default {defaultPort})")
    parser.add_argument("-t", "--thread", required=False, type=int, default=512, help=f"Number of thread (default 512)")
    parser.add_argument("-T", "--Timeout", required=False, type=int, default=3, help="Request timeout (default 3)")
    parser.add_argument("-o", "--output", required=False, type=str, default=f"webEye_title_{date}", help="Output file (default ./output/webEye_title_{date}.csv)")
    example = parser.add_argument_group("examples")
    example.add_argument(action='store_false',
                         dest="python3 webEye.py -i 192.168.1.1/16\n  "
                              "python3 webEye.py -i 192.168.1.1-20,192.168.2.1/24\n  "
                              "python3 webEye.py -i 192.168.1-5.* -p 80,8080,100-999\n  "
                              "python3 webEye.py -f ipList.txt -p 1-65535")
    return parser

if __name__ == "__main__":
    pass
