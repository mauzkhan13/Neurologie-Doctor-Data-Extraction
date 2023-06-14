import scrapy
from time import  sleep
import re

class DoctorSpider(scrapy.Spider):
    name = "doctor"
    start_urls = ['https://www.arzt-auskunft.de/neurologie/']

    def __init__(self):
        self.current_page_number = 1
        self.scraped_pages = 0
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response):
        d_urls = response.xpath('//a[@class="btn-detail"]/@href').getall()
        for index, url in enumerate(d_urls):
            yield scrapy.Request(url=url, callback=self.parse_item,
                                 meta={'page_number': self.current_page_number, 'index': index})
    
    
        self.current_page_number += 1
    
        if self.current_page_number <= 91:
            next_page_url = f"https://www.arzt-auskunft.de/neurologie/{self.current_page_number}/"
            yield scrapy.Request(next_page_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        page_number = response.meta['page_number']

        index = response.meta['index']
        
        url = response.url

        names = response.xpath('//h1[@class="fs2"]/text()').getall()
        corrected_names = [' '.join(name.split()) for name in names]

        addresses = response.xpath('//div[@itemprop="address"]/span/text()').getall()
        corrected_address = [' '.join(address.split()) for address in addresses]

        fax = response.xpath('//span[@itemprop="fax"]/text()').get()
        fax = fax if fax else 'Not Available'

        phone = response.xpath('//span[@itemprop="telephone"]/a/text()').get()
        phone = phone if phone else 'Not Available'

        yield {
            'Page Number': page_number,
            'Name': corrected_names,
            'Address': corrected_address,
            'Fax Number': fax,
            'Phone Number': phone,
            'Index': index,
            'URL': url,
        }

        self.scraped_pages += 1
        
        if self.scraped_pages >= 91:
            return
