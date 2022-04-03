from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from .utilities import  emailWrapper

class myThreadPool(object):
    '''
    def __new__(cls):  #for create singleton class 
        if not hasattr(cls, 'instance'):
            cls.instance = super(myThreadPool, cls).__new__(cls)
            return cls.instance
    '''
    # state shared by each instance
    __shared_state = dict()
 
    # constructor method
    def __init__(self):
        self.__dict__ = self.__shared_state
        self.isthreadPoolActive = 0
        self.executor = ""
 
    def __str__(self):
        return self.state

    def threadPoolInit(self):
        if self.isthreadPoolActive == 0:
            max_workers = 1
            self.executor = ThreadPoolExecutor(max_workers)
            self.isthreadPoolActive = 1
        else:
            print("threadPoolInit::ERROR")

    def addTaskToThreadPool(self, taskType, taskDataDict):
        print("addTaskToThreadPool.......::", taskType, taskDataDict)
        self.threadPoolInit()
        print("1...........")
        if taskType == "sentEmail":
            print("2...........")
            if taskDataDict["operation"] == "credentials":
                print("3...........")
                obj = emailWrapper()
                print("4...........")
                self.executor.submit(obj.credentialsOperation, taskDataDict)
                print("5...........")
        else:
            print("addTaskToThreadPool::ERROR......................")