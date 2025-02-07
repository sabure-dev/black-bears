from datetime import date, datetime

import flet as ft
import requests

poly_logo = ft.Image(src=f"/logo.png", fit=ft.ImageFit.CONTAIN, width=75, height=75)
poly_text = ft.Text("Черные Медведи", font_family="Montserrat", color='#FFFFFF', size=14, weight=ft.FontWeight.W_400)
news_text = ft.Text("Новости", font_family="Montserrat", color='#FFFFFF', size=14, weight=ft.FontWeight.W_400)
matches = ft.Text("Матчи", font_family="Montserrat", color='#FFFFFF', size=14, weight=ft.FontWeight.W_400)
men = ft.Text("Мужская команда", font_family="Montserrat", color='#FFFFFF', size=14, weight=ft.FontWeight.W_400)
women = ft.Text("Женская команда", font_family="Montserrat", color='#FFFFFF', size=14, weight=ft.FontWeight.W_400)
address = ft.Row([ft.Icon(name=ft.Icons.LOCATION_PIN, color="#2E363E"),
                  ft.Text("г. Санкт-Петербург, ул. Политехническая, д. 27 (Спортивный комплекс «Политехник»)",
                          font_family="Montserrat", color='#FFFFFF', size=12, weight=ft.FontWeight.W_300,
                          style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE))])
email = ft.Row([ft.Icon(name=ft.Icons.EMAIL, color="#2E363E"),
                ft.Text("sskblackbears@spbstu.ru", font_family="Montserrat", color='#FFFFFF', size=12,
                        weight=ft.FontWeight.W_300)])
title = ft.Row([email, address], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

footer = ft.BottomAppBar(
    bgcolor="#131211",
    height=60,
    content=ft.Row(
        controls=[
            ft.Image(src='/polytech.png'),
            ft.Image(src='/asb.png'),
            ft.Row([
                ft.Text("Мы в соцсетях: ", font_family="Montserrat", weight=ft.FontWeight.W_300,
                        size=14, color='#776E67'),
                ft.CupertinoButton(content=ft.Image(src='/vk.png'), padding=5, url='https://vk.com/blackbears_mbasket'),
                ft.CupertinoButton(content=ft.Image(src='/youtube.png'), padding=5,
                                   url='https://www.youtube.com/@blackbears-polytech3931'),
                ft.CupertinoButton(content=ft.Image(src='/tg.png'), padding=5, url='https://t.me/bearsbasketball'), ],
                alignment=ft.MainAxisAlignment.END)
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY),
)


def video_container(path):
    video = ft.Video(
        autoplay=False,
        muted=False,
        playlist=[
            ft.VideoMedia(
                path
            )
        ],
        aspect_ratio=16 / 9,
        filter_quality=ft.FilterQuality.HIGH,
        volume=1.0,
    )

    video_con = ft.Container(
        content=video,
        padding=20,
        alignment=ft.alignment.bottom_left,
        width=800,
        height=450,
        border_radius=10
    )
    return video_con


video_container1 = video_container('/1.mp4')
video_container2 = video_container('/2.mp4')
# Основные элементы страницы
txt_number = ft.Text(
    "БК «Черные Медведи - Политех»",
    font_family="Montserrat",
    weight=ft.FontWeight.W_700,
    size=52,
    color='#FFFFFF'
)
text = "Наша команда является: \n" \
       " – двукратным чемпионом чемпионата АСБ, \n" \
       " – двукратным призером чемпионата АСБ, \n" \
       " – чемпионом Студенческой суперлиги, \n" \
       " – бронзовым призером Студенческой лиги РЖД, \n" \
       " – трехкратным чемпионом дивизиона «Санкт-Петербург», \n" \
       " – двукратным призером дивизиона «Санкт-Петербург». "
about = ft.Container(
    content=ft.Text(
        text,
        font_family="Montserrat",
        weight=ft.FontWeight.W_700,
        size=22,
        color='#FFFFFF'
    ),
    padding=20
)
team_img = ft.Container(
    content=ft.Row(
        [ft.Container(content=ft.Image(src='team.png', border_radius=10, width=1000), padding=0, margin=0)],
        alignment=ft.MainAxisAlignment.END
    ),
    padding=20
)


def header(page):
    head = ft.AppBar(
        elevation_on_scroll=0,
        toolbar_height=95,
        leading_width=850,
        bgcolor="#131211",
        leading=ft.Row(
            [ft.CupertinoButton(
                content=ft.Container(content=ft.Image(src=f"/logo.png", fit=ft.ImageFit.CONTAIN, width=75, height=75),
                                     margin=20),
                on_click=lambda x: page.go('/main'), padding=0),
                ft.CupertinoButton(content=men, bgcolor='#095644', width=161, height=42, padding=2,
                                   on_click=lambda x: page.go('/playersm')),
                ft.CupertinoButton(content=women, bgcolor='#095644', width=161, height=42, padding=2,
                                   on_click=lambda x: page.go('/playersf')),
                ft.CupertinoButton(content=news_text, bgcolor='#095644', width=161, height=42, padding=2,
                                   on_click=lambda x: page.go('/news')),
                ft.CupertinoButton(content=matches, bgcolor='#095644', width=161, height=42, padding=2,
                                   on_click=lambda x: page.go('/matches'))],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY),

        center_title=False,
        title=title,
        actions=[
        ],
    )
    return head


def fetch_news(selected_tags=None):
    try:
        # Базовые параметры запроса
        params = [("skip", 0), ("limit", 100)]

        # Добавляем теги, если они выбраны
        if selected_tags:
            for tag in selected_tags:
                params.append(("tags", tag))

        # Отправляем запрос с параметрами
        response = requests.get("https://black-bears-service.onrender.com/api/v1/news", params=params)
        response.raise_for_status()
        news_data = response.json()
        return prepare_news(news_data)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе новостей: {e}")
        return []


def prepare_news(news_data):
    prepared_news = []
    for news in news_data:
        # Укорачиваем текст для краткого содержания
        short_content = news["content"][:100] + "..." if len(news["content"]) > 100 else news["content"]
        prepared_news.append({
            "title": news["title"],
            "date": datetime.fromisoformat(news["created_at"]),  # Преобразуем строку в datetime
            "content": short_content,  # Краткий текст
            "full_content": news["content"],  # Полный текст
            "image": news["image_url"],  # URL изображения
        })
    return prepared_news


def news_card(page, news):
    show_full_content = False

    # Текстовый элемент для отображения контента
    content_text = ft.Text(
        news["content"],  # По умолчанию показываем краткий текст
        color="#FFFFFF",
        font_family='Montserrat',
        size=14,
    )

    # Кнопка для переключения текста
    button = ft.ElevatedButton(
        "Читать полностью",
        color="#FFFFFF",
        bgcolor="#095644",
        style=ft.ButtonStyle(padding=10, text_style=ft.TextStyle(font_family='Montserrat')),
    )

    # Функция для переключения текста
    def toggle_content(e):
        nonlocal show_full_content
        show_full_content = not show_full_content

        # Обновляем текст
        content_text.value = (
            news["full_content"] if show_full_content else news["content"]
        )

        # Обновляем текст кнопки
        button.text = "Свернуть" if show_full_content else "Читать полностью"

        # Обновляем страницу
        page.update()

    # Привязываем обработчик к кнопке
    button.on_click = toggle_content

    # Возвращаем карточку с фиксированной шириной
    return ft.Container(
        content=ft.Card(
            color="#2E363E",
            elevation=5,
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    [
                        ft.Image(src=news['image'], width=800, height=600, fit=ft.ImageFit.COVER, border_radius=10),
                        ft.Text(news['title'], color="#FFFFFF", size=20, weight=ft.FontWeight.W_600,
                                font_family='Montserrat'),
                        ft.Text(news['date'].strftime("%d.%m.%Y"), color="#FFFFFF", size=12, font_family='Montserrat'),
                        content_text,  # Отображаем текст
                        button,  # Отображаем кнопку
                    ],
                    spacing=10,
                ),
            ),
        ),
        width=800,  # Ограничиваем ширину карточки
        alignment=ft.alignment.center,  # Центрируем карточку
    )


# Класс для сообщений
class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


# Класс для отображения сообщений в чате
class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name), font_family='Montserrat'),
                color=ft.Colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE,
                            font_family='Montserrat'),
                    ft.Text(message.text, selectable=True, color=ft.colors.WHITE, font_family='Montserrat'),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    def get_initials(self, user_name: str):
        if user_name:
            return user_name[:1].capitalize()
        else:
            return "Unknown"

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


def fetch_tags():
    try:
        response = requests.get("https://black-bears-service.onrender.com/api/v1/news/tags/")
        response.raise_for_status()
        res = response.json()
        return res
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе тегов: {e}")
        return []


def match_container(gender, team_name, date, location, scorep, score2):
    if gender == 'male': gender_text = ft.Text("Мужчины", font_family="Montserrat", color='#FFFFFF', size=14,
                                               weight=ft.FontWeight.W_400)
    elif gender == 'female': gender_text = ft.Text("Женщины", font_family="Montserrat", color='#FFFFFF', size=14,
                                               weight=ft.FontWeight.W_400)
    date_text = ft.Text(date, font_family="Montserrat", color='#FFFFFF', size=14,
                        weight=ft.FontWeight.W_400)
    location_text = ft.Text(location, font_family="Montserrat", color='#FFFFFF', size=14,
                        weight=ft.FontWeight.W_400)
    poly_logo = ft.Image(src=f"/logo.png", fit=ft.ImageFit.CONTAIN, width=65, height=65)
    poly_text = ft.Text("Черные Медведи", font_family="Montserrat", color='#FFFFFF', size=14,
                        weight=ft.FontWeight.W_400)
    poly_color = '#00B43E'
    op_color = '#00B43E'
    if scorep > score2:
        op_color = '#DE3225'
    elif scorep < score2:
        poly_color = '#DE3225'
    poly_score = ft.Text(scorep, font_family="Montserrat", color=poly_color, size=32, weight=ft.FontWeight.W_600)
    op_logo = ft.Image(src=f"/{team_name}.png", fit=ft.ImageFit.CONTAIN, width=65, height=65)
    op_text = ft.Text(team_name, font_family="Montserrat", color='#FFFFFF', size=14,
                      weight=ft.FontWeight.W_400)
    op_score = ft.Text(score2, font_family="Montserrat", color=op_color, size=32, weight=ft.FontWeight.W_600)
    cont = ft.Column([ft.Row([ft.Container(ft.Row(
        [ft.Column([poly_logo, poly_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=250), poly_score, op_score,
         ft.Column([op_logo, op_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=250)],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY), width=960,
        bgcolor='#2E363E', border_radius=10)], alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER)])
    return cont


def get_matches():
    try:
        response = requests.get('https://black-bears-service.onrender.com/api/v1/games/?skip=0&limit=100')
        response.raise_for_status()
        res = response.json()
        return res
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении матчей: {e}")
        return []


matchesjson = get_matches()
matchesc = []
for i in matchesjson:
    matchesc.append(match_container(i['gender'], i['team_name'], i['date_time'], i['location'], i['score_black_bears'],
                                    i['score_opponent']))

matches_col = ft.Column(matchesc)
