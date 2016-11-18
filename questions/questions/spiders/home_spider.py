import scrapy

from .. import settings


class HomeSpider(scrapy.Spider):
    name = "home_page"

    login_path = settings.LOGIN_PATH
    home_path = settings.HOME_PATH

    def __init__(self, h=None, u=None, p=None, *args, **kwargs):
        super(HomeSpider, self).__init__(*args, **kwargs)
        self.host = h or settings.HOST
        self.username = u or settings.USERNAME
        self.password = p or settings.PASSWORD
        self.host_url = 'http://%s' % self.host
        self.login_url = self.host_url + self.login_path
        self.home_url = self.host_url + self.home_path

    def start_requests(self):
        print(self.username)
        print(self.password)
        print(self.login_url)
        if not self.host or not self.username or not self.password:
            print("Parameters Error!")
            return None
        yield scrapy.FormRequest(self.login_url, self.parse, formdata={
            'email': self.username, 'password': self.password})

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'questions-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
