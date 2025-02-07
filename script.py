import flet as ft
from cards_with_stats import players
from elements import footer, header, video_container1, team_img, about, txt_number, video_container2, fetch_tags, \
    ChatMessage, Message, news_card, prepare_news, fetch_news, matches_col


def main(page: ft.Page):
    page.fonts = {
        "Montserrat": '/Montserrat.ttf'
    }
    page.scroll = ft.ScrollMode.AUTO
    page.route = '/main'
    player_row = players(page, 'male')
    player_rowf = players(page, 'female')

    page.padding = 0
    page.spacing = 0
    page.title = "Черные Медведи"
    news_feed = ft.Column(
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    tags = fetch_tags()
    selected_tags = []

    # Чекбоксы для выбора тегов
    tag_checkboxes = ft.Column(
        scroll=ft.ScrollMode.AUTO
    )

    # Функция для обновления тегов
    def update_tags():
        nonlocal tags
        tags = fetch_tags()  # Загружаем теги с сервера
        tag_checkboxes.controls = [
            ft.Checkbox(
                label=tag['name'],
                value=tag['name'] in selected_tags,  # Сохраняем состояние выбранных тегов
                label_style=ft.TextStyle(font_family='Montserrat'),
                on_change=lambda e, tag=tag: update_selected_tags(e, tag)
            ) for tag in tags
        ]
        page.update()

    # Функция для обновления выбранных тегов
    def update_selected_tags(e, tag):
        if e.control.value:
            selected_tags.append(tag['name'])
        else:
            selected_tags.remove(tag['name'])
        update_news()

    # Обновление новостей с учетом выбранных тегов
    def update_news(e=None):
        news_feed.controls.clear()
        news_feed.controls.extend([news_card(page, news) for news in fetch_news(selected_tags)])

        page.update()

    # Функция для обновления новостей и тегов
    def refresh_data(e=None):
        update_tags()  # Обновляем теги
        update_news()  # Обновляем новости

    # Кнопка для обновления новостей
    refresh_button = ft.IconButton(
        icon=ft.icons.REFRESH,
        tooltip="Обновить новости",
        on_click=refresh_data,  # Привязываем функцию обновления
        icon_color="#FFFFFF",
        bgcolor="#095644",
    )

    # Заголовок новостной ленты с кнопкой обновления
    news_header = ft.Row(
        controls=[
            ft.Text("Новости", size=24, color="#FFFFFF", weight=ft.FontWeight.W_600, font_family='Montserrat'),
            refresh_button,  # Добавляем кнопку обновления
            tag_checkboxes,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Размещаем текст и кнопку по краям
    )

    # Контейнер для новостной ленты
    news_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Новости", size=24, color="#FFFFFF", weight=ft.FontWeight.W_600,
                                    font_family='Montserrat'),
                            refresh_button,  # Добавляем кнопку обновления
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Размещаем текст и кнопку по краям
                    ),
                    padding=ft.padding.only(bottom=20),  # Отступ снизу
                ),
                ft.Container(
                    content=tag_checkboxes,
                    padding=ft.padding.only(bottom=20),  # Отступ снизу
                ),
                news_feed,  # Новостная лента
            ],
            scroll=ft.ScrollMode.AUTO,  # Добавляем скроллинг для всей ленты
            expand=True,
        ),
        padding=ft.padding.symmetric(horizontal=30, vertical=20),
        alignment=ft.alignment.center,  # Центрируем содержимое контейнера
        width=800,  # Ограничиваем ширину контейнера
    )

    # Обновляем новости при загрузке страницы
    refresh_data()

    # Чат
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # Поле для ввода нового сообщения
    new_message = ft.TextField(
        hint_text="Введите сообщение...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=lambda e: send_message_click(e),
        color=ft.colors.WHITE,
        bgcolor="#1C1B19",
        border_color=ft.colors.WHITE,
    )

    # Функция для отправки сообщения
    def send_message_click(e):
        if new_message.value != "":
            page.pubsub.send_all(
                Message(
                    page.session.get("user_name"),
                    new_message.value,
                    message_type="chat_message",
                )
            )
            new_message.value = ""
            new_message.focus()
            page.update()

    # Функция для обработки входящих сообщений
    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.WHITE54, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    # Диалоговое окно запроса имени
    join_user_name = ft.TextField(
        label="Введите имя чтобы присоединиться к чату",
        text_style=ft.TextStyle(font_family='Montserrat'),
        autofocus=True,
        on_submit=lambda e: join_chat_click(e),
        color=ft.colors.WHITE,
        bgcolor='#1C1B19',
        border_color=ft.colors.WHITE,
        label_style=ft.TextStyle(color=ft.colors.WHITE),
    )
    welcome_dlg = ft.AlertDialog(
        open=False,  # По умолчанию окно закрыто
        modal=True,
        title=ft.Text("Добро пожаловать!", color=ft.colors.WHITE, font_family='Montserrat'),
        content=ft.Column([join_user_name], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text="Join chat", on_click=lambda e: join_chat_click(e))],
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor="#1C1B19",
    )

    page.overlay.append(welcome_dlg)

    # Функция для присоединения к чату
    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Имя не может быть пустым"
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            welcome_dlg.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ", color=ft.colors.WHITE)
            page.pubsub.send_all(
                Message(
                    user_name=join_user_name.value,
                    text=f"{join_user_name.value} присоединился к чату.",
                    message_type="login_message",
                )
            )
            page.update()

    # Функция для обработки изменения вкладки
    def on_tab_change(e):
        if e.control.selected_index == 1:  # Если выбрана вкладка "Обсуждение"
            if not page.session.get("user_name"):  # Если имя пользователя не задано
                welcome_dlg.open = True
                page.update()

    # Вкладки для переключения между новостями и комментариями
    tabs = ft.Tabs(
        label_color='FFFFFF',
        indicator_color='#095644',
        label_text_style=ft.TextStyle(font_family='Montserrat'),
        selected_index=0,
        on_change=on_tab_change,  # Обработчик изменения вкладки
        tabs=[
            ft.Tab(
                text="Новости",
                content=ft.Container(
                    content=news_container,
                    alignment=ft.alignment.center,  # Центрируем содержимое
                    expand=True,
                ),
            ),
            ft.Tab(
                text="Обсуждение",
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=chat,
                                border=ft.border.all(1, ft.colors.WHITE),
                                border_radius=5,
                                padding=10,
                                height=500,  # Высота окошка чата
                                width=950,  # Ширина окошка чата
                                expand=False,
                                bgcolor="#1C1B19",
                            ),
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Container(
                                            content=new_message,
                                            height=50,  # Высота панели ввода сообщения
                                            expand=True,
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.SEND_ROUNDED,
                                            tooltip="Отправить сообщение",
                                            on_click=send_message_click,
                                            icon_color=ft.colors.WHITE,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                padding=10,
                                width=950,  # Ширина панели ввода сообщения
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Центрирование всей колонки
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,  # Центрирование содержимого контейнера
                    expand=True,
                ),
            ),
        ],
        expand=True,
    )

    # Функция для изменения маршрута
    def route_change(route):
        page.views.clear()
        if page.route == '/playersm':
            page.views.append(
                ft.View(
                    bgcolor="#1C1B19",
                    route='/playersm',
                    controls=
                    [
                        header(page), ft.Row([ft.Text("Мужская команда", font_family="Montserrat",
                                                      text_align=ft.TextAlign.CENTER, color='#FFFFFF', size=32,
                                                      weight=ft.FontWeight.W_600)],
                                             alignment=ft.MainAxisAlignment.CENTER),
                        ft.Container(content=player_row, padding=20, expand=True), footer
                    ]
                )
            )
        if page.route == '/playersf':
            page.views.append(
                ft.View(
                    bgcolor="#1C1B19",
                    route='/playersf',
                    controls=
                    [
                        header(page), ft.Row([ft.Text("Женская команда", font_family="Montserrat",
                                                      text_align=ft.TextAlign.CENTER, color='#FFFFFF', size=32,
                                                      weight=ft.FontWeight.W_600)],
                                             alignment=ft.MainAxisAlignment.CENTER),
                        ft.Container(content=player_rowf, padding=20), footer
                    ]
                )
            )
        elif page.route == '/main':
            page.views.append(
                ft.View(bgcolor="#1C1B19",
                        route='/main',
                        controls=[
                            header(page),  # Добавляем header (AppBar)
                            ft.Column(
                                [
                                    ft.Row([txt_number], alignment=ft.MainAxisAlignment.CENTER),
                                    ft.Row([about, team_img], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                                    ft.Row([video_container1, video_container2],
                                           alignment=ft.MainAxisAlignment.SPACE_EVENLY)
                                ]
                            ), footer
                        ], scroll=ft.ScrollMode.AUTO
                        )
            )
        elif page.route == '/news':
            page.views.append(
                ft.View(bgcolor="#1C1B19",
                        route='/news', controls=[header(page), ft.Container(
                        content=tabs,
                        padding=ft.padding.symmetric(horizontal=40),
                        alignment=ft.alignment.center,
                        width=page.width,
                        expand=True,
                    ), footer])
            )
        elif page.route == '/matches':
            page.views.append(
                ft.View(bgcolor="#1C1B19",
                        route='/macthes', controls=[header(page), matches_col, footer])
            )

        page.update()

    # Устанавливаем обработчик изменения маршрута
    page.on_route_change = route_change
    page.go(page.route)


# Запуск приложения
ft.app(main, view=ft.WEB_BROWSER, assets_dir="assets")
