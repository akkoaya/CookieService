# 网站账号管理
Accounts = {
    "zhihu":{
        "username":"18545531240",
        "password":"admin123456",
        "cookie_name":"zhihu_cookies", #reids里的set的名字
        "max_cookie_num":1, #可以根据网站调节，cookie池的大小
        "check_cookie_interval":30 #检擦cookie有效的时间间隔
    }
}

# REDIS管理(如果设置了账号密码，也可以输入)
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
