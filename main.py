from server import CookieServer
import settings
from services.zhihu import ZhihuLoginService

server = CookieServer(settings)
#注册需要启动服务的网站
server.register(ZhihuLoginService)

#启动cookie的服务
print("启动cookie池服务")
server.run()
#通过在终端输入`chrome.exe --remote-debugging-port=9222`进入托管的chrome