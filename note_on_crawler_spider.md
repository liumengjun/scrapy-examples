# 谈 **爬虫** & scrapy框架

> 爬取网页内容，程序自动的，像蜘蛛一样把整个网的内容扫一遍。

### 基本

> 请求网站内容 -> 分析网站内容 [-> 存储获取的信息] -> 递归请求网站内容

> 比如：requests + pyquery

### 框架(python的，其他语言的等等多的是)

* scrapy
* grab
* pyspider

### 问题

* css选择器标准([https://developer.mozilla.org/zh-CN/docs/Learn/CSS/Building_blocks/Selectors](https://developer.mozilla.org/zh-CN/docs/Learn/CSS/Building_blocks/Selectors))
* 异步加载，js执行问题
* 反爬，IP代理，机器人验证(假账号)，...
* robots.txt公约(只是约定，和版权无关)

## **scrapy**框架

[https://docs.scrapy.org/en/latest/index.html](https://docs.scrapy.org/en/latest/index.html)

single spider 模式，[https://docs.scrapy.org/en/latest/intro/overview.html](https://docs.scrapy.org/en/latest/intro/overview.html)

project 模式，[https://docs.scrapy.org/en/latest/intro/tutorial.html](https://docs.scrapy.org/en/latest/intro/tutorial.html)

### selectors([https://docs.scrapy.org/en/latest/topics/selectors.html](https://docs.scrapy.org/en/latest/topics/selectors.html)):

* css
* xpath
* 其他

### js处理([https://docs.scrapy.org/en/latest/topics/dynamic-content.html](https://docs.scrapy.org/en/latest/topics/dynamic-content.html)):

* scrapy-splash
* scrapy-selenium

### 架构

> [https://docs.scrapy.org/en/latest/topics/architecture.html](https://docs.scrapy.org/en/latest/topics/architecture.html)

> [Twisted](https://twistedmatrix.com/trac/) 事件驱动异步框架(**异步**：大家都知道，每次网络请求都很慢，所以需要异步)

![Scrapy architecture](https://docs.scrapy.org/en/latest/_images/scrapy_architecture_02.png)

主要写spiders，处理response内容：返回item，用户item pipelines保存或直接输出；返回requests，又交给engine再去获取新的内容。

获取网络内容，网络代理，js处理等在downloader模块。

延时或者去重在scheduler模块。

## 延伸

* 浏览器插件是否可以变成爬虫
* headless浏览器
* [https://www.zhihu.com/question/60280580](https://www.zhihu.com/question/60280580)