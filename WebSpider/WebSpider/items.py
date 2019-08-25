# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Ps4Item(scrapy.Item):
    """
    Defining the fields that spider will scrape and store them in temporary
    containers called fields. so we can easily store them in any format
    like (csv, json, db).
    """

    # PS4 fields
    image = scrapy.Field()
    name_of_game = scrapy.Field()
    price = scrapy.Field()


class ShoeItem(scrapy.Item):

    image = scrapy.Field()
    name_of_shoe = scrapy.Field()
    start_price = scrapy.Field()
    end_price = scrapy.Field()

