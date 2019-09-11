import pynvml
import json
import datetime
import socket
import psutil
import os
from psutil._common import sdiskpart

class nodeMonitor:
    def __init__(self):
        #with open(configFilePath, "r", encoding='utf-8') as f:                        
            #__configObj__ = json.load(f)
        self.__remoteDir__ = ".ds300/nodeInfo.json"
            

    def getSystemInfo(self):
        thisNode = {}
        hostName=socket.gethostname()
        thisNode["nodeIPv4"]= os.popen("ifconfig | grep -A 5 'enp'| grep 'inet addr:' | cut -d: -f2 ").read().split()[0]
        thisNode["nodeIPv6"] = os.popen("ifconfig | grep -A 5 'enp'| grep 'inet6 addr:' | grep 'Global' ").read().split()[2].split('/')[0]
        thisNode["nodeName"] = hostName
        #thisNode["nodeCPUs"] = psutil.name()
        #thisNode["nodeCPUFrequence"] = psutil.cpu_freq().current
        thisNode["nodeCPUNum"] = str(psutil.cpu_count())
        thisNode["CPUUsage"] = psutil.cpu_percent(1,0)
        pynvml.nvmlInit()
        deviceCount = pynvml.nvmlDeviceGetCount()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        thisNode["nodeGPUs"] = str(pynvml.nvmlDeviceGetName(handle))
        thisNode["nodeGPUNum"] = deviceCount
        thisNode["nodeGPUMem"] = info.total # total  free  used
        thisNode["GPUUsage"] = 100*info.used/info.total
        pynvml.nvmlShutdown()

        thisNode["nodeRAM"] = psutil.virtual_memory().total
        thisNode["RAMUsage"]= psutil.virtual_memory().percent

        diskNum = len(psutil.disk_partitions())
        diskSpace = []
        diskIdle = []
        diskUsage = []
        for i in psutil.disk_partitions():
            diskSpace.append(str(psutil.disk_usage(i.device).total))
            diskIdle.append(str(psutil.disk_usage(i.device).free))
            diskUsage.append(str(psutil.disk_usage(i.device).percent))

        thisNode["nodeDiskNum"] = diskNum
        thisNode["nodeDiskSpace"] = ",".join(diskSpace)
        thisNode["nodeDiskIdle"] = ",".join(diskIdle)
        thisNode["DiskUsage"] = ",".join(diskUsage)
        
        thisNode["createTime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")#datetime类型不能转化为json
        
        thisNode["isDeleted"] = 0
        thisNode["enabledMachine"] = 1
        thisNode["userGroup"] = "admin"
        print(thisNode)
        #for item in thisNode.keys():
        #    print(type(thisNode[item]))

        with open("nodeInfo.json","w",encoding='utf-8') as f:
            json.dump(thisNode,f)
        return True


a=nodeMonitor()
a.getSystemInfo()