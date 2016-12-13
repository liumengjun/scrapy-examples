import os
import re
import scrapy

from .. import settings


class HomeSpider(scrapy.Spider):
    name = "home_page"
    cookie_store = {}

    host = None
    username = None
    password = None
    host_url = None
    login_url = None
    home_url = None

    output_dir = ''

    visited_urls = set()
    visited_tag_ids = set()

    _re_deny_paths = []

    def __init__(self, h=None, u=None, p=None, *args, **kwargs):
        super(HomeSpider, self).__init__(*args, **kwargs)
        self.host = h or settings.HOST
        self.username = u or settings.USERNAME
        self.password = p or settings.PASSWORD
        self.host_url = '%s://%s' % (settings.PROTOCOL, self.host)
        self.login_url = self.host_url + settings.LOGIN_PATH
        self.home_url = self.host_url + settings.HOME_PATH
        for rs in settings.DENY_PATHS:
            self._re_deny_paths.append(re.compile(rs))
        if settings.OUTPUT_DIR and self.username:
            self.output_dir = '%s/%s/' % (settings.OUTPUT_DIR, self.username)
        elif settings.OUTPUT_DIR:
            self.output_dir = '%s/' % settings.OUTPUT_DIR
        if self.output_dir:
            os.makedirs(self.output_dir, exist_ok=True)

    def set_cookie_store(self, cookies):
        self.cookie_store = cookies

    def update_cookie_store(self, cookies):
        if self.cookie_store:
            self.cookie_store.update(cookies)
        else:
            self.cookie_store = cookies

    def resolve_response_cookies(self, response):
        cookies = {}
        for s in response.headers.getlist('Set-Cookie'):
            sc = s.decode()
            pke = sc.find('=')
            if pke != -1:
                key = sc[:pke]
                pve = sc.find(';', pke)
                val = sc[pke + 1:pve]
                cookies[key] = val
        return cookies

    def write_response_to_file(self, response, page_name=''):
        segs = response.url.split("/")
        page = page_name or segs[-1] or segs[-2]
        filename = self.output_dir + 'page-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def write_tag_to_file(self, text: str, tag, tag_id):
        filename = self.output_dir + '%s-%s.html' % (tag, tag_id)
        with open(filename, 'wb') as f:
            f.write(text.encode())
        self.log('Saved tag file %s' % filename)

    def start_requests(self):
        if not self.host or not self.username or not self.password:
            print("Parameters Error!")
            return None
        self.visited_urls.add(self.host_url)
        # 开始访问第一个URL
        yield scrapy.Request(self.host_url, self.parse, headers=settings.HEADERS)

    def parse(self, response: scrapy.http.Response):
        # print(response.url)
        # print(response.headers)
        # 解析cookies
        cookies = self.resolve_response_cookies(response)
        # print(cookies)
        self.set_cookie_store(cookies)

        self.write_response_to_file(response)

        # 准备登录
        params = {settings.USERNAME_ALIAS: self.username, settings.PASSWORD_ALIAS: self.password}
        params.update(settings.DEFAULT_LOGIN_PARAMS)
        # some params in cookies, such as session_token
        for key in settings.LOGIN_KEYS_IN_COOKIE:
            if type(key) is str:
                params[key] = cookies.get(key, '')
            if type(key) is tuple or type(key) is list:
                c_v = cookies.get(key[0], '')
                p_name = key[1] if len(key) >=2 else key[0]
                p_v = key[2](c_v) if len(key) >=3 and callable(key[2]) else c_v
                params[p_name] = p_v
        yield scrapy.FormRequest(self.login_url, self.after_login, formdata=params,
                                 headers=settings.HEADERS, cookies=cookies)

    def after_login(self, response):
        # print(response.url)
        # print(response.headers)
        # 解析cookies
        cookies = self.resolve_response_cookies(response)
        # print(cookies)
        self.set_cookie_store(cookies)

        self.write_response_to_file(response)

        # 然后访问含有具体内容页面
        self.visited_urls.add(self.home_url)
        yield scrapy.Request(self.home_url, self.visit_pages,
                             headers=settings.HEADERS, cookies=self.cookie_store)

    def visit_pages(self, response):
        '''
        递归访问该网站内容页面
        '''
        self.visited_urls.add(response.url)
        self.write_response_to_file(response)

        if response.status >= 400:
            return
        if not hasattr(response, 'selector'):
            return

        # 处理想要的HTML TAGS
        tags = response.css(settings.CRAWL_TAG_NAME)
        for tag in tags:
            tag_id = tag.xpath('@id').extract_first()
            if not tag_id:
                continue
            if tag_id in self.visited_tag_ids:
                continue
            # process this tag
            self.visited_tag_ids.add(tag_id)
            text = tag.extract()
            self.write_tag_to_file(text, tag.root.tag, tag_id)

        # 处理超链接
        links = response.css('a[href]::attr(href)').extract()
        for href in links:
            # default filter
            if not href or href == '/' or href.startswith('http') or href.endswith(settings.HOME_PATH):
                continue
            # check deny paths' settings
            deny = False
            for ro in self._re_deny_paths:
                if ro.match(href):
                    deny = True
                    break
            if deny:
                continue
            # check if has visited or not
            next_url = response.urljoin(href)
            if next_url in self.visited_urls:
                continue
            # visit it
            self.visited_urls.add(next_url)
            yield scrapy.Request(next_url, self.visit_pages,
                                 headers=settings.HEADERS, cookies=self.cookie_store)

    def closed(self, reason):
        print("Count of visited pages: %s", len(self.visited_urls))
        print("Count of visited tags: %s", len(self.visited_tag_ids))
