from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
import time
import settings
from selenium.webdriver.chrome.service import Service
from baseservice import BaseService
import requests
class ZhihuLoginService(BaseService):
    name = "zhihu"  #这里采用和scrapy一样的方式，防止后面的文件要修改很麻烦
    def __init__(self,settings):  #注意这里传递一个settings参数，采用类似pipelines里的from_setting的方法
        self.username = settings.Accounts[self.name]["username"]
        self.password = settings.Accounts[self.name]["password"]
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-extensions') #禁用拓展
        #chrome_options.add_argument('--start - maximized') #启动时最大化
        chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
        #通过在终端输入`chrome.exe --remote-debugging-port=9222`进入托管的chrome

        #设置托管已打开的chrome时，不能有以下设置:
        # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  #设置开发者模式启动，该模式下webdriver属性为正常值
        # chrome_options.add_experimental_option('useAutomationExtension', False)  #关闭selenium对chrome driver的自动控制

        service = Service('D:/chromedriver/chromedriver.exe') #设置路径
        self.browser = webdriver.Chrome(options=chrome_options,service=service) #这里记得加上self

    def check_login(self):
        try:
            self.browser.find_element(By.CLASS_NAME, "AppHeader-userInfo")
            return True
        except Exception as e:
            return False

    def check_cookie(self,cookie_dict):
        #配置了抽象基类之后这个方法会自动执行
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
        res = requests.get("https://www.zhihu.com", headers=headers,cookies=cookie_dict,allow_redirects=False)
        if res.status_code == 200:
            return True
        else:
            return False

    def login(self):
        # self.browser.maximize_window()
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
              """
        })
        self.browser.get("https://www.zhihu.com")
        time.sleep(1)
        if not self.check_login():
            self.browser.find_element(By.CSS_SELECTOR, '.SignFlow-tabs div[class="SignFlow-tab"]').click()
            self.browser.find_element(By.CSS_SELECTOR, '.SignFlow-account input[name="username"]').send_keys(self.username)
            self.browser.find_element(By.CSS_SELECTOR, '.SignFlow-password input[name="password"]').send_keys(self.password)
            time.sleep(1)
            self.browser.find_element(By.CSS_SELECTOR, '.SignFlow-password input[name="password"]').send_keys(Keys.ENTER)
            time.sleep(10)
        else:
            time.sleep(1)
        cookies = self.browser.get_cookies()
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie['name']] = cookie['value']
        # self.browser.close()
        return cookie_dict



if __name__ == '__main__':
    zhihu = ZhihuLoginService(settings)
    cookie_dict = zhihu.login()
    print(cookie_dict)

    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    res = requests.get("https://www.zhihu.com", headers=headers, cookies=cookie_dict, allow_redirects=False)
    print(res.status_code)







