## Scrapy Example

Click [here](https://doc.scrapy.org/en/latest/intro/overview.html) see more.

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
- ``questions`` Scrapy one whole web site and certain tag, may with authentication
