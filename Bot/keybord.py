from telegram import InlineKeyboardButton

KMain_menu = [
    [InlineKeyboardButton("Сотрудники", callback_data="employees")],
    [InlineKeyboardButton("Проекты", callback_data="projects_list")],
    [InlineKeyboardButton("Выйти", callback_data="auth")]
    
    ]

start = [
            [InlineKeyboardButton("Авторизация", callback_data="auth")]
        ]

KAuthorization_menu = [
    [InlineKeyboardButton("Логин", callback_data="login")],
    [InlineKeyboardButton("Пароль", callback_data="password")],
    [InlineKeyboardButton("Компания", callback_data="company")],
    [InlineKeyboardButton("Вход", callback_data="main_menu")]
    ]

KProject_menu = [
            [InlineKeyboardButton("Список проектов", callback_data="projects_list")],
            [InlineKeyboardButton("Создать проект", callback_data="project_create")],
            [InlineKeyboardButton("Назад", callback_data="main_menu")]
    ]   

KBoard_menu = [
            [InlineKeyboardButton("Список всех доск", callback_data="board_list")],
            [InlineKeyboardButton("Изменить", callback_data="board_change")],
            [InlineKeyboardButton("Назад", callback_data="main_menu")]
    ]

KChange_User = [
            [InlineKeyboardButton("Удалить пользователя", callback_data="deletUser")],
            [InlineKeyboardButton("Выдать админку", callback_data="giveAdminRule")],
            [InlineKeyboardButton("Забрать админку", callback_data="takeAdminRule")],
            [InlineKeyboardButton("Назад", callback_data="members_list")]
    ]

KInfo_project = [
            [InlineKeyboardButton("Пользователи", callback_data="UsersByProjectId")],
            [InlineKeyboardButton("Изменить проект", callback_data="change_project")],
            [InlineKeyboardButton("Удалить проект", callback_data="deleate_project")],
            [InlineKeyboardButton("Назад", callback_data="projects_list")]
    ]

KChange_Project = [
            [InlineKeyboardButton("Добавить участника", callback_data="???")],
            [InlineKeyboardButton("Удалить Участника", callback_data="???")],
            [InlineKeyboardButton("Изменить роль участника", callback_data="???")],
            [InlineKeyboardButton("Изменить имя проекта", callback_data="renameProject")],
            [InlineKeyboardButton("Назад", callback_data="KInfo_project")]
    ]

