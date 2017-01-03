import datetime
import scrapy


class LotteryDrawListSpider(scrapy.Spider):
    name = "lottery-draw"

    def start_requests(self):
        url = 'http://baidu.lecai.com/lottery/draw/list/557?d='
        today = datetime.datetime.now()
        draw_date = datetime.datetime.strptime('2012-06-01', '%Y-%m-%d')
        while draw_date < today:
            req_url = url + draw_date.strftime('%Y-%m-%d')
            draw_date += datetime.timedelta(days=1)
            yield scrapy.Request(req_url, self.parse)

    def parse(self, response):
        for item in response.css('#draw_list tbody tr'):
            seq_no = item.css('td.td2::text').extract_first().strip()
            nums = item.css('td.td3 span.result span')
            num_list = []
            for n in nums:
                num_list.append(n.css('::text').extract_first())
            yield {
                'seq_no': seq_no,
                'nums': ','.join(num_list),
            }
