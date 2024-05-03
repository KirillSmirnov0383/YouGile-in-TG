from telegram import InlineKeyboardButton
from services.NetworkingManager import NetworkingManager as NM
from DB.Database import DatabaseManager

employees = ["Сотрудник 1", "Сотрудник 2", "Сотрудник 3", "Сотрудник 4", "Сотрудник 5", "Сотрудник 6", "Сотрудник 7", "Сотрудник 8", "Сотрудник 9", "Сотрудник 10", "Сотрудник 11", "Сотрудник 12", "Сотрудник 13", "Сотрудник 14", "Сотрудник 15", "Сотрудник 16", "Сотрудник 17", "Сотрудник 18", "Сотрудник 19", "Сотрудник 20", "Сотрудник 21", "Сотрудник 22", "Сотрудник 23", "Сотрудник 24", "Сотрудник 25",]

projects = ["Проект 1", "Проект 2", "Проект 3", "Проект 4", "Проект 5", "Проект 6", "Проект 7", "Проект 8", "Проект 9", "Проект 10", "Проект 11", "Проект 12", "Проект 13", "Проект 14", "Проект 15", "Проект 16", "Проект 17", "Проект 18", "Проект 19", "Проект 20", "Проект 21", "Проект 22", "Проект 23", "Проект 24", "Проект 25"]

def Ktask_list(Api, columId, BoId, current_page = 0, task_per_page = 6):
    boards_dict = NM.getTasksByColumn(key=Api, column_id=columId)

    keys = list(boards_dict.keys())
    
    start_index = current_page * task_per_page
    end_index = min((current_page + 1) * task_per_page, len(keys))

    task_buttons = []
    for i in range(start_index, end_index, 2):  # Увеличиваем шаг на 2, чтобы добавить по два сотрудника в одну строку
        buttons_row = []
        for j in range(2):  # Добавляем по два сотрудника в одну строку
            if i + j < len(keys):
                button = InlineKeyboardButton(boards_dict[keys[i + j]], callback_data=f"TaskById{keys[i + j]}")
                buttons_row.append(button)
        task_buttons.append(buttons_row)

    if len(keys) <= 6:
        navigation_buttons = [[InlineKeyboardButton("Создать Таску", callback_data="CreateTask{columId}")],
            [InlineKeyboardButton(" ", callback_data="-"), 
            InlineKeyboardButton("Назад", callback_data=f"СolumListId{BoId}"), 
            InlineKeyboardButton(" ", callback_data="-")]
        ]
    elif current_page == 0:
        navigation_buttons = [[InlineKeyboardButton("Создать Таску", callback_data="???")],
            [InlineKeyboardButton(" ", callback_data="-"), 
            InlineKeyboardButton("Назад", callback_data=f"СolumListId{BoId}"), 
            InlineKeyboardButton("->", callback_data=f"TaskButRight{columId}")]
        ]
    elif end_index == len(keys):
        navigation_buttons = [[InlineKeyboardButton("Создать Таску", callback_data="???")],
            [InlineKeyboardButton("<-", callback_data=f"TaskButLeft{columId}"), 
            InlineKeyboardButton("Назад", callback_data=f"СolumListId{BoId}"), 
            InlineKeyboardButton(" ", callback_data="-")]
        ]
    else:
        navigation_buttons = [[InlineKeyboardButton("Создать колонку", callback_data="???")],
            [InlineKeyboardButton("<-", callback_data=f"TaskButLeft{columId}"), 
            InlineKeyboardButton("Назад", callback_data=f"СolumListId{BoId}"), 
            InlineKeyboardButton("->", callback_data=f"TaskButRight{columId}")]
        ]         

    return task_buttons + navigation_buttons

def Kcolum_list(Api, columId, projectId, BoId, current_page = 0, colum_per_page = 6):
    boards_dict = NM.getColumns(key=Api, board_id=columId)

    keys = list(boards_dict.keys())
    
    start_index = current_page * colum_per_page
    end_index = min((current_page + 1) * colum_per_page, len(keys))

    colum_buttons = []
    for i in range(start_index, end_index, 2):  # Увеличиваем шаг на 2, чтобы добавить по два сотрудника в одну строку
        buttons_row = []
        for j in range(2):  # Добавляем по два сотрудника в одну строку
            if i + j < len(keys):
                button = InlineKeyboardButton(boards_dict[keys[i + j]], callback_data=f"ColumById{keys[i + j]}")
                buttons_row.append(button)
        colum_buttons.append(buttons_row)

    if len(keys) <= 6:
        navigation_buttons = [[InlineKeyboardButton("Создать колонку", callback_data=f"CreateColumId{projectId}")],
            [InlineKeyboardButton(" ", callback_data="-"), 
            InlineKeyboardButton("Назад", callback_data=f"BoardsById{BoId}"), 
            InlineKeyboardButton(" ", callback_data="-")]
        ]
    elif current_page == 0:
        navigation_buttons = [[InlineKeyboardButton("Создать колонку", callback_data=f"CreateColumId{projectId}")],
            [InlineKeyboardButton(" ", callback_data="-"), 
            InlineKeyboardButton("Назад", callback_data=f"BoardsById{BoId}"), 
            InlineKeyboardButton("->", callback_data=f"ColumButRight{columId}")]
        ]
    elif end_index == len(keys):
        navigation_buttons = [[InlineKeyboardButton("Создать колонку", callback_data=f"CreateColumId{projectId}")],
            [InlineKeyboardButton("<-", callback_data=f"ColumButLeft{columId}"), 
            InlineKeyboardButton("Назад", callback_data=f"BoardsById{BoId}"), 
            InlineKeyboardButton(" ", callback_data="-")]
        ]
    else:
        navigation_buttons = [[InlineKeyboardButton("Создать колонку", callback_data=f"CreateColumId{projectId}")],
            [InlineKeyboardButton("<-", callback_data=f"ColumButLeft{columId}"), 
            InlineKeyboardButton("Назад", callback_data=f"BoardsById{BoId}"), 
            InlineKeyboardButton("->", callback_data=f"ColumButRight{columId}")]
        ]         

    return colum_buttons + navigation_buttons

def Kboards_list(Api, projectId, current_page = 0, boards_per_page = 6):
    boards_dict = NM.getBoardsByProjectID(key=Api, project_id=projectId)

    keys = list(boards_dict.keys())
    
    start_index = current_page * boards_per_page
    end_index = min((current_page + 1) * boards_per_page, len(keys))

    boards_buttons = []
    for i in range(start_index, end_index, 2):  # Увеличиваем шаг на 2, чтобы добавить по два сотрудника в одну строку
        buttons_row = []
        for j in range(2):  # Добавляем по два сотрудника в одну строку
            if i + j < len(keys):
                button = InlineKeyboardButton(boards_dict[keys[i + j]], callback_data=f"BoardsById{keys[i + j]}")
                buttons_row.append(button)
        boards_buttons.append(buttons_row)

    if len(keys) <= 6:
        navigation_buttons = [[InlineKeyboardButton(f"Создать доску", callback_data=f"CreateBoardsById{projectId}")],
            [InlineKeyboardButton(" ", callback_data="-"), 
            InlineKeyboardButton("Назад", callback_data=f"ProjectId{projectId}"), 
            InlineKeyboardButton(" ", callback_data="-")]
        ]
    elif current_page == 0:
        navigation_buttons = [[InlineKeyboardButton(f"Создать доску", callback_data=f"CreateBoardsById{projectId}")],
            [InlineKeyboardButton(" ", callback_data="-"), 
            InlineKeyboardButton("Назад", callback_data=f"ProjectId{projectId}"), 
            InlineKeyboardButton("->", callback_data=f"BoardsButRight{projectId}")]
        ]
    elif end_index == len(keys):
        navigation_buttons = [
            [InlineKeyboardButton("<-", callback_data=f"BoardsButLeft{projectId}"), 
            InlineKeyboardButton("Назад", callback_data=f"ProjectId{projectId}"), 
            InlineKeyboardButton(" ", callback_data="-")]
        ]
    else:
        navigation_buttons = [[InlineKeyboardButton(f"Создать доску", callback_data=f"CreateBoardsById{projectId}")],
            [InlineKeyboardButton("<-", callback_data=f"BoardsButLeft{projectId}"), 
            InlineKeyboardButton("Назад", callback_data=f"ProjectId{projectId}"), 
            InlineKeyboardButton("->", callback_data=f"BoardsButRight{projectId}")]
        ]         

    return boards_buttons + navigation_buttons

def Kmembers_list(Api, current_page = 0, employees_per_page = 6, email=None, projectId=None, projectIdForAdd=None, FlagDel=False, projectIdForChangeRole=None):
    staff_dict = NM.getStaff(Api, email, projectId)
    start_index = current_page * employees_per_page
    keys = list(staff_dict.keys())

    end_index = min((current_page + 1) * employees_per_page, len(keys))
    if projectIdForAdd and projectId and FlagDel:
        buttontext = 'employeesBoardDeleteId'
    elif projectIdForChangeRole:
        buttontext = 'BoardChangeUserRoleId'
    elif projectIdForAdd:
        buttontext = 'employeesBoardAddId'
    else: buttontext = 'employeesBoardId'
    employee_buttons = []
    for i in range(start_index, end_index, 2):  # Увеличиваем шаг на 2, чтобы добавить по два сотрудника в одну строку
        buttons_row = []
        for j in range(2):  # Добавляем по два сотрудника в одну строку
            if i + j < len(keys):
                button = InlineKeyboardButton(staff_dict[keys[i + j]], callback_data=f"{buttontext}{keys[i + j]}")
                buttons_row.append(button)
        employee_buttons.append(buttons_row)
    if projectId or projectIdForAdd or projectIdForChangeRole:
        back = f'ProjectId{projectId}'
    else: back = 'employees'
    if len(keys) <= 6:
        navigation_buttons = [
            [InlineKeyboardButton(" ", callback_data="-"), 
            InlineKeyboardButton("Назад", callback_data=f"{back}"), 
            InlineKeyboardButton(" ", callback_data="-")]
        ]
    elif current_page == 0:
        navigation_buttons = [
            [InlineKeyboardButton(" ", callback_data="-"), 
            InlineKeyboardButton("Назад", callback_data=f"{back}"), 
            InlineKeyboardButton("->", callback_data="MembersButRight")]
        ]
    elif end_index == len(keys):
        navigation_buttons = [
            [InlineKeyboardButton("<-", callback_data="MembersButLeft"), 
            InlineKeyboardButton("Назад", callback_data=f"{back}"), 
            InlineKeyboardButton(" ", callback_data="-")]
        ]
    else:
        navigation_buttons = [
            [InlineKeyboardButton("<-", callback_data="MembersButLeft"), 
            InlineKeyboardButton("Назад", callback_data=f"{back}"), 
            InlineKeyboardButton("->", callback_data="MembersButRight")]
        ]         

    return employee_buttons + navigation_buttons

def Kprojects_list(Api, current_page = 0, projects_per_page = 6):
    project_dict = NM.getProjects(Api)

    keys = list(project_dict.keys())
    
    start_index = current_page * projects_per_page
    end_index = min((current_page + 1) * projects_per_page, len(keys))

    projects_buttons = []
    for i in range(start_index, end_index, 2):  # Увеличиваем шаг на 2, чтобы добавить по два сотрудника в одну строку
        buttons_row = []
        for j in range(2):  # Добавляем по два сотрудника в одну строку
            if i + j < len(keys):
                button = InlineKeyboardButton(project_dict[keys[i + j]], callback_data=f"ProjectId{keys[i + j]}")
                buttons_row.append(button)
        projects_buttons.append(buttons_row)

    if len(keys) <= 6:
        navigation_buttons = [[InlineKeyboardButton("Создать проект", callback_data="project_create")],
            [InlineKeyboardButton(" ", callback_data="-"), 
            InlineKeyboardButton("Назад", callback_data="main_menu"), 
            InlineKeyboardButton(" ", callback_data="-")]
        ]
    elif current_page == 0:
        navigation_buttons = [[InlineKeyboardButton("Создать проект", callback_data="project_create")],
            [InlineKeyboardButton(" ", callback_data="-"), 
            InlineKeyboardButton("Назад", callback_data="main_menu"), 
            InlineKeyboardButton("->", callback_data="ProjectsButRight")]
        ]
    elif end_index == len(keys):
        navigation_buttons = [[InlineKeyboardButton("Создать проект", callback_data="project_create")],
            [InlineKeyboardButton("<-", callback_data="ProjectsButLeft"), 
            InlineKeyboardButton("Назад", callback_data="main_menu"), 
            InlineKeyboardButton(" ", callback_data="-")]
        ]
    else:
        navigation_buttons = [[InlineKeyboardButton("Создать проект", callback_data="project_create")],
            [InlineKeyboardButton("<-", callback_data="ProjectsButLeft"), 
            InlineKeyboardButton("Назад", callback_data="main_menu"), 
            InlineKeyboardButton("->", callback_data="ProjectsButRight")]
        ]         

    return projects_buttons + navigation_buttons

def Kemploees_info(Flag=True):
    if Flag:
        Kemploeesinfo = [
                [InlineKeyboardButton("Изменить", callback_data="ChangeUser")],
                [InlineKeyboardButton("Назад", callback_data="members_list")]
        ]
    else:
        Kemploeesinfo = [
                [InlineKeyboardButton("Назад", callback_data="members_list")]
        ]   
    return Kemploeesinfo


def KEmployees_menu(Flag=True):
    if Flag:
        KEmployees_menu = [
                    [InlineKeyboardButton("Весь список сотрудников", callback_data="members_list")],
                    [InlineKeyboardButton("Поиск по email", callback_data="search_email")],
                    [InlineKeyboardButton("Пригласить в компанию", callback_data="invite_people")],
                    [InlineKeyboardButton("Назад", callback_data="main_menu")]
                ]
    else:
        KEmployees_menu = [
                    [InlineKeyboardButton("Весь список сотрудников", callback_data="members_list")],
                    [InlineKeyboardButton("Поиск по email", callback_data="search_email")],
                    [InlineKeyboardButton("Назад", callback_data="main_menu")]
                ]
    return KEmployees_menu

def KInfo_project(ProjectId):
    KInfo_project = [
                [InlineKeyboardButton("Пользователи", callback_data=f"UsersByProjectId{ProjectId}")],
                [InlineKeyboardButton("Доски", callback_data=f"ListBoardsById{ProjectId}")],
                [InlineKeyboardButton("Изменить проект", callback_data=f"change_projectId{ProjectId}")],
                [InlineKeyboardButton("Удалить проект", callback_data=f"deleate_projectId{ProjectId}")],
                [InlineKeyboardButton("Назад", callback_data=f"projects_list")]
        ]
    return KInfo_project

def KChange_Project(ProjectId):
    KChange_Project = [
            [InlineKeyboardButton(f"Добавить участника", callback_data=f"AddUserInProject{ProjectId}")],
            [InlineKeyboardButton(f"Удалить Участника", callback_data=f"DeleateUserInProject{ProjectId}")],
            [InlineKeyboardButton(f"Изменить роль участника", callback_data=f"ChangeUserRoleListInProject{ProjectId}")],
            [InlineKeyboardButton(f"Изменить имя проекта", callback_data=f"renameProject{ProjectId}")],
            [InlineKeyboardButton("Назад", callback_data=f"ProjectId{ProjectId}")]
    ]
    return KChange_Project

def KChange_Role_User_Project(ProjectId):
    KChange_Role_User_Project = [
            [InlineKeyboardButton(f"Админ", callback_data=f"RoleProject{ProjectId}_admin")],
            [InlineKeyboardButton(f"Работник", callback_data=f"RoleProject{ProjectId}_worker")],
            [InlineKeyboardButton(f"Наблюдатель", callback_data=f"RoleProject{ProjectId}_observer")],
            [InlineKeyboardButton("Назад", callback_data="projects_list")]
    ]
    return KChange_Role_User_Project
    

def KBoard_Meny(ProjectId):
    KBoard_Meny = [
            [InlineKeyboardButton(f"Список всех досок", callback_data=f"ListBoardsById{ProjectId}")],
            [InlineKeyboardButton(f"Создать доску", callback_data=f"CreateBoardsById{ProjectId}")],
            [InlineKeyboardButton("Назад", callback_data=f"ProjectId{ProjectId}")]
    ]
    return KBoard_Meny

def Kboards_info(BoardId, PrId):
    KBoard_Meny = [
            [InlineKeyboardButton(f"Изменить доску", callback_data=f"ChangeBoardId{BoardId}")],
            [InlineKeyboardButton(f"Удалить доску", callback_data=f"DeleteBoardId{BoardId}")],
            [InlineKeyboardButton(f"Колонки", callback_data=f"СolumListId{BoardId}")],
            [InlineKeyboardButton("Назад", callback_data=f"ListBoardsById{PrId}")]
    ]
    return KBoard_Meny

def Ktask_info(TaskId):
    KBoard_Meny = [
            [InlineKeyboardButton(f"???", callback_data=f"???")],
            [InlineKeyboardButton(f"???", callback_data=f"???")],
            [InlineKeyboardButton(f"???", callback_data=f"???")],
            [InlineKeyboardButton("???", callback_data=f"???")]
    ]
    return KBoard_Meny

def KEdit_board(BoId):
    KEdit_board = [
            [InlineKeyboardButton(f"Удалить доску", callback_data=f"DeleteBoardId{BoId}")],
            [InlineKeyboardButton(f"Изменить название доски", callback_data=f"RenameBoardId{BoId}")],
            [InlineKeyboardButton("Назад", callback_data=f"BoardsById{BoId}")]
    ]
    return KEdit_board

