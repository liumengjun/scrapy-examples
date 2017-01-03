import datetime
import scrapy


class LotteryDrawListSpider(scrapy.Spider):
    '''
    usage:
        scrapy crawl lottery-draw
        scrapy crawl lottery-draw -o draw_list.jl
        scrapy crawl lottery-draw -a day=2013-09-20
        scrapy crawl lottery-draw -a start=2013-10-01 -a end=2013-10-07
    '''
    name = "lottery-draw"

    def start_requests(self):
        url = 'http://baidu.lecai.com/lottery/draw/list/557?d='

        # only one day
        day = getattr(self, 'day', None)
        if day:
            yield scrapy.Request(url + day, self.parse)
            return

        # range: start -> end
        today = datetime.datetime.now()
        start_day = getattr(self, 'start', '2012-06-01')
        end_day = getattr(self, 'end', None)
        end_date = None
        if end_day:
            end_date = datetime.datetime.strptime(end_day, '%Y-%m-%d')
        end_date = (end_date and end_date <= today) and end_date or today
        draw_date = datetime.datetime.strptime(start_day, '%Y-%m-%d')
        while draw_date <= end_date:
            req_url = url + draw_date.strftime('%Y-%m-%d')
            draw_date += datetime.timedelta(days=1)
            yield scrapy.Request(req_url, self.parse)

    def parse(self, response):
        for item in response.css('#draw_list tbody tr'):
            day = item.css('td.td1::text').extract_first().strip()
            seq_no = item.css('td.td2::text').extract_first().strip()
            nums = item.css('td.td3 span.result span')
            num_list = []
            for n in nums:
                num_list.append(n.css('::text').extract_first())
            yield {
                'seq_no': seq_no,
                'nums': ','.join(num_list),
                'day': day,
            }
