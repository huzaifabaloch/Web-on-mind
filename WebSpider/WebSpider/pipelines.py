# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector


class Ps4Pipeline(object):
    """
    To store data of Ps4 games in some sort of database.
    like sqlite3, mysql, mongodb etc.
    """

    def __init__(self):

        self.create_connection()
        self.create_table()

    def create_connection(self):

        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='abc123',
            database='web_on_mind'
        )

        self.my_cursor = self.conn.cursor()

    def create_table(self):

        self.my_cursor.execute("""DROP TABLE IF EXISTS ps4_tbl""")
        self.my_cursor.execute("""CREATE TABLE ps4_tbl(
            name_of_game text,
            price text,
            image_link text
        )""")

    def store_data(self, item):

        self.my_cursor.execute("""INSERT INTO ps4_tbl VALUES (%s, %s, %s)""",
        (
            item['name_of_game'],
            item['price'],
            item['image']
        ))

        self.conn.commit()

    def process_item(self, item, spider):

        self.store_data(item)
        return item


# -------------------------------------------------------------------------
class PhonePipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):

        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='abc123',
            database='web_on_mind'
        )
        self.cursor = self.conn.cursor()

    def create_table(self):

        self.cursor.execute('DROP TABLE IF EXISTS phone_tbl')
        self.cursor.execute("""CREATE TABLE phone_tbl (
            name_of_phone text,
            price text,
            image_url text
            )
        """)

    def store_data(self, item):

        self.cursor.execute("""INSERT INTO phone_tbl VALUES (%s, %s, %s)""", (
                    item['name_of_phone'],
                    item['price'],
                    item['image_url']
                )
            )
        self.conn.commit()

    def process_item(self, item, spider):

        self.store_data(item)
        return item


# -------------------------------------------------------------------
class ShoePipeline(object):
    """
    To store data of shoes in some sort of database.
    like sqlite3, mysql, mongodb etc.
    """

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):

        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='abc123',
            database='web_on_mind'
        )
        self.my_cursor = self.conn.cursor()

    def create_table(self):
        
        self.my_cursor.execute("""DROP TABLE IF EXISTS shoes_tbl""")
        self.my_cursor.execute("""CREATE TABLE shoes_tbl (
            name_of_shoe text,
            start_price text,
            end_price text,
            image_link text
        )
        """)

    def store_data(self, item):

        self.my_cursor.execute("""
        INSERT INTO shoes_tbl values (%s, %s, %s, %s)""",
        (
            item['name_of_shoe'],
            item['start_price'],
            item['end_price'],
            item['image']
        ))

        self.conn.commit()

    def process_item(self, item, spider):
        
        self.store_data(item)
        return item
