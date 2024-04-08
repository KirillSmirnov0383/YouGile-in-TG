from telegram import InlineKeyboardButton

employees = ["Сотрудник 1", "Сотрудник 2", "Сотрудник 3", "Сотрудник 4", "Сотрудник 5", "Сотрудник 6", "Сотрудник 7", "Сотрудник 8", "Сотрудник 9", "Сотрудник 10", "Сотрудник 11", "Сотрудник 12", "Сотрудник 13", "Сотрудник 14", "Сотрудник 15", "Сотрудник 16", "Сотрудник 17", "Сотрудник 18", "Сотрудник 19", "Сотрудник 20", "Сотрудник 21", "Сотрудник 22", "Сотрудник 23", "Сотрудник 24", "Сотрудник 25",]


projects = ["Проект 1", "Проект 2", "Проект 3", "Проект 4", "Проект 5", "Проект 6", "Проект 7", "Проект 8", "Проект 9", "Проект 10", "Проект 11", "Проект 12", "Проект 13", "Проект 14", "Проект 15", "Проект 16", "Проект 17", "Проект 18", "Проект 19", "Проект 20", "Проект 21", "Проект 22", "Проект 23", "Проект 24", "Проект 25"]

def Kmembers_list(current_page = 0, employees_per_page = 6):
    start_index = current_page * employees_per_page
    end_index = min((current_page + 1) * employees_per_page, len(employees))

    employee_buttons = []
    for i in range(start_index, end_index, 2):  # Увеличиваем шаг на 2, чтобы добавить по два сотрудника в одну строку
        buttons_row = []
        for j in range(2):  # Добавляем по два сотрудника в одну строку
            if i + j < len(employees):
                button = InlineKeyboardButton(employees[i + j], callback_data="board_list")
                buttons_row.append(button)
        employee_buttons.append(buttons_row)


    if current_page == 0:
        navigation_buttons = [
            [InlineKeyboardButton(" ", callback_data="-"), 
            InlineKeyboardButton("Назад", callback_data="main_menu"), 
            InlineKeyboardButton("->", callback_data="MembersButRight")]
        ]
    elif end_index == len(employees):
        navigation_buttons = [
            [InlineKeyboardButton("<-", callback_data="MembersButLeft"), 
            InlineKeyboardButton("Назад", callback_data="main_menu"), 
            InlineKeyboardButton(" ", callback_data="-")]
        ]
    else:
        navigation_buttons = [
            [InlineKeyboardButton("<-", callback_data="MembersButLeft"), 
            InlineKeyboardButton("Назад", callback_data="main_menu"), 
            InlineKeyboardButton("->", callback_data="MembersButRight")]
        ]         

    return employee_buttons + navigation_buttons

def Kprojects_list(current_page = 0, projects_per_page = 6):
    start_index = current_page * projects_per_page
    end_index = min((current_page + 1) * projects_per_page, len(projects))

    projects_buttons = []
    for i in range(start_index, end_index, 2):  # Увеличиваем шаг на 2, чтобы добавить по два сотрудника в одну строку
        buttons_row = []
        for j in range(2):  # Добавляем по два сотрудника в одну строку
            if i + j < len(projects):
                button = InlineKeyboardButton(projects[i + j], callback_data="board_list")
                buttons_row.append(button)
        projects_buttons.append(buttons_row)


    if current_page == 0:
        navigation_buttons = [
            [InlineKeyboardButton(" ", callback_data="-"), 
            InlineKeyboardButton("Назад", callback_data="main_menu"), 
            InlineKeyboardButton("->", callback_data="ProjectsButRight")]
        ]
    elif end_index == len(projects):
        navigation_buttons = [
            [InlineKeyboardButton("<-", callback_data="ProjectsButLeft"), 
            InlineKeyboardButton("Назад", callback_data="main_menu"), 
            InlineKeyboardButton(" ", callback_data="-")]
        ]
    else:
        navigation_buttons = [
            [InlineKeyboardButton("<-", callback_data="ProjectsButLeft"), 
            InlineKeyboardButton("Назад", callback_data="main_menu"), 
            InlineKeyboardButton("->", callback_data="ProjectsButRight")]
        ]         

    return projects_buttons + navigation_buttons


    