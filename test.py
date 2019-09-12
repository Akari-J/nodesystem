import pynvml
import pymysql
import json
import datetime
import paramiko
import socket
import traceback
import time
import psutil
import re
from psutil._common import sdiskpart

class nodesManagementClass:
    def __init__(self, configFilePath):
        with open(configFilePath, "r", encoding='utf-8') as f:                        
            __configObj__ = json.load(f)
            self.__db__         = __configObj__["database"]
            self.__dbName__     = self.__db__['database_name']
            self.__dbUserName__ = self.__db__['user_name']
            self.__dbPasswd__   = self.__db__['passwd']
            self.__dbHost__     = self.__db__['database_host']
            self.__port__       = 22
            self.__ssh__        = paramiko.SSHClient() 
            self.__remoteDir__  = __configObj__['remote_dir']#代码发送到子节点的路径
            self.__nodeInfoDir__= __configObj__['nodeinfo_dir']#子节点的系统信息的路径
            self.__downDir__    = __configObj__['down_path']#节点的信息下载到主节点的路径
            self.__upDir__      = __configObj__['up_path']#上传的空文件
            self.__codePath__   = __configObj__['code_path']#发送到子节点的代码在主节点上的位置
            self.__folderPath__ = __configObj__['folder']#在子节点建立的文件夹名字
            self.__ssh__.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
    def addNode(self, nodeInfo):    
        try:
            nodeInfor = json.loads(nodeInfo)
            nodeIPvn = 4
            for i in nodeInfor["nodeIP"]:
                if i == ':':
                    nodeIPvn = 6
                    break
            self.__sentCodeToNewNode__(nodeInfor["nodeIP"],nodeInfor["sshUserName"],nodeInfor["sshUserPasswd"],nodeIPvn)
            self.__runCodeInNewNode__(nodeInfor["nodeIP"],nodeInfor["sshUserName"],nodeInfor["sshUserPasswd"],nodeIPvn)
            
            with open (self.__downDir__, "r", encoding='utf-8') as f:                        
                nodeInformation = json.load(f)
                #print(nodeInformation)
                db=pymysql.connect (self.__dbHost__ ,self.__dbUserName__ ,self.__dbPasswd__ ,self.__dbName__  ,charset ='utf8' )
                cursor=db.cursor()
                cursor.execute('insert into systemNodes (nodeIPv4,nodeIPv6,nodeName,nodeCPUNum,nodeGPUs, nodeGPUNum,\
                        nodeGPUMem,nodeRAM,nodeDiskNum,nodeDiskSpace,nodeDiskIdle,createTime,updateTime,\
                        isDeleted,enabledMachine,userGroup,sshUserName,sshUserPasswd) values("{}","{}","{}","{}","{}","{}",{},{},\
                        "{}","{}","{}","{}","{}",{},{},"{}","{}","{}")'.format(nodeInformation["nodeIPv4"],\
                        nodeInformation["nodeIPv6"],nodeInformation["nodeName"],nodeInformation["nodeCPUNum"],\
                        nodeInformation["nodeGPUs"], nodeInformation["nodeGPUNum"],nodeInformation["nodeGPUMem"],\
                        nodeInformation["nodeRAM"],\
                        nodeInformation["nodeDiskNum"],nodeInformation["nodeDiskSpace"],\
                        nodeInformation["nodeDiskIdle"],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),\
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),nodeInformation["isDeleted"],\
                        nodeInformation["enabledMachine"],\
                        nodeInformation["userGroup"],nodeInfor["sshUserName"],nodeInfor["sshUserPasswd"] ))
                        #如果nodeInfo里没有createTime  用datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                db.commit()
                cursor.close()
                db.close()
                
        except Exception as e:
            print(str(e))
            return False
        else:
            return True

    def deleteNodeByIP(self, nodeIP):
        try:
            nodeIPvn = 4
            for i in nodeIP:
                if i == ':':
                    nodeIPvn = 6
                    break
            db=pymysql.connect (self.__dbHost__ ,self.__dbUserName__ ,self.__dbPasswd__ ,self.__dbName__  ,charset ='utf8' )
            cursor=db.cursor()
            if nodeIPvn == 4:
                cursor.execute('update systemnodes set isdeleted = 1 where nodeIPv4 = %s' ,(nodeIP))
            else:
                cursor.execute('update systemnodes set isdeleted = 1 where nodeIPv6 = %s' ,(nodeIP))
            db.commit()
            db.close()
        except Exception as e:
            print(str(e))
            return False
        else:
            return True

    def deleteNodeByName(self, nodeName):
        try:
            db=pymysql.connect (self.__dbHost__ ,self.__dbUserName__ ,self.__dbPasswd__ ,self.__dbName__  ,charset ='utf8' )
            cursor=db.cursor()
            cursor.execute('update systemnodes set isdeleted = 1 where nodeName = %s' ,(nodeName))
            db.commit()
            db.close()
        except Exception as e:
            print(str(e))
            return False
        else:
            return True
    
    def updateNodeInfo(self, nodeIP):
        try:   
            nodeIPvn = 4
            for i in nodeIP:
                if i == ':':
                    nodeIPvn = 6
                    break
            db=pymysql.connect (self.__dbHost__ ,self.__dbUserName__ ,self.__dbPasswd__ ,self.__dbName__  ,charset ='utf8' )
            cursor=db.cursor()
            if nodeIPvn == 4:
                cursor.execute('select sshUserName,sshUserPasswd from systemnodes where nodeipv4 = %s',nodeIP)
            else:
                cursor.execute('select sshUserName,sshUserPasswd from systemnodes where nodeipv6 = %s',nodeIP)
            r = cursor.fetchone()
            db.commit()
            aNode = {}
            aNode["sshUserName"] = r[0]
            aNode["sshUserPasswd"] = r[1]
            cursor.close()
            db.close()
            
            self.__runCodeInNewNode__(nodeIP,aNode["sshUserName"],aNode["sshUserPasswd"],nodeIPvn)
            with open (self.__downDir__, "r", encoding='utf-8') as f:                        
                aNode = json.load(f)
                db=pymysql.connect (self.__dbHost__ ,self.__dbUserName__ ,self.__dbPasswd__ ,self.__dbName__  ,charset ='utf8' )
                cursor=db.cursor()
                if nodeIPvn == 4:
                    cursor.execute('update systemnodes set nodeipv6= %s, nodeName = %s,nodeCPUNum= %s,\
                        nodeGPUs= %s, nodeGPUNum= %s,nodeGPUMem= %s,nodeRAM= %s,nodeDiskNum= %s,\
                        nodeDiskSpace= %s,nodeDiskIdle= %s,updateTime= %s where nodeIPv4 = %s',(\
                        aNode["nodeIPv6"],aNode["nodeName"],aNode["nodeCPUNum"],aNode["nodeGPUs"],\
                        aNode["nodeGPUNum"],aNode["nodeGPUMem"],aNode["nodeRAM"],\
                        aNode["nodeDiskNum"],aNode["nodeDiskSpace"],aNode["nodeDiskIdle"],\
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),nodeIP))

                else:
                    cursor.execute('update systemnodes set nodeipv4= %s, nodeName = %s,nodeCPUNum= %s,\
                        nodeGPUNum= %s,\
                        nodeGPUMem= %s,nodeRAM= %s,nodeDiskNum= %s,nodeDiskSpace= %s,nodeDiskIdle= %s,updateTime= %s where nodeIPv6 = %s' ,(\
                        aNode["nodeIPv4"],aNode["nodeName"],aNode["nodeCPUNum"],\
                        aNode["nodeGPUNum"],aNode["nodeGPUMem"],aNode["nodeRAM"],\
                        aNode["nodeDiskNum"],aNode["nodeDiskSpace"],aNode["nodeDiskIdle"],\
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),nodeIP))
                cursor.close()

                db.commit()
                db.close()
        except Exception as e:
            print(str(e))
            return False
        else:
            return True
    
    def getNodeRunningInfoByIP(self, nodeIP):
        nodeIPvn = 4
        for i in nodeIP:
            if i == ':':
                nodeIPvn = 6
                break
        db=pymysql.connect (self.__dbHost__ ,self.__dbUserName__ ,self.__dbPasswd__ ,self.__dbName__  ,charset ='utf8' )
        cursor=db.cursor()
        if nodeIPvn == 4:
            cursor.execute('select sshUserName,sshUserPasswd from systemnodes where nodeipv4 = %s',nodeIP)
        else:
            cursor.execute('select sshUserName,sshUserPasswd from systemnodes where nodeipv6 = %s',nodeIP)
        r = cursor.fetchone()
        db.commit()
        aNode = {}
        aNode["sshUserName"] = r[0]
        aNode["sshUserPasswd"] = r[1]
        cursor.close()
        db.close()  
        self.__runCodeInNewNode__(nodeIP,aNode["sshUserName"],aNode["sshUserPasswd"],nodeIPvn)
        with open (self.__downDir__, "r", encoding='utf-8') as f:                        
            info = json.load(f)
        RunningInfo = {}
        RunningInfo["RAMUsage"] = info["RAMUsage"]
        RunningInfo["CPUUsage"] = info["CPUUsage"]
        RunningInfo["GPUUsage"] = info["GPUUsage"]
        RunningInfo["DiskUsage"] = info["DiskUsage"]
        return json.dumps(RunningInfo)
        #[running information contains: CPU usage, RAM usage, Disk usage,GPU usage]

    def getNodeList(self):
        db=pymysql.connect (self.__dbHost__ ,self.__dbUserName__ ,self.__dbPasswd__ ,self.__dbName__  ,charset ='utf8' )
        cursor=db.cursor()
        cursor.execute('select nodeipv4,nodeipv6,nodename from systemnodes')
        results = cursor.fetchall()
        nodeNumber = len(results)
        db.commit()
        nodeList = []
        nodeList.append(nodeNumber)
        for r in results:
            aNode = {}
            aNode["nodeIPv4"] = r[0]
            aNode["nodeIPv6"] = r[1]
            aNode["nodeName"] = r[2]
            nodeList.append(aNode)
        cursor.close()
        db.close()
        return json.dumps(nodeList)
        #nodeList[0]是总数
  
    def getDetailNodeList(self):   
        db=pymysql.connect (self.__dbHost__ ,self.__dbUserName__ ,self.__dbPasswd__ ,self.__dbName__  ,charset ='utf8' )
        cursor=db.cursor()
        cursor.execute('select * from systemnodes')
        results = cursor.fetchall()
        nodeNumber = len(results)
        db.commit()
        nodeList = []
        nodeList.append(nodeNumber)
        print (results)
        for r in results:
            aNode = {}
            aNode["nodeIPv4"] = r[1]
            aNode["nodeIPv6"] = r[2]
            aNode["nodeName"] = r[3]
            #aNode["nodeCPUs"] = r[3]
            #aNode["nodeCPUFrequence"] = r[4]
            aNode["nodeCPUNum"] = r[6]
            aNode["nodeGPUs"] = r[7]
            aNode["nodeGPUNum"] = r[8]
            aNode["nodeGPUMem"] = r[9]
            aNode["nodeRAM"] = r[10]
            #aNode["nodeRAMFrequence"] = r[10]
            aNode["nodeDiskNum"] = r[12]
            aNode["nodeDiskSpace"] = r[13]
            aNode["nodeDiskIdle"] = r[14]
            #aNode["nodeCUDAVersion"] = r[14]
            aNode["createTime"] = r[16].strftime("%Y-%m-%d %H:%M:%S")#datetime类型不能转化为json
            aNode["updateTime"] = r[17].strftime("%Y-%m-%d %H:%M:%S")
            aNode["isDeleted"] = r[18]
            aNode["enabledMachine"] = r[19]
            aNode["userGroup"] = r[20]
            aNode["sshUserName"] = r[21]
            aNode["sshUserPasswd"] = r[22]
            nodeList.append(aNode)
            #print(aNode)
        cursor.close()
        db.close()
        return json.dumps(nodeList)
        #nodeList[0]是总数

    def __sentCodeToNewNode__(self,nodeIP,sshUserName,sshUserPasswd,nodeIPvn):
        try:
            if nodeIPvn == 4:
                self.__ssh__.connect(nodeIP, self.__port__ ,sshUserName, sshUserPasswd)
            else:
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                sock.connect((nodeIP, self.__port__))
                self.__ssh__.connect(nodeIP,username = sshUserName, password = sshUserPasswd,sock = sock)

            sftp = paramiko.SFTPClient.from_transport(self.__ssh__.get_transport())
            sftp = self.__ssh__.open_sftp()

            stdin, stdout, stderr =self.__ssh__.exec_command('ls -a')
            folders = stdout.read().decode("utf-8").split('\n')
            isExist = False
            
            for i in folders:
                if i == self.__folderPath__:
                    isExist = True
                    break
            if isExist == False:
                sftp.mkdir(self.__folderPath__)
            sftp.put(self.__upDir__,self.__nodeInfoDir__)#空json
            sftp.put(self.__codePath__,self.__remoteDir__)
            sftp.close()
            self.__ssh__.close()
        except Exception as e:
            print(str(e))
            
            return False
        else:
            return True
        #通过ssh将节点的监测代码发送到该节点的对应位置(位置默认值在config.json中配置)，此处需要通过ssh指令在默认位置创建文件夹
        #return [返回是否成功将文件传递到该节点的指定位置] 
  
    def __runCodeInNewNode__(self,nodeIP,sshUserName,sshUserPasswd,nodeIPvn):
        try:
            if nodeIPvn == 4:
                self.__ssh__.connect(nodeIP, self.__port__ ,sshUserName, sshUserPasswd)
            else:
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                sock.connect((nodeIP, self.__port__))
                self.__ssh__.connect(nodeIP,username = sshUserName, password = sshUserPasswd,sock = sock)

            sftp = paramiko.SFTPClient.from_transport(self.__ssh__.get_transport())
            sftp = self.__ssh__.open_sftp()
            
            stdin, stdout, stderr =self.__ssh__.exec_command('cd '+self.__folderPath__+'\n nohup python3 Monitor.py > log.out 2>&1 &')
            error = stderr.read().decode("utf-8")
    
            print(stdout.read())
            print(error)
            a = re.search('ModuleNotFoundError: No module named .\w*.\s',error)
            if a != None:
                module = a.group()[38:-2]
                print(module)


            time.sleep(2)
            sftp.get(self.__nodeInfoDir__,self.__downDir__)

            sftp.close()
            self.__ssh__.close()
        except Exception as e:
            print(str(e))
            return False
        else:
            return True
        
        #执行传到节点的节点监测代码，对应需要执行的命令从cmd中传入，cmd在配置文件中（config.json）中设置，命令通过ssh来执行
        #return [返回是否成功执行了上传的节点监测脚本]

if __name__ == '__main__':
    a = nodesManagementClass('D:/vs/config.json')

    diction = {"nodeIP":"192.168.4.247","sshUserName":"ubuntu","sshUserPasswd":"1"}
    data = json.dumps(diction)
    a.addNode(data)
    a.updateNodeInfo("2001:da8:8000:6880:6bff:f783:c376:de87")
    
    
