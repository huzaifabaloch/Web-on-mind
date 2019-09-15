import mysql.connector
import time
import os
import threading
import multiprocessing
import tkinter.messagebox
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QDialog, QMessageBox
from tkinter import *


class Tracker:
    """
    It is responsible to run the web crawlers after every 1 - 2 minutes
    that will crawl web pages and extract data from them, storing relevant
    data back in local server.
    Then it will lookup the tracking table where products are stored that
    are going to be tracked after a minute.
    Now the products that are on tracked will be matched to server products,
    if any of the target price (user set price) get matched that was set during
    product traction, the user get notified.
    In case of product is missing from the server but added on track table,
    this means that the product was deleted by seller on the specific website
    and user will be notified that product was deleted from website.
    """

    def __init_(self):
        super().__init__()

    def create_connection(self):
        """Creating connection locally."""

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='abc123',
            database='web_on_mind'
        )

        return conn

    def run_crawlers(self):
        """To run the web crawlers."""

        print(os.getcwd())
        os.chdir('C:\\Users\sunny ahmed\Desktop\Web on mind\WebSpider')
        print(os.getcwd())
        os.system('scrapy crawl ps4bot && scrapy crawl shoebot')

    def gather_data_from_local_server(self):
        """
        Gather all the data from local server that was scraped by crawlers
        and added to local server.
        """

        items = {}  # To store name of product as key and price as value.
        conn = self.create_connection()
        my_cursor = conn.cursor()

        query = 'SELECT name_of_game, price FROM ps4_tbl'
        my_cursor.execute(query)
        result = my_cursor.fetchall()
        for each in result:
            items[each[0]] = each[1]

        my_cursor.close()
        conn.close()

        return items

    def gather_tracking_data(self):
        """Gather all the data that are added on tracking list by users."""

        title = ''
        items_on_track = {}
        conn = self.create_connection()
        my_cursor = conn.cursor()

        query = 'SELECT title, actual_price, user_price FROM track_tbl'
        my_cursor.execute(query)
        result = my_cursor.fetchall()
        for product in result:
            items = []
            for key, each in enumerate(product):
                if key == 0:
                    title = each
                else:
                    items.append(each)
                    items_on_track.update({title: items})

        return items_on_track

    def check_price(self):
        """Check the price if it got lowered."""

        while True:
            user_tracked_items = self.gather_tracking_data()
            server_items = self.gather_data_from_local_server()
            time.sleep(2)
            """
            Selecting each product one by one from tracked list and finding it in the server list,
            if get matched then we start checking the price.
            """

            for each_tracked_item in user_tracked_items.items():
                item_found = False
                print(each_tracked_item)
                for each_item in server_items.items():
                    if each_tracked_item[0] == each_item[0]:
                        if int(each_item[1]) < int(each_tracked_item[1][0]):
                            if int(each_item[1]) <= int(each_tracked_item[1][1]):
                                print('YES')
                                # self.send_email()
                                item_found = True
                                break
                        else:
                            item_found = True
                            break

                if item_found is False:
                    self.product_deleted_prompt(each_tracked_item[0])


    def product_deleted_prompt(self, product_name):
        """
        The prompt when any product is removed from website by seller or web owner.
        """

        self.dialog = Tk()
        self.dialog.title('Product removed')
        self.dialog.configure(background='#FFFFFF')
        self.dialog.geometry('900x180+190+200')
        top_frame = Frame(self.dialog)
        bot_frame = Frame(self.dialog)
        top_frame.configure(background='white')
        deletion_label = Label(top_frame, font=('Arial', 14), text='The following product:\n"{}"\nhas been removed from the server\n\nDo you want to completely remove it from the tracking list.'.format(product_name), bg='white')
        yes_btn = Button(bot_frame, text='Yes', font=('Arial', 12), padx=80, pady=8, bg='#46a6b3', fg='#FFFFFF', command=lambda: self.remove_product_from_tracking(product_name))
        no_btn = Button(bot_frame, text='No', font=('Arial', 12), padx=80, pady=8, bg='#46a6b3', fg='#FFFFFF', command=self.dialog.destroy)
        top_frame.pack()
        bot_frame.pack(side=BOTTOM)
        deletion_label.grid(row=0, column=0)
        yes_btn.grid(row=1, column=0)
        no_btn.grid(row=1, column=1)
        self.dialog.mainloop()
        print('PRODUCT REMOVE')
        time.sleep(2)

    def remove_product_from_tracking(self, product_name):
        """Permanently remove the product from the tracking list."""

        conn = self.create_connection()
        my_cursor = conn.cursor()
        my_cursor.execute('SELECT title FROM track_tbl WHERE title = %s', (product_name,))
        result = my_cursor.fetchone()
        if result is not None:
            my_cursor.execute('DELETE FROM track_tbl WHERE title = %s', (product_name,))
            tkinter.messagebox.showinfo('Product Removed Success', 'Product is removed from tracking list successfully')
            self.dialog.destroy()

        conn.commit()
        conn.close()

    def send_email(self):
        pass
