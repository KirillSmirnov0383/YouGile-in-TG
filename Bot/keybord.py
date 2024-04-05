from telegram import InlineKeyboardButton

KMain_meny = [
    [InlineKeyboardButton("Сменить пользователя", callback_data="auth")],
    [InlineKeyboardButton("Сменить компанию", callback_data="auth")],
    [InlineKeyboardButton("Сотрудники", callback_data="employees")]
    ]

KEmployees_menu = [
            [InlineKeyboardButton("Поиск по email", callback_data="search_email")],
            [InlineKeyboardButton("Поиск по проекту", callback_data="search_project")],
            [InlineKeyboardButton("Дать/Забрать админку", callback_data="admin")],
            [InlineKeyboardButton("Удалить сотрудника", callback_data="delete")],
            [InlineKeyboardButton("Назад", callback_data="back")]
        ]

start = [
            [InlineKeyboardButton("Авторизация", callback_data="auth")]
        ]