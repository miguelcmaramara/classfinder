import scrapy

class ClassSpider(scrapy.Spider):
    name = "ClassSpider"

    def start_requests(self):
        url = 'https://www.stonybrook.edu/sb/bulletin/current/academicprograms/mec/courses.php'
        
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
        yield {
            'className': response.css('h3::text').getall(),
            'preReq': response.css('p:nth-child(3)::text').getall(),
        }

