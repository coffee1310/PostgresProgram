import threading
import flet as ft
from utils import *

def main(page: ft.Page):
    page.title = "Программа для работы с PostgreSQL"
    page.vertical_aligment = ft.MainAxisAlignment.CENTER
    txt_field = ft.TextField(value="", text_align=ft.TextAlign.LEFT, width=400, autofocus=True)


    lv = ft.ListView(expand=True, spacing=10)

    txt_title = ft.Row(
        [
            ft.Text("Data Bases", text_align=ft.TextAlign.LEFT, size=20, weight=ft.FontWeight.W_900)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # def select_option(e):
    #     sel_index = e.control.selected_index
    #     if sel_index == 0:
    #         page.add(txt_title)
    #         page.add(lv)
    #         page.update()
    #
    #     elif sel_index == 1:
    #         if (lv in page.controls and txt_title in page.controls):
    #             page.remove(lv)
    #             page.remove(txt_title)
    #             page.update()
    #
    #     page.update()

    def menu_sel_1(e):
        page.update()


    rail = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.IconButton(ft.icons.DATA_ARRAY, on_click=menu_sel_1),
                    animate=ft.animation.Animation(1000,'bounceOut')
                ),
                ft.Container(
                    content=ft.IconButton(ft.icons.SETTINGS)
                ),
                ft.Container(
                    content=ft.IconButton(ft.icons.COLOR_LENS)
                ),
                ft.Container(
                    content=ft.IconButton(ft.icons.INFO)
                ),
                ft.Container(
                    content=ft.IconButton(ft.icons.CLOSE),
                    alignment=ft.alignment.bottom_left
                )
            ]
        ),
        width=page.window_width,
        height=page.window_height,
        margin=ft.margin.only(top=20),
    )

    def search_btn(e):
        search_db(db_name=txt_field.value, lv=lv)
        page.update()


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

    lv = add_lv_on_page(lv, page=page)

    message = ft.Row(
            [
                ft.Text("You haven't created any database yet", weight=ft.FontWeight.W_700, size=20,)
            ],
            alignment=ft.MainAxisAlignment.CENTER)

    if len(lv.controls) != 0:
        message = ft.Row(
            [
            ],
            alignment=ft.MainAxisAlignment.CENTER)

    page.add(
            ft.Stack([
                rail,
                ft.Container(
                    margin=ft.margin.only(top=50, left=60),
                    content=(
                        ft.Row(
                            [
                                txt_field,
                                ft.IconButton(ft.icons.ADD, on_click=create_db),
                                ft.IconButton(ft.icons.SEARCH, on_click=search_btn)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER))
                    ),
                ft.Container(
                    margin=ft.margin.only(top=150),
                    content=lv,
                ),
                ft.Container(
                    margin=120,
                    content= txt_title
                ),
                ft.Container(
                    margin=150,
                    content=message
                )
                ]
            )
        )

    DataBase.lv = lv
    DataBaseControl.message = message
    DataBase.page = page
    DataBaseControl.page = page


ft.app(target=main, view=ft.FLET_APP)