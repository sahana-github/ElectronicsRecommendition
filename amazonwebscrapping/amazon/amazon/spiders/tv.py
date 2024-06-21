import scrapy
import pandas as pd

class TvSpider(scrapy.Spider):
    name = "tv"
    allowed_domains = ["amazon.in"]
    start_urls = [
        f"https://www.amazon.com/s?k=tv&page={page}&crid=ZZ7AZOP6XVWW&qid=1718013348&sprefix=tv%2Caps%2C316&ref=sr_pg_{page}"
        for page in range(1, 20)
    ]

    def __init__(self, *args, **kwargs):
        super(TvSpider, self).__init__(*args, **kwargs)
        self.items = []

    def parse(self, response):
        products = response.xpath('//div[@data-component-type="s-search-result"]')
        
        for tv in products:
            item = {
                'Title': tv.xpath('.//h2/a/span/text()').get(),
                'Ratings': tv.xpath('.//span[@class="a-size-base s-underline-text"]/text()').get(),
                'Before_Price': tv.xpath('.//span[@class="a-price a-text-price"]/span[2]/text()').get(),
                'After_Price': tv.xpath('.//span[@class="a-price-whole"]/text()').get(),
                'Image': tv.xpath('.//img/@src').get()
            }
            self.items.append(item)
        
        # Continue to the next page
        next_page = response.xpath('//ul[@class="a-pagination"]/li[@class="a-last"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)
        else:
            # Save to Excel file after scraping all pages
            df = pd.DataFrame(self.items)
            df.to_excel("tv.xlsx", index=False)
