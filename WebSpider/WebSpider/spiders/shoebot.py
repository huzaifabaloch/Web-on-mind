import scrapy
from ..items import ShoeItem


class ShoebotSpider(scrapy.Spider):

    name = 'shoebot'
    custom_settings = {
        'ITEM_PIPELINES': {
            'WebSpider.pipelines.ShoePipeline': 400
        }
    }
    start_urls = ['https://www.amazon.com/s?i=fashion-mens-intl-ship&bbn=16225019011&rh=n%3A7141123011%2Cn%3A16225019011%2Cn%3A679255011&page=1&pf_rd_i=16225019011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=554625a3-8de1-4fdc-8877-99874d353388&pf_rd_r=2ZFYEQ143CRV6H24GKR9&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1566593205&ref=sr_pg_4']
    page_number = 2

    def price_set(self, price):
        """To set the start and end price of a good."""
        
        if price != None:
            start_price = end_price = ''
            for k, each_price in enumerate(price):
                if k == 0 and each_price != None:
                    start_price = each_price
                elif k == 1 and each_price != None:
                    end_price = each_price
            if end_price == '':
                end_price = start_price
        else:
            start_price = end_price = 'NIL'
            
        return start_price, end_price

    def parse(self, response):

        # To store scraped fields in temporary containers.
        item = ShoeItem()

        # finding each block of good and storing in list.
        containers = response.css('div.sg-col-4-of-24.sg-col-4-of-12.sg-col-4-of-36.s-result-item.sg-col-4-of-28.sg-col-4-of-16.sg-col.sg-col-4-of-20.sg-col-4-of-32')

        for container in containers:

            # finding whether the th good block is actually a shoe not other.
            type_of = container.css('a.a-size-base.a-link-normal.a-text-bold::text').extract_first()
            
            if type_of != None:
                if type_of.strip() == 'Shoes' or type_of.strip() == 'Apparel' or type_of.strip() == 'Automotive':
                    image = container.css('div.a-section.aok-relative.s-image-square-aspect img::attr(src)').extract_first()
                    name = container.css('span.a-size-base-plus.a-color-base.a-text-normal::text').extract_first()
                    price = container.css('span.a-price-whole::text').extract()
                    start_price, end_price = self.price_set(price)
                    
                    item['image'] = image
                    item['name_of_shoe'] = name
                    item['start_price'] = start_price
                    item['end_price'] = end_price

                    yield item

            else:
                image = container.css('div.a-section.aok-relative.s-image-square-aspect img::attr(src)').extract_first()
                name = container.css('span.a-size-base-plus.a-color-base.a-text-normal::text').extract_first()
                price = container.css('span.a-price-whole::text').extract()
                start_price, end_price = self.price_set(price)
                    
                item['image'] = image
                item['name_of_shoe'] = name
                item['start_price'] = start_price
                item['end_price'] = end_price

                yield item

        next_page = 'https://www.amazon.com/s?i=fashion-mens-intl-ship&bbn=16225019011&rh=n%3A7141123011%2Cn%3A16225019011%2Cn%3A679255011&page=' + str(ShoebotSpider.page_number) + '&pf_rd_i=16225019011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=554625a3-8de1-4fdc-8877-99874d353388&pf_rd_r=2ZFYEQ143CRV6H24GKR9&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1566578456&ref=sr_pg_2'
        if ShoebotSpider.page_number < 6:
            ShoebotSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)



            