import pynvml
import pymysql
import json
import datetime
import paramiko
import socket
import psutil
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

            self.__codePath__   = __configObj__['code_path']#发送到子节点的代码在主节点上的位置
            self.__ssh__.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            

    def addNode(self, nodeInfo):
        
        
        try:
            nodeInformation = json.loads(nodeInfo)
            #print(self.__codePath__, nodeInformation["nodeIPv4"])
            
            #self.__sentCodeToNewNode__(nodeInformation["nodeIPv4"],nodeInformation["sshUserName"],nodeInformation["sshUserPasswd"])
            self.__runCodeInNewNode__(nodeInformation["nodeIPv4"],nodeInformation["sshUserName"],nodeInformation["sshUserPasswd"])

            '''db=pymysql.connect (self.__dbHost__ ,self.__dbUserName__ ,self.__dbPasswd__ ,self.__dbName__  ,charset ='utf8' )
            cursor=db.cursor()
            
            cursor.execute('insert into systemNodes (nodeIPv4,nodeIPv6,nodeName,nodeCPUs,nodeCPUFrequence,nodeCPUNum,nodeGPUs, nodeGPUNum,\
                nodeGPUMem,nodeRAM,nodeRAMFrequence,nodeDiskNum,nodeDiskSpace,nodeDiskIdle,nodeCUDAVersion,createTime,updateTime,\
                isDeleted,enabledMachine,userGroup,sshUserName,sshUserPasswd) values("{}","{}","{}","{}","{}","{}","{}","{}",{},{},"{}",\
                "{}","{}","{}","{}","{}","{}",{},{},"{}","{}","{}")'.format(nodeInformation["nodeIPv4"],nodeInformation["nodeIPv6"],\
                nodeInformation["nodeName"],nodeInformation["nodeCPUs"],nodeInformation["nodeCPUFrequence"],nodeInformation["nodeCPUNum"],\
                nodeInformation["nodeGPUs"], nodeInformation["nodeGPUNum"],nodeInformation["nodeGPUMem"],nodeInformation["nodeRAM"],\
                nodeInformation["nodeRAMFrequence"],nodeInformation["nodeDiskNum"],nodeInformation["nodeDiskSpace"],\
                nodeInformation["nodeDiskIdle"],nodeInformation["nodeCUDAVersion"],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),\
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),nodeInformation["isDeleted"],nodeInformation["enabledMachine"],\
                nodeInformation["userGroup"],nodeInformation["sshUserName"],nodeInformation["sshUserPasswd"] ))
                #如果nodeInfo里没有createTime  用datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.commit()
            db.close()'''

        except Exception as e:
            print(str(e))
            return False
        else:
            return True

    def deleteNodeByIP(self, nodeIP):
        try:
            db=pymysql.connect (self.__dbHost__ ,self.__dbUserName__ ,self.__dbPasswd__ ,self.__dbName__  ,charset ='utf8' )
            cursor=db.cursor()
            
            cursor.execute('update systemnodes set isdeleted = 1 where nodeIP = %s' ,(nodeIP))
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
            db=pymysql.connect (self.__dbHost__ ,self.__dbUserName__ ,self.__dbPasswd__ ,self.__dbName__  ,charset ='utf8' )
            cursor=db.cursor()
            cursor.execute('select sshUserName, sshUserPasswd from systemnodes where nodeIP = %s' ,(nodeIP))
            results = cursor.fetchone()
            userName = results[0]
            passWd = results[1]
            # 连接SSH服务端，以用户名和密码进行认证
            self.__ssh__.connect(nodeIP, self.__port__ , userName, passWd)
            sftp = paramiko.SFTPClient.from_transport(self.__ssh__.get_transport())
            sftp.get(self.__nodeInfoDir__,self.__downDir__)
            sftp.close()
            self.__ssh__.close()
            with open(self.__downDir__, "r", encoding='utf-8') as f: 
                __nodeInfo__ = json.load(f) 
                aNode = {}
                aNode["nodeIP"] = __nodeInfo__["nodeIP"]
                aNode["nodeName"] = __nodeInfo__["nodeName"]
                aNode["nodeCPUs"] = __nodeInfo__["nodeCPUs"]
                aNode["nodeCPUFrequence"] = __nodeInfo__["nodeCPUFrequence"]
                aNode["nodeCPUNum"] = __nodeInfo__["nodeCPUNum"]
                aNode["nodeGPUs"] = __nodeInfo__["nodeGPUs"] 
                aNode["nodeGPUNum"] = __nodeInfo__["nodeGPUNum"]
                aNode["nodeGPUMem"] = __nodeInfo__["nodGPUMem"]
                aNode["nodeRAM"] = __nodeInfo__["nodeRAM"]
                aNode["nodeRAMFrequence"] = __nodeInfo__["nodeRAMFrequence"]
                aNode["nodeDiskNum"] = __nodeInfo__["nodeDiskNum"]
                aNode["nodeDiskSpace"] = __nodeInfo__["nodeDiskSpace"]
                aNode["nodeDiskIdle"] = __nodeInfo__["nodeDiskIdle"]
                aNode["nodeCUDAVersion"] = __nodeInfo__["nodeCUDAVersion"]
                aNode["createTime"] = __nodeInfo__["createTime"]
                aNode["updateTime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                aNode["isDeleted"] = __nodeInfo__["isDeleted"]
                aNode["enabledMachine"] = __nodeInfo__["enabledMachine"]
                aNode["userGroup"] = __nodeInfo__["userGroup"] 
                aNode["sshUserName"] = __nodeInfo__["sshUserName"]
                aNode["sshUserPasswd"] = __nodeInfo__["sshUserPasswd"]
            
            cursor.execute('update systemnodes set nodeName = %s,nodeCPUs= %s,nodeCPUFrequence= %s,nodeCPUNum= %s,nodeGPUs= %s, nodeGPUNum= %d,\
                nodeGPUMem= %d,nodeRAM= %d,nodeRAMFrequence= %s,nodeDiskNum= %s,nodeDiskSpace= %s,nodeDiskIdle= %s,nodeCUDAVersion= %s,updateTime= %s,\
                isDeleted= %d,enabledMachine= %d,userGroup= %s,sshUserName= %s,sshUserPasswd= %s where nodeIP = %s' ,(aNode["nodeName"],\
                aNode["nodeCPUs"],aNode["nodeCPUFrequence"],aNode["nodeCPUNum"],\
                aNode["nodeGPUs"], aNode["nodeGPUNum"],aNode["nodeGPUMem"],aNode["nodeRAM"],\
                aNode["nodeRAMFrequence"],aNode["nodeDiskNum"],aNode["nodeDiskSpace"],\
                aNode["nodeDiskIdle"],aNode["nodeCUDAVersion"],\
                aNode["updateTime"],aNode["isDeleted"],aNode["enabledMachine"],\
                aNode["userGroup"],aNode["sshUserName"],aNode["sshUserPasswd"] ,nodeIP))
            




            db.commit()
            db.close()
        except Exception as e:
            print(str(e))
            return False
        else:
            return True
    
    def getNodeRunningInfoByIP(self, nodeIP):
        RunningInfo = {}
        
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        GPUUsage = 100*info.used/info.total
        pynvml.nvmlShutdown()

        RAMUsage = psutil.virtual_memory().percent

        disk = []
        for i in psutil.disk_partitions():
            disk.append(str(psutil.disk_usage(i.device).percent))
        diskUsage = ",".join(disk)
            
        CPUUsage = psutil.cpu_percent(1,0)


        return json.dumps(RunningInfo)
        #[running information contains: CPU usage, RAM usage, Disk usage,GPU usage]

    def getNodeList(self):
        db=pymysql.connect (self.__dbHost__ ,self.__dbUserName__ ,self.__dbPasswd__ ,self.__dbName__  ,charset ='utf8' )
        cursor=db.cursor()
        cursor.execute('select nodename, nodeip from systemnodes')
        results = cursor.fetchall()
        nodeNumber = len(results)
        db.commit()
        nodeList = []
        nodeList.append(nodeNumber)
        for r in results:
            aNode = {}
            aNode['nodeName'] = r[0]
            aNode['nodeIP'] = r[1]
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
        for r in results:
            aNode = {}
            aNode["nodeIP"] = r[1]
            aNode["nodeName"] = r[2]
            aNode["nodeCPUs"] = r[3]
            aNode["nodeCPUFrequence"] = r[4]
            aNode["nodeCPUNum"] = r[5]
            aNode["nodeGPUs"] = r[6]
            aNode["nodeGPUNum"] = r[7]
            aNode["nodeGPUMem"] = r[8]
            aNode["nodeRAM"] = r[9]
            aNode["nodeRAMFrequence"] = r[10]
            aNode["nodeDiskNum"] = r[11]
            aNode["nodeDiskSpace"] = r[12]
            aNode["nodeDiskIdle"] = r[13]
            aNode["nodeCUDAVersion"] = r[14]
            aNode["createTime"] = r[15].strftime("%Y-%m-%d %H:%M:%S")#datetime类型不能转化为json
            aNode["updateTime"] = r[16].strftime("%Y-%m-%d %H:%M:%S")
            aNode["isDeleted"] = r[17]
            aNode["enabledMachine"] = r[18]
            aNode["userGroup"] = r[19]
            aNode["sshUserName"] = r[20]
            aNode["sshUserPasswd"] = r[21]
            nodeList.append(aNode)
            #print(aNode)
        cursor.close()
        db.close()
        return json.dumps(nodeList)
        #nodeList[0]是总数

    def __sentCodeToNewNode__(self,nodeIP,sshUserName,sshUserPasswd):
        try:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            sock.connect((nodeIP, self.__port__))
            self.__ssh__.connect(nodeIP,username = sshUserName, password = sshUserPasswd,sock = sock)
            sftp = paramiko.SFTPClient.from_transport(self.__ssh__.get_transport())
            sftp = self.__ssh__.open_sftp()
            
            #sftp.mkdir(self.__remoteDir__)
            
            sftp.put(self.__codePath__,self.__remoteDir__)
            #sftp.put("D:/vs/node.json",".ds300/nodeInfo.json")
            #sftp.get(".ds300/Monitor.py","D:/vs/ss.py")
            sftp.close()

            self.__ssh__.close()
        except Exception as e:
            print(str(e))
            return False
        else:
            return True
        #通过ssh将节点的监测代码发送到该节点的对应位置(位置默认值在config.json中配置)，此处需要通过ssh指令在默认位置创建文件夹
        #return [返回是否成功将文件传递到该节点的指定位置] 
  
    def __runCodeInNewNode__(self,nodeIP,sshUserName,sshUserPasswd):
        try:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            sock.connect((nodeIP, self.__port__))
            self.__ssh__.connect(nodeIP,username = sshUserName, password = sshUserPasswd,sock = sock)
            stdin, stdout, stderr = self.__ssh__.exec_command('nohup python3 -u .ds300/Monitor.py > ./log_your.out 2>&1 & echo $! >> ./[Monitor.py]pid.txt')
            print(stdout.read(),stderr.read())

            sftp = paramiko.SFTPClient.from_transport(self.__ssh__.get_transport())
            sftp = self.__ssh__.open_sftp() 
            
            sftp.get(self.__nodeInfoDir__,self.__downDir__)
            sftp.close()

            self.__ssh__.close()
        except Exception as e:
            print(str(e))
            return False
        else:
            return True
        
        #执行传到节点的节点监测代码，对应需要执行的命令从cm

if __name__ == '__main__':
    a = nodesManagementClass('D:/vs/config.json')
    '''dic = {"nodeIP":"CHAR(15)","nodeName" :"VARCHAR(30)","nodeCPUs":"VARCHAR(30)","nodeCPUFrequence":"fff","nodeCPUNum":34,\
        "nodeGPUs":"VARCHAR(30)", "nodeGPUNum":"4","nodeGPUMem" :123,"nodeRAM" :134,"nodeRAMFrequence":"bn",\
        "nodeDiskNum":20,"nodeDiskSpace":"VARCHAR(255)","nodeDiskIdle":"VARCHAR(255)","nodeCUDAVersion":111,\
        "createTime":"2019-07-21 15:08:30","updateTime" :"2019-07-21 15:24:30","isDeleted":0,"enabledMachine":1,\
        "userGroup":"VARCHAR(30)","sshUserName":"VARCHAR(30)","sshUserPasswd":"yyyyyyy"}'''
    diction = {"nodeIPv4":"2001:da8:8000:6880:6bff:f783:c376:de87","sshUserName":"ubuntu","sshUserPasswd":"1"}
    data = json.dumps(diction)

    a.addNode(data)
