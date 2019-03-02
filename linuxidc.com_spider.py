# -*- coding: utf-8 -*-
import time
import random
import scrapy


class LinuxidcSpider(scrapy.Spider):
    name = 'linuxidc'
    allowed_domains = ['linux.linuxidc.com']
    start_urls = ['https://linux.linuxidc.com/']
    visited = set()

    def parse(self, response):
        for link in response.css('a[href]'):
            href = link.xpath('@href').extract()
            text = link.xpath('.//text()').extract()
            # print('a'.center(80,'-'))
            # print(href)
            # print(text)
            # print('<a href="%s">%s</a>' % (href[0], text and text[0] or None))
            if href[0].startswith('index.php?folder') and (href[0] not in self.visited):
                self.visited.add(href[0])
                print('f'.center(80,'-'))
                print('<a href="%s">%s</a>' % (href[0], text and text[0] or None))
                time.sleep(0.5+random.random())
                yield scrapy.Request('https://linux.linuxidc.com/%s' % href[0], callback=self.parse)
            if href[0].startswith('linuxconf/download.php'):
                print('d'.center(80,'-'))
                print('<a href="%s">%s</a>' % (href[0], text and text[0] or None))
                pass
        pass
