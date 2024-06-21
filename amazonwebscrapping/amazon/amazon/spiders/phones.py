import scrapy
import pandas as pd

class PhonesSpider(scrapy.Spider):
    name = "phones"
    allowed_domains = ["amazon.in"]
    start_urls = [
        f"https://www.amazon.in/s?k=phones&i=electronics&page={page}&crid=2713ZGFZU5MTB&qid=1717930961&sprefix=%2Celectronics%25"
        for page in range(1, 400)
    ]

    def __init__(self, *args, **kwargs):
        super(PhonesSpider, self).__init__(*args, **kwargs)
        self.items = []

    def parse(self, response):
        products = response.xpath('//div[@data-component-type="s-search-result"]')
        
        for phone in products:
            item = {
                'Title': phone.xpath('.//h2/a/span/text()').get(),
                'Ratings': phone.xpath('.//div[@class="a-row a-size-small"]/span[2]/a/span/text()').get(),
                'Before_Price': phone.xpath('.//span[@class="a-price a-text-price"]/span[2]/text()').get(),
                'After_Price': phone.xpath('.//span[@class="a-price-whole"]/text()').get(),
                'Image': phone.xpath('.//img/@src').get()
            }
            self.items.append(item)
        
        # Continue to the next page
        next_page = response.xpath('//ul[@class="a-pagination"]/li[@class="a-last"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)
        else:
            # Save to Excel file after scraping all pages
            df = pd.DataFrame(self.items)
            df.to_excel("Phone.xlsx", index=False)
