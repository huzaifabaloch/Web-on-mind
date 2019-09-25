import mysql.connector
import time
import os
import tkinter.messagebox
from tkinter import *
from PIL import ImageTk, Image
import smtplib
import Design_and_Work.config as credential


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
        os.system('scrapy crawl ps4bot && scrapy crawl phonebot')

    def gather_data_from_local_server(self):
        """
        Gather all the data from local server that was scraped by crawlers
        and added to local server.
        """

        items = {}  # To store name of product as key and price as value.
        conn = self.create_connection()
        my_cursor = conn.cursor()

        query1 = 'SELECT name_of_game, price FROM ps4_tbl'
        query2 = 'SELECT name_of_phone, price FROM phone_tbl'
        my_cursor.execute(query1)
        ps4 = my_cursor.fetchall()
        my_cursor.execute(query2)
        phone = my_cursor.fetchall()

        for each in range(0, 2):
            if each == 0:
                for each_ps4 in ps4:
                    items[each_ps4[0]] = each_ps4[1]
            else:
                for each_phone in phone:
                    items[each_phone[0]] = each_phone[1]

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
            self.run_crawlers()
            user_tracked_items = self.gather_tracking_data()
            server_items = self.gather_data_from_local_server()
            time.sleep(5)
            """
            Selecting each product one by one from tracked list and finding it in the server list,
            if get matched then we start checking the price.
            """

            for each_tracked_item in user_tracked_items.items():
                item_found = False
                print(each_tracked_item)
                for each_item in server_items.items():
                    if each_tracked_item[0] == each_item[0]:
                        if int(float(each_item[1])) < int(float(each_tracked_item[1][0])):
                            if int(float(each_item[1])) <= int(float(each_tracked_item[1][1])):
                                print('YES')
                                self.send_email(each_tracked_item[0], each_item[1])
                                self.track_list_to_finished_list(each_tracked_item[0], each_tracked_item[1][0], each_tracked_item[1][1])
                                self.delete_from_track_list(each_tracked_item[0])
                                item_found = True
                                time.sleep(5)
                                break
                        else:
                            item_found = True
                            break

                if item_found is False:
                    self.product_deleted_prompt(each_tracked_item[0])
            time.sleep(60)

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

    def send_email(self, product_name, product_price):

        standard_message = """The following product '{}' with the target price '{}' has been dropped.
        Go and check it.""".format(product_name, product_price)
        msg = 'Subject: {}\n\n{}'.format('Price Dropped - Web on Mind', standard_message)
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(credential.EMAIL_ADDRESS, credential.PASSWORD)
            server.sendmail(credential.EMAIL_ADDRESS, credential.EMAIL_ADDRESS, msg)
            server.quit()
        except Exception as e:
            self.build_dialog('An internet connection dropped while sending email.' + str(e))
            return

    def delete_from_track_list(self, product_name):
        """If product got tracked, then move the product details to finished tracking list."""

        conn = self.create_connection()
        cur = conn.cursor()
        try:
            query = 'DELETE FROM track_tbl WHERE title = %s'
            cur.execute(query, (product_name, ))
            conn.commit()
            print('DELETING')
        except:
            pass
        finally:
            cur.close()
            conn.close()

    def track_list_to_finished_list(self, product_name, actual_price, user_price):
        """To move product from track list to finished tracking list."""

        conn = self.create_connection()
        cur = conn.cursor()
        try:
            cur.execute('SELECT id FROM finished_tracking_tbl ORDER BY id DESC LIMIT 1')
            record_no = cur.fetchone()
            if record_no is None:
                record_no = 1
            else:
                record_no = record_no[0] + 1

            print(record_no)
            print(record_no, product_name, actual_price, user_price)
            query = 'INSERT INTO finished_tracking_tbl VALUES (%s, %s, %s, %s)'
            cur.execute(query, (record_no, product_name, actual_price, user_price,))
            conn.commit()
            print('Added')
        except Exception as e:
            print(str(e))
        finally:
            cur.close()
            conn.close()

    def build_dialog(self, msg):

        dialog = Tk()
        dialog.title('error')
        dialog.geometry('400x50+500+200')
        dialog.resizable(False, False)
        var = StringVar()
        var.set(msg)
        message = Label(dialog, textvariable=var)

        #image = Image.open('resources\error.ico')
        #image = image.resize((25, 25), Image.ANTIALIAS) ## The (250, 250) is (height, width)
        #pic = ImageTk.PhotoImage(image)
        #lbl = Label(dialog, image=pic)

        #lbl.pack(side=TOP)
        message.pack(side=TOP)
        dialog.mainloop()





