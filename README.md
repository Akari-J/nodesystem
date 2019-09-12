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
            #self.__remoteDir__  #代码发送到子节点的路径
            #self.__nodeInfoDir__#子节点的系统信息的路径
            #self.__downDir__  #节点的信息下载到主节点的路径
            #self.__upDir__    #上传的空文件
            #self.__codePath__  #发送到子节点的代码在主节点上的位置
            
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
     
