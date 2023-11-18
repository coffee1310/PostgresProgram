from utils import *

display_color_change_bool = False

page_theme = get_theme_setting()

black_theme_text = ft.Text("Black Theme")
white_theme_text = ft.Text("White Theme")

def change_white_theme(e):
    e.page.theme_mode = "white"
    white_theme_text.weight = ft.FontWeight.W_700
    black_theme_text.weight = None
    e.page.update()
    set_theme_setting("white")
def change_black_theme(e):
    e.page.theme_mode = "dark"
    black_theme_text.weight = ft.FontWeight.W_700
    white_theme_text.weight = None
    e.page.update()
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

def display_color_scheme(e):
    global display_color_change_bool
    print(colors_lv.opacity)
    if display_color_change_bool:
        colors_lv.offset = ft.transform.Offset(-0.25, 0)
        colors_lv.opacity = 0
        colors_lv.width = 100
        display_color_change_bool = False
        print(1)
    else:
        colors_lv.offset = ft.transform.Offset(0, 0)
        colors_lv.opacity = 1
        colors_lv.width = 100
        display_color_change_bool = True
        print(2)
    e.page.update()

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

nav_menu = ft.Column(
    controls=[
        ft.Container(content=ft.IconButton(ft.icons.DATA_ARRAY, on_click=lambda e: e.page.go("/"))),
        ft.Container(content=ft.IconButton(ft.icons.SETTINGS, on_click=lambda e: e.page.go("/settings"))),
        ft.Container(content=ft.IconButton(ft.icons.COLOR_LENS, on_click=display_color_scheme)),
        ft.Container(content=ft.IconButton(ft.icons.INFO)),
        ft.Container(content=ft.IconButton(ft.icons.CLOSE, on_click=lambda e: e.page.window_destroy(), icon_color="red"),
                     alignment=ft.alignment.bottom_left)
    ]
)

if page_theme == "dark":
    black_theme_text.weight = ft.FontWeight.W_700
else:
    white_theme_text.weight = ft.FontWeight.W_700


def index_view():
    txt_field = ft.TextField(value="", text_align=ft.TextAlign.LEFT, width=400, autofocus=True,
                             label="Search and create DataBase")
    lv = DataBaseControl.lv

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

    return ft.View(
        "/",
        controls=[
            ft.Stack([
                ft.Container(
                    margin=ft.margin.only(top=50),
                    content=ft.Row(
                        [
                            sorting_drop_down,
                            txt_field,
                            ft.IconButton(ft.icons.ADD, on_click=lambda e: DataBaseControl(txt_field.value).create_DB_control()),
                            ft.IconButton(ft.icons.SEARCH, on_click=lambda e:search_db(db_name=txt_field.value, lv=lv, page=e.page))
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ),
                ft.Container(margin=ft.margin.only(top=120), content=txt_title),
                ft.Container(margin=ft.margin.only(top=150), content=lv),
                colors_lv,
                nav_menu,
            ]
            )
        ]
    )

def settings_view():
    txt_settings = ft.Container(
        ft.Row([ft.Text("Settings", size=30)],
               alignment=ft.MainAxisAlignment.CENTER,
               ),
        margin=ft.margin.only(top=80),
    )
    user_input = ft.Container(
        ft.Row([ft.TextField(
            label="Username",
            text_align=ft.TextAlign.LEFT,
            width=400)],
            alignment=ft.MainAxisAlignment.CENTER),
        margin=ft.margin.only(top=150)
    )
    password_input = ft.Container(
        ft.Row([ft.TextField(
            label="Password",
            text_align=ft.TextAlign.LEFT,
            width=400)],
            alignment=ft.MainAxisAlignment.CENTER),
        margin=ft.margin.only(top=220)
    )

    def get_fields(e):
        set_settings(e, user_input.content.controls[0].value, password_input.content.controls[0].value)

    save_settings = ft.Container(
        ft.FilledButton(text="Save", width=200, on_click=get_fields),
        margin=ft.margin.only(top=300, left=-200),
        alignment=ft.alignment.center,
    )
    return ft.View(
        "/settings",
        controls=[
            ft.Stack([
                txt_settings,
                user_input,
                password_input,
                save_settings,
                nav_menu,
                colors_lv,
            ])
        ]
    )

def edit_data_base_view(db_name):

    return ft.View(
        "/edit/:db_name"
    )