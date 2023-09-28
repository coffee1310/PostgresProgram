import psycopg2
import flet as ft
from config import *
from utils import *

def main(page: ft.Page):
    page.title = "Программа для работы с PostgreSQL"
    page.vertical_aligment = ft.MainAxisAlignment.CENTER
    txt_field = ft.TextField(value="", text_align=ft.TextAlign.CENTER, width=300)

    title_text = ft.Row(
        [
            ft.Text(
                "Создайте новую БД PostgreSQL или работайте с существующей.",
                color="green",
                weight=ft.FontWeight.W_900,
                size=20,
                text_align=ft.TextAlign.CENTER,
                width=300
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    page.add(title_text)

    def search_btn(e):
        pass

    def create_db(e):
        db_name = txt_field.value
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            database=db_name
        )

        try:
            conn.autocommit = True

            cursor = conn.cursor()

            if conn is not None:
                cursor.execute(f"""
                    CREATE database {db_name}
                """)

                print("Database has been created!")

                page.add(ft.Checkbox(label=db_name))

            else:
                text_error = ft.Text("БД с таким именем уже существует", size=20, color="red", text_align=ft.TextAlign.CENTER)
                page.add(text_error)

        except Exception as _ex:
            txt_field.value = _ex
            print(_ex)
        finally:
            conn.close()
            page.update()

    page.add(
        ft.Row(
            [
                txt_field,
                ft.ElevatedButton("Создать новую БД", on_click=create_db)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(target=main, view=ft.WEB_BROWSER)