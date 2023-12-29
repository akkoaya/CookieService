import redis
import json
import time
from concurrent.futures import ThreadPoolExecutor,as_completed
from functools import partial #用于偏函数的定义

class CookieServer():
    def __init__(self,settings):
        #注意这里面如果需要给下面的方法引用，必须加上self
        self.redis_cli = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
        self.service_list = [] #用于存放需要启动的网站
        self.settings = settings

    def register(self,cls):
        #类似于settings里pipeline的配置，填入路径
        self.service_list.append(cls) #把class注册进来

    def login_service(self,service): #填入具体的service参数来对具体的某个网站进行调用，比如ZhihuLoginService；多个网站就调用多次这个函数就可以了
        #启动服务，并一直监听cookie池
        while 1: #建立一个死循环
            service_cli = service(self.settings) #把具体的service实例化
            service_name = service_cli.name
            cookie_num = self.redis_cli.scard(self.settings.Accounts[service_name]["cookie_name"]) #获取redis已有的cookie数量
            if cookie_num < self.settings.Accounts[service_name]["max_cookie_num"]:
                cookie_dict = service_cli.login()  # 调用login获取cookie_dict
            # 要区分不同网站的cookies，在settings里面写好，并且可以通过`service_name`定位获取，如"zhihu"
                self.redis_cli.sadd(self.settings.Accounts[service_name]["cookie_name"], json.dumps(cookie_dict))
            else:
                print(f"{service_name}的cookie池无需更新")
                time.sleep(30)

    def check_cookie_service(self,service):
        # 检查cookie是否可用，不可用就删除
        while 1:
            service_cli = service(self.settings)
            service_name = service_cli.name
            cookie_list = self.redis_cli.smembers(self.settings.Accounts[service_name]["cookie_name"])
            print(f"目前可用cookie数量：{len(cookie_list)}")
            for i,cookie_str in enumerate(cookie_list):
                cookie_dict = json.loads(cookie_str)
                valid = service_cli.check_cookie(cookie_dict)
                if not valid:
                    print(f"cookie{i+1}无效，删除")
                    self.redis_cli.srem(self.settings.Accounts[service_name]["cookie_name"], cookie_str) #srem表示redis删除集合的某个或多个元素
                    print(f"正在重新获取cookie{i+1}...")
                    self.login_service(service)
                else:
                    print(f"cookie{i+1}有效")
            #设置一个检查间隔，防止不断测试cookie是否有效而请求网页，导致被封
            interval = self.settings.Accounts[service_name]["check_cookie_interval"]
            time.sleep(interval)

    def run(self):
        task_list = []
        print("正在启动登录服务")
        login_executor =  ThreadPoolExecutor(max_workers=5) #最大线程数
        for service in self.service_list:
            #用于启动login_service
            #task = login_executor.submit(self.login_service, service)
            #对于线程池，里面最好只传递函数的名字，函数本身带参数的可以这样传，如这里的`service`,但是不易于理解，会以为后面这个参数是`submit`的参数
            #这里用偏函数解决，可以把后面传递的函数改造成没有参数的函数
            task = login_executor.submit(partial(self.login_service, service))  #partial可以把一个函数和它的参数组装成另外一个函数，这个组装的函数是没有参数的
            task_list.append(task)

        print("正在启动cookie检查服务")
        check_executor = ThreadPoolExecutor(max_workers=5)  #再启动一个线程池
        for service in self.service_list:
            #用于启动check_cookie_service
            task = check_executor.submit(partial(self.check_cookie_service, service))
            task_list.append(task)

        for future in as_completed(task_list):
            #每启动一个线程，就启动一个future，用来获取线程的返回值
            data = future.result()
            print(data)





#self.redis_cli.srandmember("zhihu_cookies") #随机获取cookie