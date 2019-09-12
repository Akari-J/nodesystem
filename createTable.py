
#create database node character set utf8;

import pymysql
import json

class createTable:
        def __init__(self, configFilePath):               
                with open(configFilePath, "r", encoding='utf-8') as f:                        
                        __configObj__ = json.load(f)
                        self.__db__        = __configObj__['database']
                        self.__dbName__    = self.__db__['database_name']
                        self.__dbUserName__= self.__db__['user_name']
                        self.__dbPasswd__  = self.__db__['passwd']
                        self.__dbHost__    = self.__db__['database_host']
        def createSystemNodes(self):
                db=pymysql.connect (self.__dbHost__ ,self.__dbUserName__ ,self.__dbPasswd__ ,self.__dbName__  ,charset ='utf8' )
                cursor=db.cursor()
                #print("123")
                cursor.execute("CREATE TABLE systemNodes (\
                        id                INT not null auto_increment primary key,\
                        nodeIPv4          VARCHAR(255),\
                        nodeIPv6          VARCHAR(255),\
                        nodeName          VARCHAR(30),\
                        nodeCPUs          VARCHAR(30),\
                        nodeCPUFrequence  CHAR(5),\
                        nodeCPUNum        CHAR(2),\
                        nodeGPUs          VARCHAR(30) ,\
                        nodeGPUNum        CHAR(1),\
                        nodeGPUMem        BIGINT,\
                        nodeRAM           BIGINT,\
                        nodeRAMFrequence  CHAR(5),\
                        nodeDiskNum       CHAR(2),\
                        nodeDiskSpace     VARCHAR(255),\
                        nodeDiskIdle      VARCHAR(255),\
                        nodeCUDAVersion   CHAR(4),\
                        createTime        DATETIME,\
                        updateTime        DATETIME,\
                        isDeleted         BOOL,\
                        enabledMachine    BOOL,\
                        userGroup         VARCHAR(30),\
                        sshUserName       VARCHAR(30),\
                        sshUserPasswd     VARCHAR(30))")
                db.commit()
                db.close()


a = createTable('D:/vs/config.json')
a.createSystemNodes()
