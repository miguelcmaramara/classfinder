import scrapy

class ClassSpider(scrapy.Spider):
    name = "ClassSpider"

    def start_requests(self):
        url = 'https://www.stonybrook.edu/sb/bulletin/current/academicprograms/mec/courses.php'
        
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for course in response.css('div.course'):
            yield {
                'className': course.css('h3::text').getall(),
                'desc': course.css('h3+ p::text').getall(),
                'extras': course.css('i::text, a::text, span::text, p + p ::text').getall(),
                # 'extras': course.css('i::text , a::text , span::text , p::text , p+ p::text').getall(),
                # 'preReq': course.css('p:nth-child(3)::text').getall(),
                # 'test': course.css('p:nth-child(4)::text').getall(),
                'credits': course.css('.partial-message+ p::text, a+ p::text , p:nth-child(5)::text').getall(),
            }

