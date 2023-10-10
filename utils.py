#Python file with some functions, classes

import time
import flet as ft
import psycopg2
import configparser
import threading

from flet_core import Row

from config import *

def stopwatch(page,elem, sec):
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= sec:
            remove_element(page, elem)
            break
        time.sleep(1)
def remove_element(page:ft.page,elem):
    page.controls.remove(elem)
    page.update()

def get_data_base():
    config_ = configparser.ConfigParser()
    config_.read("db_config.ini")
    return config_.sections()

class DataBase():
    lv = None
    page = None

    def __init__(self, db_name):
        self.db_name = db_name

    def connect_to_DB(self):
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
        )
        conn.autocommit = True

        return conn

    def create_DB(self):
        conn = self.connect_to_DB()

        cursor = conn.cursor()
        cursor.execute(f"""CREATE database {self.db_name}""")

        print("Database has been created!")
        conn.close()

        self.save_DB_name()
        self.page.update()

    def remove_DB(self, e=None):
        conn = self.connect_to_DB()

        cursor = conn.cursor()
        cursor.execute(f"""DROP DATABASE IF EXISTS {self.db_name}""")

        print("Database has been deleted!")
        conn.close()

        self.remove_DB_name()

    def create_table(self,):
        pass

    def save_DB_name(self):
        config_ = configparser.ConfigParser()
        config_.read("db_config.ini")
        config_[self.db_name] = {
            "db_name" : self.db_name,
        }

        with open('db_config.ini', 'w+') as configfile:
            config_.write(configfile)
            configfile.flush()

        print("Database name has been created!")

    def remove_DB_name(self):
        config_ = configparser.ConfigParser()
        config_.read("db_config.ini")
        config_.remove_section(self.db_name)


        with open('db_config.ini', 'w+') as configfile:
            config_.write(configfile)
            configfile.flush()

        print("Database name has been deleted!")

class DataBaseControl(DataBase, ft.UserControl):
    message = None

    def __init__(self, db_name):
        ft.UserControl.__init__(self)
        self.db_name = db_name
        self.data_base_row = ft.Row(
            [
                ft.Text(self.db_name, size=20, width=300),
                ft.IconButton(ft.icons.EDIT, icon_size=20,),
                ft.IconButton(ft.icons.DELETE, icon_size=20, on_click=self.remove_DB_control)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    def remove_DB_control(self, e=None):
        conn = self.connect_to_DB()

        cursor = conn.cursor()
        cursor.execute(f"""DROP DATABASE IF EXISTS {self.db_name}""")

        print("Database has been deleted!")
        conn.close()

        self.remove_DB_name()

        if self.page:
            print(self.page.controls)
            self.check_DB()
            if self.lv:
                self.lv.controls.remove(self)
            self.page.update()
    def create_DB_control(self):
        if self.lv and  self.db_name not in get_data_base():
            self.lv.controls.insert(0, self)
            self.create_DB()
            self.page.update()
            self.check_DB()
    def check_DB(self):
        if len(self.lv.controls) == 0:
            self.message = ft.Row(
                [
                    ft.Text("You haven't created any database yet", weight=ft.FontWeight.W_700, size=20,)
                ],
                alignment=ft.MainAxisAlignment.CENTER)
            self.page.add(self.message)
        else:
            if self.message in self.page.controls:
                self.page.controls.remove(self.message)


    def build(self):
        return self.data_base_row

def add_lv_on_page(lv: ft.ListView, page:ft.Page):
    data_bases = get_data_base()
    for db_name in data_bases:
        lv_elem = DataBaseControl(db_name)
        lv.controls.append(lv_elem)
        DataBaseControl.lv = lv
    return lv


def search_db(db_name, lv:ft.ListView):
    config = configparser.ConfigParser()
    config.read("db_config.ini")
    lv.controls.clear()
    if config.has_section(db_name):
        lv.controls.append(DataBaseControl(db_name))
    else:
        pass
