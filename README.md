## 为什么要设计cookie池
- 1.登录才能爬取
- 2.单账号会受到访问频率限制
- 3.账号过多的情况下，全部放在scrapy会难以管理
- 4.模拟登录的逻辑比较复杂
- 5.登录的逻辑写入到scrapy中后就很难把其他语言的逻辑插入进来，比如nodejs的puppeteer
- 6.把登录的逻辑单独做成一个服务会变得很灵活

## cookie池的优点
- 1.服务分离-多语言开发，和微服务的理念非常相似
- 2.组件分离-比如redis可以换成mysql等
- 3.服务分别部署，防止网站变化导致的爬虫宕机


## 需要实现的功能
- 1.模拟登录服务
- 2.cookie检测服务，因为cookie过一段时间就会失效
- 3.把cookie放入redis，通过redis作为中间件，爬虫服务和cookie服务使用不同的语言也能实现

## 需要解决的问题
- 1.如何发现cookie池不够了
- 2.各个网站的cookie如何分开进行管理
- 3.如何及时发现cookie的失效
- 4.新加入的网站如何快速接入
- 5.统一配置