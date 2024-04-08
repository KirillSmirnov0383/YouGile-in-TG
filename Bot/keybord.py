from telegram import InlineKeyboardButton

KMain_menu = [
    [InlineKeyboardButton("Сменить пользователя", callback_data="auth")],
    [InlineKeyboardButton("Сменить компанию", callback_data="auth")],
    [InlineKeyboardButton("Сотрудники", callback_data="employees")],
    [InlineKeyboardButton("Проекты", callback_data="projects")],
    [InlineKeyboardButton("Доски", callback_data="boards")]
    
    ]

KEmployees_menu = [
            [InlineKeyboardButton("Весь список сотрудников", callback_data="members_list")],
            [InlineKeyboardButton("Поиск по email", callback_data="search_email")],
            [InlineKeyboardButton("Пригласить в компанию", callback_data="invite_people")],
            [InlineKeyboardButton("Поиск по проекту", callback_data="search_project")],
            [InlineKeyboardButton("Назад", callback_data="main_menu")]
        ]

start = [
            [InlineKeyboardButton("Авторизация", callback_data="auth")]
        ]

KAuthorization_menu = [
    [InlineKeyboardButton("Логин", callback_data="??")],
    [InlineKeyboardButton("Компания", callback_data="??")],
    [InlineKeyboardButton("Пароль", callback_data="??")],
    [InlineKeyboardButton("Вход", callback_data="main_menu")]
    ]

KProject_menu = [
            [InlineKeyboardButton("Список проектов", callback_data="projects_list")],
            [InlineKeyboardButton("Создать проект", callback_data="project_create")],
            [InlineKeyboardButton("доски", callback_data="board")],
            [InlineKeyboardButton("Назад", callback_data="main_menu")]
    ]   

KBoard_menu = [
            [InlineKeyboardButton("Список всех доск", callback_data="board_list")],
            [InlineKeyboardButton("Изменить", callback_data="board_change")],
            [InlineKeyboardButton("Назад", callback_data="main_menu")]
    ]
