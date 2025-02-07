import json
from datetime import date, datetime

import flet as ft
import requests
from elements import footer, header


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


# Функция для экрана с подробной информацией о игроке
def player_detail_screen(page, name, image_src, stats, biography):
    def go_back(e):
        page.views.pop()  # Удаляем последний экран (возвращаемся)
        page.update()

    page.views.append(
        ft.View(
            route=f"/player/{name}",
            controls=[
                ft.AppBar(leading=ft.IconButton(icon=ft.Icons.ARROW_BACK_ROUNDED, on_click=go_back, padding=10),
                          title=ft.Text(name, font_family="Montserrat", color="#FFFFFF"), bgcolor="#131211"),
                ft.Container(
                    content=ft.Row(
                        [
                            # Левая часть — фото игрока
                            ft.Column(
                                [
                                    ft.Image(src=image_src, width=250, height=300, fit=ft.ImageFit.COVER),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            # Правая часть — краткая информация и биография
                            ft.Column(
                                [
                                    # Краткая информация
                                    ft.Text(f"Рост: {stats.get('рост', 'N/A')}", size=16, color="#FFFFFF",
                                            font_family="Montserrat"),
                                    ft.Text(f"Вес: {stats.get('вес', 'N/A')}", size=16, color="#FFFFFF",
                                            font_family="Montserrat"),
                                    ft.Text(f"Позиция: {stats.get('позиция', 'N/A')}", size=16, color="#FFFFFF",
                                            font_family="Montserrat"),
                                    ft.Text(f"Дата рождения: {stats.get('год_рождения', 'N/A')}", size=16,
                                            color="#FFFFFF", font_family="Montserrat"),
                                    # Биография
                                    ft.Text(f"Биография: {biography}", size=16, color="#FFFFFF",
                                            font_family="Montserrat"),
                                    # Кнопка назад
                                    ft.ElevatedButton("Назад", on_click=go_back, bgcolor="#095644", color="#FFFFFF"),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                spacing=10,
                                expand=True
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=20,
                        run_spacing=20,
                    ),
                    padding=20,
                    bgcolor="#1C1B19",
                    alignment=ft.alignment.top_left
                ),
            ],
            bgcolor="#1C1B19"
        )
    )
    page.update()


# Функция для карточки игрока
def player_card(image_src, name, description, stats, biography, page):
    def on_card_tap(e):
        player_detail_screen(page, name, image_src, stats, biography)

    return ft.Container(
        content=ft.Column(
            [
                ft.Image(src=image_src, width=150, height=200, fit=ft.ImageFit.COVER),
                ft.Text(name, font_family="Montserrat", weight=ft.FontWeight.BOLD, size=18, color="#FFFFFF"),
                ft.Text(description, font_family="Montserrat", size=14, color="#CCCCCC")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
        ),
        width=180,
        height=320,
        padding=15,
        bgcolor="#2A2926",
        border_radius=10,
        alignment=ft.alignment.center,
        on_click=on_card_tap  # Нажатие на карточку
    )


def players(page, gender):
    page.scroll = ft.ScrollMode.ALWAYS
    pl = []
    playersjson = requests.request(method='GET',
                                   url='https://black-bears-service.onrender.com/api/v1/players/?skip=0&limit=100&sort_by'
                                       '=name').json()

    for i in playersjson:
        borndate = datetime.strptime(i['birth_date'], '%Y-%m-%d').date()
        age = calculate_age(borndate)
        if i['gender'] == gender:
            pl.append(
                player_card(
                    f"/{gender} team png/{i['last_name']} {i['first_name']}-Photoroom.png",
                    f"{i['last_name']} {i['first_name']}",
                    f"{i['position']}, {age}",
                    {"рост": i['height'], "вес": i['weight'], "позиция": i['position'],
                     "год_рождения": i['birth_date'].split('-')[0]},
                    i['biography'],
                    page
                )
            )
    player_row = ft.Column([ft.Row(
        pl,
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True,
        spacing=22)], expand=True, width=1920,
        scroll=ft.ScrollMode.AUTO
    )
    return player_row
