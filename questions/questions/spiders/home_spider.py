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

    def __init__(self, h=None, u=None, p=None, *args, **kwargs):
        super(HomeSpider, self).__init__(*args, **kwargs)
        self.host = h or settings.HOST
        self.username = u or settings.USERNAME
        self.password = p or settings.PASSWORD
        self.host_url = '%s://%s' % (settings.PROTOCOL, self.host)
        self.login_url = self.host_url + settings.LOGIN_PATH
        self.home_url = self.host_url + settings.HOME_PATH

    def set_cookie_store(self, cookies):
        self.cookie_store = cookies

    def update_cookie_store(self, cookies):
        if self.cookie_store:
            self.cookie_store.update(cookies)
        else:
            self.cookie_store = cookies

    def start_requests(self):
        # print(self.username)
        # print(self.password)
        # print(self.login_url)
        if not self.host or not self.username or not self.password:
            print("Parameters Error!")
            return None
        yield scrapy.Request(self.host_url, self.parse, headers=settings.HEADERS)

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
        page = response.url.split("/")[-2] or page_name
        filename = 'questions-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def parse(self, response: scrapy.http.Response):
        # print(response.url)
        # print(response.status)
        # print(response.headers)
        cookies = self.resolve_response_cookies(response)
        # print(cookies)
        self.set_cookie_store(cookies)

        self.write_response_to_file(response)

        params = {'email': self.username, 'password': self.password, 'remeber': "0", 'next_url': ""}
        for key in settings.LOGIN_KEYS_IN_COOKIE:
            params[key] = cookies.get(key, '')
        yield scrapy.FormRequest(self.login_url, self.after_login, formdata=params,
                                 headers=settings.HEADERS, cookies=cookies)

    def after_login(self, response):
        # print(response.url)
        # print(response.status)
        # print(response.headers)
        cookies = self.resolve_response_cookies(response)
        # print(cookies)
        self.set_cookie_store(cookies)

        self.write_response_to_file(response)

        yield scrapy.Request(self.home_url, self.visit_pages,
                             headers=settings.HEADERS, cookies=self.cookie_store)

    def visit_pages(self, response):
        self.write_response_to_file(response)
