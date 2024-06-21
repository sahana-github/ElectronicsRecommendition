import scrapy
import pandas as pd

class TabletsSpider(scrapy.Spider):
    name = "tablets"
    allowed_domains = ["amazon.in"]
    start_urls = [
        f"https://www.amazon.com/s?k=tablet&i=computers&rh=n%3A565108&page={page}&qid=1718011070&ref=sr_pg_{page}"
        for page in range(1, 57)
    ]

    def __init__(self, *args, **kwargs):
        super(TabletsSpider, self).__init__(*args, **kwargs)
        self.items = []

    def parse(self, response):
        products = response.xpath('//div[@data-component-type="s-search-result"]')

        for product in products:
            item = {
                'Title': product.xpath('.//h2/a/span/text()').get(),
                'Ratings': product.xpath('.//span[@class="a-size-base s-underline-text"]/text()').get(),
                'Before_Price': product.xpath('.//span[@class="a-price a-text-price"]/span[2]/text()').get(),
                'After_Price': product.xpath('.//span[@class="a-price-whole"]/text()').get(),
                'Image': product.xpath('.//img/@src').get()
            }
            self.items.append(item)

        # Continue to the next page
        next_page = response.xpath('//ul[@class="a-pagination"]/li[@class="a-last"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)
        else:
            # Save to Excel file after scraping all pages
            df = pd.DataFrame(self.items)
            df.to_excel("tablets.xlsx", index=False)

