import pynvml
import pymysql
import json
import datetime
import paramiko
import socket
import psutil
from psutil._common import sdiskpart

class nodeMonitor:
    def __init__(self):
        #with open(configFilePath, "r", encoding='utf-8') as f:                        
            #__configObj__ = json.load(f)
        self.__remoteDir__ = ".ds300/nodeInfo.json"
            

    def getSystemInfo(self):
        thisNode = {}
        hostName=socket.gethostname()
        #thisNode["nodeIPv4"] = socket.gethostbyname(hostName)
        thisNode["nodeIPv6"] =  socket.getaddrinfo(socket.gethostname(),None)[0][4][0]
        thisNode["nodeName"] = hostName
        #thisNode["nodeCPUs"] = psutil.name()
        #thisNode["nodeCPUFrequence"] = psutil.cpu_freq().current
        thisNode["nodeCPUNum"] = psutil.cpu_count()

        pynvml.nvmlInit()
        deviceCount = pynvml.nvmlDeviceGetCount()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        thisNode["nodeGPUs"] = str(pynvml.nvmlDeviceGetName(handle))
        thisNode["nodeGPUNum"] = deviceCount
        thisNode["nodeGPUMem"] = info.total # total  free  used
        pynvml.nvmlShutdown()

        thisNode["nodeRAM"] = psutil.virtual_memory().total
        #thisNode["nodeRAMFrequence"] = r[10]
        diskNum = len(psutil.disk_partitions())
        diskSpace = []
        diskIdle = []
        for i in psutil.disk_partitions():
            diskSpace.append(str(psutil.disk_usage(i.device).total))
            diskIdle.append(str(psutil.disk_usage(i.device).free))

        thisNode["nodeDiskNum"] = diskNum
        thisNode["nodeDiskSpace"] = ",".join(diskSpace)
        thisNode["nodeDiskIdle"] = ",".join(diskIdle)

        #thisNode["nodeCUDAVersion"] = r[14]
        
        thisNode["createTime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")#datetime类型不能转化为json
        
        thisNode["isDeleted"] = 0
        thisNode["enabledMachine"] = 1
        thisNode["userGroup"] = "admin"
        print(thisNode)
        #for item in thisNode.keys():
        #    print(type(thisNode[item]))

        with open(".ds300/nodeInfo.json","w",encoding='utf-8') as f:
            json.dump(thisNode,f)
        return True


a=nodeMonitor()
a.getSystemInfo()