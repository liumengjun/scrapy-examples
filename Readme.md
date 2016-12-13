## Scrapy Example

See more at [doc.scrapy.org](https://doc.scrapy.org/).

### run spider:
- scrapy runspider quotes_spider.py
- scrapy runspider quotes_spider.py -o quotes.jl

***interactive model:***
- scrapy shell 'http://quotes.toscrape.com/page/1/'

### startproject:
- scrapy startproject tutorial

***run spider in project:***
- scrapy crawl quotes
- scrapy crawl quotes -o quotes.jl
- scrapy crawl quotes -o quotes-humor.jl -a tag=humor


### Projects
- ``tutorial`` Demo [@doc.scrapy.org](https://doc.scrapy.org/en/latest/intro/tutorial.html)
- ``webpicker`` Scrapy one whole web site and certain html tags, may with authentication. (爬一个网站，抓取特定的html标签，支持用户登录)
