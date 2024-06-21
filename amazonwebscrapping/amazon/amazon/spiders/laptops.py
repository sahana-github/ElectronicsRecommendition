import scrapy
import pandas as pd

class LaptopsSpider(scrapy.Spider):
    name = "laptops"
    allowed_domains = ["amazon.in"]
    start_urls = [
        f"https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page={page}&qid=1718006018&ref=sr_pg_{page}"
        for page in range(1, 400)
    ]

    def __init__(self, *args, **kwargs):
        super(LaptopsSpider, self).__init__(*args, **kwargs)
        self.items = []

    def parse(self, response):
        products = response.xpath('//div[@data-component-type="s-search-result"]')

        for product in products:
            item = {
                'Title': product.xpath('.//h2/a/span/text()').get(),
                'Rating_Count': product.xpath('.//span[@class="a-size-base s-underline-text"]/text()').get(),
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
            df.to_excel("laptop.xlsx", index=False)
