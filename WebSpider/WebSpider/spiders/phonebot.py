import scrapy
from ..items import PhoneItem


class PhoneBot(scrapy.Spider):

    name = 'phonebot'
    start_urls = [
        'https://www.ebay.com/b/Samsung-Cell-Phones-and-Smartphones/9355/bn_352130?rt=nc&_pgn=1'
    ]
    page_number = 2

    def parse(self, response):

        item = PhoneItem()
        phone_container = response.css('li.s-item')

        for each_phone in phone_container:

            if each_phone.css('img.s-item__image-img::attr(data-src)'):
                image_url = each_phone.css('img.s-item__image-img::attr(data-src)').extract_first()
            else:
                image_url = each_phone.css('img.s-item__image-img::attr(src)').extract_first()

            phone_name = each_phone.css('div.s-item__info.clearfix h3::text').extract_first()
            if phone_name is None:
                phone_name = each_phone.css('div.s-item__info.clearfix h3 span::text').extract_first()

            price = each_phone.css('div.s-item__detail.s-item__detail--primary span::text').extract_first()[1:].strip()

            item['image_url'] = image_url
            item['name_of_phone'] = phone_name
            item['price'] = price

            yield item

        next_page = 'https://www.ebay.com/b/Samsung-Cell-Phones-and-Smartphones/9355/bn_352130?rt=nc&_pgn=' + str(PhoneBot.page_number)
        if PhoneBot.page_number < 336:
            PhoneBot.page_number += 1
            yield response.follow(next_page, self.parse)
