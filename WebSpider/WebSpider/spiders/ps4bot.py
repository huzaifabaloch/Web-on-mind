import scrapy
from ..items import Ps4Item
from scrapy.crawler import CrawlerProcess


class Ps4botSpider(scrapy.Spider):
    """
    This class inherited from Spider class which will have all the 
    functionalities of it.
    """
    # ! The Spider class expects us to have name of bot and target url.

    pipelines = ['ps4bot']
    custom_settings = {
        'ITEM_PIPELINES': {
            'WebSpider.pipelines.Ps4Pipeline': 400
        }
    }

    name = 'ps4bot' # name of the spider that will crawl pages.
    # link that spider will start to crawl.
    start_urls = ['https://www.amazon.com/s?i=videogames-intl-ship&bbn=16225016011&rh=n%3A16225016011%2Cn%3A6427814011&page=1&_encoding=UTF8&qid=1566505817&ref=sr_pg_2']
    page_number = 2

    def parse(self, response):
        """
        The method where spider extract information from HTML based on CSS 
        selectors.The scrapy returns response object that contain all the 
        source code of a webpage. A special method from spider class that
        contain response object whichwill hold the entire source code of target 
        webpage. The Spider class expects us to have name of bot and target url
        In this method we start parsing the pages and extract required fields
        from it and keep on crawling.
        """
        # Extracting image links, game names, and their prices. 
        image_link = name = price = ''
  
        # Creating an instance to store fields in temporary containers.
        item = Ps4Item()

        # product selector list. (MAIN BLOCK WHERE ALL PRODUCT ARE PRESENT)
        containers = response.css('div.sg-col-20-of-24.s-result-item.sg-col-0-of-12.sg-col-28-of-32.sg-col-16-of-20.sg-col.sg-col-32-of-36.sg-col-12-of-16.sg-col-24-of-28')

        for container in containers:
            
            # This part is used to find the type of game (in this case PS4) and adding into type_of_game for validation.
            main_container = container.css('div.sg-col-4-of-12.sg-col-8-of-16.sg-col-16-of-24.sg-col-12-of-20.sg-col-24-of-32.sg-col.sg-col-28-of-36.sg-col-20-of-28')
            type_of_game = main_container.css('div.sg-col-inner a.a-size-base.a-link-normal.a-text-bold::text').extract_first()
            if type_of_game != None:
                if type_of_game.strip() == 'PlayStation 4':

                    # extracting of images of game.
                    image_link = container.css('div.sg-col-4-of-24.sg-col-4-of-12.sg-col-4-of-36.sg-col-4-of-28.sg-col-4-of-16.sg-col.sg-col-4-of-20.sg-col-4-of-32 img::attr(src)').extract_first()
                    # Adding to the temporary container.
                    item['image'] = image_link

                    for key_contain, row in enumerate(main_container.css('div.sg-row')):
                
                        if key_contain == 0 and type_of_game.strip() == 'PlayStation 4':
                        
                            # extracting of name of game.
                            name = row.css('a.a-link-normal.a-text-normal span.a-size-medium.a-color-base.a-text-normal::text').extract_first()
                            # Adding to the temporary container
                            item['name_of_game'] = name

                        elif key_contain == 1 and  type_of_game.strip() == 'PlayStation 4':

                            # extracting of name of game.
                            price = row.css('span.a-price span.a-price-whole::text').extract_first() 
                            # Adding to the temporary container
                            item['price'] = price

                    # returning back as generator
                    yield item

        next_page = 'https://www.amazon.com/s?i=videogames-intl-ship&bbn=16225016011&rh=n%3A16225016011%2Cn%3A6427814011&page=' + str(Ps4botSpider.page_number) + '&_encoding=UTF8&qid=1566505817&ref=sr_pg_2'
        if Ps4botSpider.page_number < 9:
            Ps4botSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
