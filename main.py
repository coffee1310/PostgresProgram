import threading
import flet as ft
from utils import *



def main(page: ft.Page):
    page.title = "Программа для работы с PostgreSQL"
    page.vertical_aligment = ft.MainAxisAlignment.CENTER
    txt_field = ft.TextField(value="", text_align=ft.TextAlign.LEFT, width=400, autofocus=True)

    lv = ft.ListView(expand=True, spacing=10)
    DataBase.page = page

    txt_title = ft.Row(
        [
            ft.Text("Data Bases", text_align=ft.TextAlign.LEFT, size=20, weight=ft.FontWeight.W_900)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    def select_option(e):
        sel_index = e.control.selected_index
        if sel_index == 0:
            page.add(txt_title)
            page.add(lv)
            page.update()

        elif sel_index == 1:
            if (lv in page.controls and txt_title in page.controls):
                page.remove(lv)
                page.remove(txt_title)
                page.update()

        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.DATA_ARRAY,label="Data Bases",),
            ft.NavigationRailDestination(icon=ft.icons.SETTINGS, label="Settings")
        ],
        selected_index=0,
        on_change=select_option
    )

    def search_btn(e):
        pass


    def create_db(e):
        try:
            db_name = txt_field.value

            DataBaseControl(db_name).create_DB_control()
            page.update()
        except Exception as _ex:
            error_txt = ft.Row(
                [
                    ft.Text(_ex, size=20, color="Red", width=300, weight=ft.FontWeight.W_700, text_align=ft.TextAlign.CENTER)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )

            page.add(error_txt)
            page.update()

            stopwatch_thread = threading.Thread(target=stopwatch, args=(page, error_txt, 3))
            stopwatch_thread.start()

    def delete_db(e:ft.TapEvent):
        pass

    page.add(
        ft.Row(
            [
                txt_field,
                ft.IconButton(ft.icons.ADD, on_click=create_db),
                ft.IconButton(ft.icons.SEARCH, on_click=search_btn)
            ],
            alignment=ft.MainAxisAlignment.CENTER,

        )
    )

    lv = add_lv_on_page(lv, page=page)
    DataBase.lv = lv
    page.add(txt_title)

    page.add(lv)


ft.app(target=main, view=ft.WEB_BROWSER)