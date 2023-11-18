import os
from utils import *
from views import *
import signal

def main(page: ft.Page):

    page_theme = get_theme_setting()
    page.title = "Программа для работы с PostgreSQL"
    page.vertical_aligment = ft.MainAxisAlignment.CENTER
    page.theme_mode = page_theme
    page.fonts = {
        "Kadwa-Regular": "fonts/Kadwa-Regular.ttf",
        "Kadwa-Bold": "Kadwa-Bold.ttf",
    }
    page.route = "/"
    page.update()

    page.theme = ft.Theme(font_family="Kadwa-Regular")

    troute = ft.TemplateRoute(page.route)

    def route_changer(route):
        page.views.clear()
        if page.route == '/settings':
            page.views.append(settings_view())
        elif page.route == '/':
            page.views.append(index_view())
        elif page.route == '/edit':
            page.views.append('/edit')
        page.update()


    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_changer
    page.on_view_pop = view_pop

    txt_field = ft.TextField(value="", text_align=ft.TextAlign.LEFT, width=400, autofocus=True, label="Search and create DataBase")
    lv = ft.ListView(expand=True, spacing=10, animate_opacity=ft.animation.Animation(200))

    txt_title = ft.Row(
            [
                ft.Container(
                    ft.Text(
                        "Data Bases",
                        text_align=ft.TextAlign.CENTER,
                        size=20,
                        weight=ft.FontWeight.W_900
                    ),
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    black_theme_text = ft.Text("Black Theme")
    white_theme_text = ft.Text("White Theme")

    if page_theme == "dark":
        black_theme_text.weight = ft.FontWeight.W_700
    else:
        white_theme_text.weight = ft.FontWeight.W_700

    def change_white_theme(e):
        page.theme_mode = "white"
        white_theme_text.weight = ft.FontWeight.W_700
        black_theme_text.weight = None
        page.update()
        set_theme_setting("white")

    def change_black_theme(e):
        page.theme_mode = "dark"
        black_theme_text.weight = ft.FontWeight.W_700
        white_theme_text.weight = None
        page.update()
        set_theme_setting("dark")

    colors_lv = ft.ListView(expand=True, spacing=10, width=100)
    colors_lv.controls.append(
        ft.Container(
            ft.Container(
                content=black_theme_text,
                on_hover=None,
                height=30,
                border_radius=10,
                on_click=change_black_theme,
            ),
        )
    )

    colors_lv.controls.append(
        ft.Container(
            content=white_theme_text,
            width=100,
            height=30,
            border_radius=10,
            bgcolor="gray",
            on_click=change_white_theme
        )
    )

    colors_lv = ft.Container(
        content=colors_lv,
        margin=ft.margin.only(50, 110),
        offset=ft.Offset(-0.25, 0),
        opacity=0,
        width=0,
        animate_size=ft.animation.Animation(100),
        animate_offset=ft.animation.Animation(200),
        animate_opacity=ft.animation.Animation(200)
    )

    display_color_change_bool = False
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

    def display_color_scheme(e):
        nonlocal display_color_change_bool
        if display_color_change_bool:
            colors_lv.offset = ft.transform.Offset(-0.25, 0)
            colors_lv.opacity = 0
            colors_lv.width = 100
            display_color_change_bool = False
        else:
            colors_lv.offset = ft.transform.Offset(0, 0)
            colors_lv.opacity = 1
            colors_lv.width = 100
            display_color_change_bool = True
        page.update()

    rail = ft.Column(
        controls=[
            ft.Container(content=ft.IconButton(ft.icons.DATA_ARRAY)),
            ft.Container(content=ft.IconButton(ft.icons.SETTINGS, on_click=lambda e: e.page.go("/settings"))),
            ft.Container(content=ft.IconButton(ft.icons.COLOR_LENS, on_click=display_color_scheme)),
            ft.Container(content=ft.IconButton(ft.icons.INFO)),
            ft.Container(content=ft.IconButton(ft.icons.CLOSE, on_click=lambda e: e.page.window_destroy(), icon_color="red"))
        ]
    )

    def search_btn(e):
        search_db(db_name=txt_field.value, lv=lv, page=page)
        page.update()

    def create_db(e):
        try:
            db_name = txt_field.value
            DataBaseControl(str(db_name)).create_DB_control()
            page.update()
        except Exception as _ex:
            print(_ex)

    lv = add_lv_on_page(lv, page=page)
    message = ft.Container(
        content=ft.Row([
            ft.Text("You haven't created any database yet", weight=ft.FontWeight.W_700, size=20)
        ],
        alignment=ft.MainAxisAlignment.CENTER),
        margin=200
    )

    if len(lv.controls) != 0:
        message = ft.Container()

    sorting_drop_down = ft.Dropdown(
        width=100,
        options=[
            ft.dropdown.Option("A-z"),
            ft.dropdown.Option("z-A"),
            ft.dropdown.Option("Creation\ndate"),
            ft.dropdown.Option("Date\nmodified")
        ],
        text_size=15,
        on_change=lambda e: asyncio.run(sort_data_base(e))
    )

    page_stack = ft.Stack([
        ft.Container(
            margin=ft.margin.only(top=50),
            content=ft.Row(
                [
                    sorting_drop_down,
                    txt_field,
                    ft.IconButton(ft.icons.ADD, on_click=create_db),
                    ft.IconButton(ft.icons.SEARCH, on_click=search_btn)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ),
        ft.Container(
            margin=ft.margin.only(top=150),
            content=lv
        ),
        ft.Container(
            margin=ft.margin.only(top=120),
            content=txt_title
        ),
        message,
        colors_lv,
        rail,
    ])

    page.add(page_stack)

    DataBase.lv = lv
    DataBaseControl.message = message
    DataBaseControl.page_stack = page_stack
    DataBase.page = page



ft.app(target=main, view=ft.FLET_APP)