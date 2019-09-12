# nodesystem

主节点需要的库：pynvml pymysql json datetime paramiko socket traceback time psutil re
子节点需要的库：pynvml json datetime socket psutil os

class createTable:
  def __init__(self, configFilePath):               
  #初始化
  
  def createSystemNodes(self):
  #建表 
  #其中 nodeCPUs nodeCPUFrequence nodeRAMFrequence nodeCUDAVersion字段始终为空

class nodeMonitor: #在子节点运行
    def __init__(self):
        self.__remoteDir__ = ".ds300/nodeInfo.json"
    #得到的节点信息默认写入".ds300/nodeInfo.json"
            
    def getSystemInfo(self):
    #获取节点信息  写入json文件

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
            self.__ssh__.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
    def addNode(self, nodeInfo):    
    #添加节点  返回操作是否成功

    def deleteNodeByIP(self, nodeIP):
    #根据IP删除节点  返回操作是否成功

    def deleteNodeByName(self, nodeName):
    #根据name删除节点  返回操作是否成功
    
    def updateNodeInfo(self, nodeIP):
     #根据IP更新节点信息  返回操作是否成功
    
    def getNodeRunningInfoByIP(self, nodeIP):
     #返回值为json
     #[running information contains: CPU usage, RAM usage, Disk usage,GPU usage]

    def getNodeList(self):
        return json.dumps(nodeList)
       #nodeList[0]是总数
       #获取所有节点列表
  
    def getDetailNodeList(self):   
        return json.dumps(nodeList)
        #nodeList[0]是总数
        #获取详细信息列表

    def __sentCodeToNewNode__(self,nodeIP,sshUserName,sshUserPasswd,nodeIPvn):
        #nodeIPvn表示nodeIP为IPv4还是IPv6
        #建文件夹的语句只能执行一次
        #return [返回是否成功将文件传递到该节点的指定位置] 
  
    def __runCodeInNewNode__(self,nodeIP,sshUserName,sshUserPasswd,nodeIPvn):
        #nodeIPvn表示nodeIP为IPv4还是IPv6
        #返回操作是否成功
        #若缺少库  会打印出缺少库的名字
     
