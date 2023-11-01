#Python file with some functions, classes
import datetime
import time
import flet as ft
import psycopg2
import configparser
import asyncio
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
    __lv = None
    page = None

    def __init__(self, db_name:str):
        self.db_name = db_name

    def connect_to_DB(self):
        try:
            conn = psycopg2.connect(
                user=user,
                password=password,
                host=host,
            )
            conn.autocommit = True
            return conn
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    def create_DB(self):

        print("db:" + self.db_name)
        conn = self.connect_to_DB()

        cursor = conn.cursor()
        cursor.execute(f"""CREATE database {self.db_name}""")

        print("Database has been created!")
        conn.close()

        self.save_DB_setting()
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

    def save_DB_setting(self):
        config_ = configparser.ConfigParser()
        config_.read("db_config.ini")
        config_[self.db_name] = {
            "db_name" : self.db_name,
            "created_at" : datetime.datetime.now(),
            "modified_at" : datetime.datetime.now(),
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

    @property
    def lv(self):
        return self.__lv
    @lv.setter
    def lv(self, val):
        self.__lv = val


class DataBaseControl(DataBase, ft.UserControl):
    message = None
    page_stack = None

    def __init__(self, db_name):
        ft.UserControl.__init__(self)
        self.db_name = db_name

        self.data_base_row = ft.Container(
            ft.Row(
                [
                    ft.Checkbox(),
                    ft.Text(self.db_name, size=20, width=300),
                    ft.IconButton(ft.icons.EDIT, icon_size=20,),
                    ft.IconButton(ft.icons.DELETE, icon_size=20, on_click=self.remove_DB_control),

                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            scale=ft.transform.Scale(scale=1),
            opacity=1,
            animate_opacity=ft.animation.Animation(100),
            animate_scale=ft.animation.Animation(600, ft.AnimationCurve.BOUNCE_IN),
        )

        self.animate_scale = ft.animation.Animation(800)
        self.animate_opacity = ft.animation.Animation(500)

    def remove_DB_control(self, e=None):
        self.scale = ft.transform.Scale(scale=0.75)
        self.opacity = 0
        self.page.update()

        self.lv.opacity = 0
        self.page.update()
        conn = self.connect_to_DB()

        cursor = conn.cursor()
        cursor.execute(f"""DROP DATABASE IF EXISTS {self.db_name}""")

        print("Database has been deleted!")
        conn.close()

        self.lv.controls.remove(self)
        self.lv.opacity = 1
        self.page.update()
        self.remove_DB_name()
        if self.page:
            self.page.update()

    def create_DB_control(self):
        if self.db_name == "" or self.db_name.replace(" ", "") == "":
            raise ValueError

        if self.lv and self.db_name not in get_data_base():
            self.lv.controls.insert(0, self)
            self.create_DB()
            self.check_DB()
            self.page.update()

    def check_DB(self):
        if self.message in self.page_stack.controls:
            self.page_stack.controls.remove(self.message)
            self.page.update()

    def build(self):
        return self.data_base_row

def add_lv_on_page(lv: ft.ListView, page:ft.Page):
    data_bases = get_data_base()
    for db_name in data_bases:
        lv_elem = DataBaseControl(db_name)
        lv.controls.append(lv_elem)
        DataBaseControl.lv = lv
    return lv

def search_db(db_name, lv:ft.ListView, page:ft.Page):
    config = configparser.ConfigParser()
    config.read("db_config.ini")

    if config.has_section(db_name) and db_name != '':
        lv.controls.clear()
        lv.controls.append(DataBaseControl(db_name))
    elif db_name == '' and len(lv.controls) == 0:
        lv = add_lv_on_page(lv, page)
        page.update()
    elif db_name == '':
        lv.clean()
        lv = add_lv_on_page(lv, page)
        page.update()

def set_theme_setting(theme):
    config = configparser.ConfigParser()
    config.read("app_settings.ini")
    config["settings"] = {
        "theme": theme
    }

    with open("app_settings.ini", "w+") as configfile:
        config.write(configfile)
        configfile.flush()

def get_theme_setting():
    config = configparser.ConfigParser()
    config.read("app_settings.ini")
    return config["settings"]["theme"]


async def sort_data_base_A_z():
    config = configparser.ConfigParser()
    config.read("db_config.ini")
    sections = config.sections()
    sections.sort()

    DataBase.lv.opacity = 0
    DataBase.page.update()

    await asyncio.sleep(0.2)

    DataBase.lv.clean()

    for i in sections:
        DataBase.lv.controls.append(DataBaseControl(i))

    DataBase.lv.opacity = 1
    DataBase.page.update()

    return DataBase.lv

async def sort_data_base_Z_A():
    config = configparser.ConfigParser()
    config.read("db_config.ini")
    sections = config.sections()
    sections.sort()
    sections.reverse()

    DataBase.lv.opacity = 0
    DataBase.page.update()

    await asyncio.sleep(0.2)

    DataBase.lv.clean()

    for i in sections:
        DataBase.lv.controls.append(DataBaseControl(i))

    DataBase.lv.opacity = 1
    DataBase.page.update()

    return DataBase.lv

async def sort_data_base_by_date():
    config = configparser.ConfigParser()
    config.read("db_config.ini")
    sections = config.sections()
    DataBase.lv.opacity = 0
    DataBase.page.update()

    await asyncio.sleep(0.2)
    DataBase.lv.clean()
    db_hash_map = {}

    for i in sections:
        db_hash_map[i] = config[i]["created_at"]


    db_hash_map = sorted(db_hash_map.items())
    db_hash_map = dict(db_hash_map)

    controls = map(lambda db_name: DataBaseControl(db_name), db_hash_map.keys())
    DataBase.lv.controls.extend(controls)

    DataBase.lv.opacity = 1
    DataBase.page.update()

    return DataBase.lv

async def sort_data_bases_by_date_modifided():
    pass

async def sort_data_base(e):
    match(e.control.value):
        case "A-z":
            task = asyncio.create_task(sort_data_base_A_z())
            await task
        case "z-A":
            task = asyncio.create_task(sort_data_base_Z_A())
            await task
        case "Creation\ndate":
            task = asyncio.create_task(sort_data_base_by_date())
            await task
        case "Date\nmodified":
            pass