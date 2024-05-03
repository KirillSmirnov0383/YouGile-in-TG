from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Application, MessageHandler, filters
from Bot.keybord import KMain_menu, start, KAuthorization_menu, KBoard_menu, KProject_menu, KChange_User
from Bot.createKeyboard import Kmembers_list, Kprojects_list, Kemploees_info, KEmployees_menu, KInfo_project, KChange_Project, KChange_Role_User_Project, KBoard_Meny, Kboards_list, Kboards_info, Kcolum_list, Ktask_list, Ktask_info, KEdit_board
import sys 
from services.NetworkingManager import NetworkingManager as NM
from DB.Database import DatabaseManager
#sys.path.append("../YouGile-in-TG")
#print(sys.path)
#from services.NetworkingManager import NetworkingManager

TOKEN = "6500071185:AAEQ_ChvOVjhwJLaJxwBN9JDqDbrDhNrnyc"
LMEMBERS = 0
LPROJECT = 0
LBOARDS = 0
LCOLUM = 0
LTASK = 0

STATE_LOGIN = 1

LOGIN = ''
COMPANY = ''
PASSWORD = ''
STATE_DATE = 1

class TelegramBot:
    def __init__(self):
        self.STATE_LOGIN = 1
        self.STATE_COMPANY = 2
        self.STATE_PASSWORD = 3
        self.STATE_SEARCH_EMP_EMAIL = 4
        self.STATE_INVITE_EMP_EMAIL = 5
        self.STATE_CREATE_PROJECT = 6
        self.STATE_CHAMGE_PROJECT_NAME = 7
        self.STATE_CREATE_BOARD = 8
        self.STATE_RENAME_BOARD = 9
        self.STATE_CREATE_COLUM = 10
        self.TGID = None

        self.companyID = None
        self.User_ID = None
        self.Project_ID = None
        self.Board_ID = None
        self.Colum_ID = None

        self.updater = Application.builder().token(TOKEN).build()
        
        self.users = {}  # Dictionary to store user information

        self.DB = DatabaseManager()

    async def start(self, update, context, FlagAuth=True):
        message = update.message
        try:
            self.TGID = message.from_user.id
        except:
            pass

        reply_markup = InlineKeyboardMarkup(KAuthorization_menu)
        self.DB.add_user(self.TGID)
        user_dict = self.DB.get_user_data(self.TGID)
        if FlagAuth:
            text = f'Добро пожаловать! Выберите действие: \n Ваше имя: {user_dict["email"]}\n Ваше компания: {user_dict["company"]}\n Ваше пароль: {user_dict["password"]}'
        else:
            text = f'Данные некоректны: {user_dict["email"]}\n Ваше компания: {user_dict["company"]}\n Ваше пароль: {user_dict["password"]}'
        try:
            await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                                message_id=update.callback_query.message.message_id,
                                                text=text, 
                                                reply_markup=reply_markup)
        except AttributeError:
            await message.reply_text(text, reply_markup=reply_markup)

    async def main_menu(self, update, context):
        reply_markup = InlineKeyboardMarkup(KMain_menu)
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      text=f"Главное меню:",
                                      reply_markup=reply_markup)

    async def employees_menu(self, update, context):
        reply_markup = InlineKeyboardMarkup(KEmployees_menu())
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      text="Меню сотрудников:",
                                      reply_markup=reply_markup)
        
    async def project_menu(self, update, context):
        reply_markup = InlineKeyboardMarkup(KProject_menu)
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      text="Меню проектов:",
                                      reply_markup=reply_markup)
        
    async def members_list(self, update, context, email=None, projectId=None, projectIdForAdd=None, FlagDel=False, projectIdForChangeRole=None):
        user_data = self.DB.get_user_data(self.TGID)
        Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
        reply_markup = InlineKeyboardMarkup(Kmembers_list(Api, LMEMBERS, email=email, projectId=projectId, projectIdForAdd=projectIdForAdd, FlagDel=FlagDel, projectIdForChangeRole=projectIdForChangeRole))
        try:
            await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                        message_id=update.callback_query.message.message_id,
                                        text="Список сотрудников:",
                                        reply_markup=reply_markup)
        except AttributeError:
            await update.message.reply_text('Список сотрудников:', reply_markup=reply_markup)
        
    async def projects_list(self, update, context):
        user_data = self.DB.get_user_data(self.TGID)
        Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
        reply_markup = InlineKeyboardMarkup(Kprojects_list(Api, LPROJECT))
        try:
            await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      text="Список проектов:",
                                      reply_markup=reply_markup)
        except AttributeError:
            await update.message.reply_text('Список проектов:', reply_markup=reply_markup)

    async def delete_last_messages(self, update, context):
        chat_id = update.message.chat_id
        message_ids = []
        messages = context.bot.fetch_all(chat_id)
        context.bot.delete_message(chat_id, update.message.message_id - 1)
        # Получаем последние два сообщения в чате
        messages = await context.bot.get_chat(chat_id)

        for message in messages:
            message_ids.append(message.message_id)

        # Удаляем последние два сообщения
        for message_id in message_ids:
            await context.bot.delete_message(chat_id, message_id)

    async def changeLogin(self, update, context):
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="auth")]])
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                            message_id=update.callback_query.message.message_id,
                                            text="Пожалуйста, введите ваш логин:",
                                            reply_markup=reply_markup)
        self.state = self.STATE_LOGIN

    async def changeCompany(self, update, context):
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="auth")]])
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                            message_id=update.callback_query.message.message_id,
                                            text="Пожалуйста, введите название вашей компании:",
                                            reply_markup=reply_markup)
        self.state = self.STATE_COMPANY

    async def changePassword(self, update, context):
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="auth")]])
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                            message_id=update.callback_query.message.message_id,
                                            text="Пожалуйста, введите пароль:",
                                            reply_markup=reply_markup)
        self.state = self.STATE_PASSWORD

    async def searchEmploeesByEmail(self, update, context):
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="employees")]])
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                            message_id=update.callback_query.message.message_id,
                                            text="Пожалуйста, введите почту сотрудника, которого вы хотите найти:",
                                            reply_markup=reply_markup)
        self.state = self.STATE_SEARCH_EMP_EMAIL

    async def inviteEploeesByEmail(self, update, context):
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="employees")]])
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                            message_id=update.callback_query.message.message_id,
                                            text="Пожалуйста, введите почту человека, которого вы хотите пригласить:",
                                            reply_markup=reply_markup)
        self.state = self.STATE_INVITE_EMP_EMAIL

    async def rename_project(self, update, context, projectId):
        projectId = projectId[projectId.find('Project')+7:]
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="projects_list")]])
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                            message_id=update.callback_query.message.message_id,
                                            text="Пожалуйста, введите новое имя проекта",
                                            reply_markup=reply_markup)
        self.state = {self.STATE_CHAMGE_PROJECT_NAME: projectId}

    async def handle_message(self, update, context):
        if self.state == self.STATE_LOGIN:
            self.state = None
            self.DB.set_user_email(update.message.text, update.message.from_user.id)
            #await self.delete_last_messages(update, context)
            await self.start(update, context)
        elif self.state == self.STATE_COMPANY:
            self.state = None
            self.DB.set_user_company(update.message.text, update.message.from_user.id)
            #await self.delete_last_messages(update, context)
            await self.start(update, context)
        elif self.state == self.STATE_PASSWORD:
            self.state = None
            self.DB.set_user_password(update.message.text, update.message.from_user.id)
            #await self.delete_last_messages(update, context)
            await self.start(update, context)
        elif self.state == self.STATE_SEARCH_EMP_EMAIL:
            user_data = self.DB.get_user_data(self.TGID)
            Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
            self.state = None
            email = update.message.text
            await self.members_list(update, context, email=email)
            #await self.delete_last_messages(update, context)
        elif self.state == self.STATE_INVITE_EMP_EMAIL:
            user_data = self.DB.get_user_data(self.TGID)
            Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
            self.state = None
            email = update.message.text
            NM.inviteStaff(email=email, key=Api)
            await self.members_list(update, context)
            #await self.delete_last_messages(update, context)
        elif self.state == self.STATE_CREATE_PROJECT:
            user_data = self.DB.get_user_data(self.TGID)
            Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
            self.state = None
            title = update.message.text
            NM.createProject(key=Api, title=title, users=dict())
            await self.projects_list(update, context)
            #await self.delete_last_messages(update, context)
        elif self.state == self.STATE_CHAMGE_PROJECT_NAME or self.STATE_CHAMGE_PROJECT_NAME in self.state.keys():
            user_data = self.DB.get_user_data(self.TGID)
            Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
            title = update.message.text
            NM.editProject(key=Api, title=title, users=dict(), project_id=self.state[7])
            self.state = None
            await self.projects_list(update, context)
            #await self.delete_last_messages(update, context)
            
        elif self.state == self.STATE_CREATE_BOARD or self.STATE_CREATE_BOARD in self.state.keys():
            user_data = self.DB.get_user_data(self.TGID)
            prId = list(self.state.keys())[0]
            Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
            title = update.message.text
            NM.createBoard(key=Api, project_id=self.state[prId], title=title)
            await self.board_list(update, context, self.state[prId])
            self.state = None
            #await self.delete_last_messages(update, context)
        elif self.state == self.STATE_RENAME_BOARD or self.STATE_RENAME_BOARD in self.state.keys():
            user_data = self.DB.get_user_data(self.TGID)
            BoId = list(self.state.keys())[0]
            Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
            title = update.message.text
            NM.renameBoard(key=Api, new_title=title, board_id=self.state[BoId])
            await self.board_list(update, context, self.Project_ID)
            self.state = None
            #await self.delete_last_messages(update, context)
        elif self.state == self.STATE_CREATE_COLUM or self.STATE_CREATE_COLUM in self.state.keys():
            user_data = self.DB.get_user_data(self.TGID)
            Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
            title = update.message.text
            NM.createColumn(key=Api, title=title, board_id=self.Board_ID)
            await self.colum_list(update, context, self.Board_ID)
            self.state = None
            #await self.delete_last_messages(update, context)
        else:
            await update.message.reply_text("Что вы хотите изменить?")
    
    async def employeesBoardId(self, update, context, id):
        self.User_ID = id[id.find('Id')+2:]
        user_data = self.DB.get_user_data(self.TGID)
        Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
        data, flagAdmin = NM.getStaffById(self.User_ID, Api)

        reply_markup = InlineKeyboardMarkup(Kemploees_info())
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      text=data,
                                      reply_markup=reply_markup)
    async def ChangeUser(self, update, context):
        reply_markup = InlineKeyboardMarkup(KChange_User)
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      text="data",
                                      reply_markup=reply_markup)
        
    async def deletUser(self, update, context):
        user_data = self.DB.get_user_data(self.TGID)
        Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
        NM.deleteUser(key=Api, user_id=self.User_ID)
        self.User_ID = None
        await self.members_list(update, context)

    async def giveAdminRule(self, update, context):
        user_data = self.DB.get_user_data(self.TGID)
        Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
        NM.giveAdmin(key=Api, id=self.User_ID, isAdmin=True)
        self.User_ID = None
        await self.members_list(update, context)

    async def takeAdminRule(self, update, context):
        user_data = self.DB.get_user_data(self.TGID)
        Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
        NM.giveAdmin(key=Api, id=self.User_ID, isAdmin=False)
        self.User_ID = None
        await self.members_list(update, context)

    async def projectId(self, update, context, id):
        self.Project_ID = id[id.find('Id')+2:]
        user_data = self.DB.get_user_data(self.TGID)
        Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
        data = NM.getProjectById(key=Api, project_id=self.Project_ID)

        reply_markup = InlineKeyboardMarkup(KInfo_project(self.Project_ID))
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      text=data,
                                      reply_markup=reply_markup)
    
    async def edit_project(self, update, context, title=None, isDeleate=None, users=dict()):
        if title:
            title = title[title.find('Id')+2:]
        user_data = self.DB.get_user_data(self.TGID)
        Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
        NM.editProject(key=Api, project_id=self.Project_ID, isDelete=isDeleate, title=title, users=users)
        await self.projects_list(update, context)

    async def project_create(self, update, context):
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="projects")]])
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                            message_id=update.callback_query.message.message_id,
                                            text="Пожалуйста, введите название компании:",
                                            reply_markup=reply_markup)
        self.state = self.STATE_CREATE_PROJECT

    async def Change_Project(self, update, context, projectId):
        reply_markup = InlineKeyboardMarkup(KChange_Project(projectId))
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                            message_id=update.callback_query.message.message_id,
                                            text="Хуй пизда",
                                            reply_markup=reply_markup)

    # async def change_project():
    #     user_data = self.DB.get_user_data(self.TGID)
    #     Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
    #     NM.giveAdmin(key=Api, id=self.User_ID, isAdmin=True)
    #     self.User_ID = None
    #     await self.members_list(update, context)
    #     KChange_Project

    async def user_roles(self, update, context, prId):
        reply_markup = InlineKeyboardMarkup(KChange_Role_User_Project(prId))
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                            message_id=update.callback_query.message.message_id,
                                            text="Выберите роль",
                                            reply_markup=reply_markup)
        
    async def boards_menu(self, update, context, prId):
        reply_markup = InlineKeyboardMarkup(KBoard_Meny(prId))
        try:
            await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                                message_id=update.callback_query.message.message_id,
                                                text="Меню Досок:",
                                                reply_markup=reply_markup)
        except AttributeError:
            await update.message.reply_text('Список Досок:', reply_markup=reply_markup)
        
    async def board_create(self, update, context, prId):
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data=f"boardsId{prId}")]])
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                            message_id=update.callback_query.message.message_id,
                                            text="Пожалуйста, введите имя доски:",
                                            reply_markup=reply_markup)
        self.state = {self.STATE_CREATE_BOARD: prId}

    async def board_list(self, update, context, prId):
        self.Project_ID = prId
        user_data = self.DB.get_user_data(self.TGID)
        Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
        reply_markup = InlineKeyboardMarkup(Kboards_list(Api, prId, LBOARDS))
        try:
            await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                        message_id=update.callback_query.message.message_id,
                                        text="Список Досок:",
                                        reply_markup=reply_markup)
        except AttributeError:
            await update.message.reply_text('Список Досок:', reply_markup=reply_markup)

    async def board_by_id(self, update, context, BoardId):
        self.Board_ID = BoardId
        user_data = self.DB.get_user_data(self.TGID)
        Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
        data = NM.getBoardByID(board_id=BoardId, key=Api)
        reply_markup = InlineKeyboardMarkup(Kboards_info(BoardId, self.Project_ID))
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                    message_id=update.callback_query.message.message_id,
                                    text=data,
                                    reply_markup=reply_markup)
        
    async def deleate_board(self, update, context, BoardId):
        BoardId = BoardId[BoardId.find('Id')+2:]
        user_data = self.DB.get_user_data(self.TGID)
        Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
        NM.deleteBoard(key=Api, board_id=BoardId)
        await self.board_list(update, context, self.Project_ID)

    async def colum_list(self, update, context, ColumId):
        user_data = self.DB.get_user_data(self.TGID)
        Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
        reply_markup = InlineKeyboardMarkup(Kcolum_list(Api, ColumId, self.Project_ID, self.Board_ID, LCOLUM))
        try:
            await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                        message_id=update.callback_query.message.message_id,
                                        text="Список Колонок:",
                                        reply_markup=reply_markup)
        except AttributeError:
            await update.message.reply_text('Список Колонок:', reply_markup=reply_markup)

    async def task_list(self, update, context, ColumId):
        user_data = self.DB.get_user_data(self.TGID)
        Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
        reply_markup = InlineKeyboardMarkup(Ktask_list(Api, ColumId, self.Board_ID, LTASK))
        try:
            await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                        message_id=update.callback_query.message.message_id,
                                        text="Список Тасок:",
                                        reply_markup=reply_markup)
        except AttributeError:
            await update.message.reply_text('Список Тасок:', reply_markup=reply_markup)

    async def task_info(self, update, context, LskId):
        user_data = self.DB.get_user_data(self.TGID)
        Api = NM.getApiKey(login=user_data["email"], password=user_data["password"], companyID=self.companyID)
        data = NM.getTaskById(task_id=LskId, key=Api)
        reply_markup = InlineKeyboardMarkup(Ktask_info(LskId))
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                    message_id=update.callback_query.message.message_id,
                                    text=data,
                                    reply_markup=reply_markup)
        
    async def edit_board(self, update, context, BoId):
        reply_markup = InlineKeyboardMarkup(KEdit_board(BoId))
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                    message_id=update.callback_query.message.message_id,
                                    text='Выберите действие',
                                    reply_markup=reply_markup)
        
    async def rename_board(self, update, context, BoId):
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data=f"ChangeBoardId{BoId}")]])
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                            message_id=update.callback_query.message.message_id,
                                            text="Пожалуйста, введите имя доски:",
                                            reply_markup=reply_markup)
        self.state = {self.STATE_RENAME_BOARD: BoId}

    async def create_colum(self, update, context, BoId):
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data=f"СolumListId{self.Board_ID}")]])
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                            message_id=update.callback_query.message.message_id,
                                            text="Пожалуйста, введите название доски:",
                                            reply_markup=reply_markup)
        self.state = {self.STATE_CREATE_COLUM: BoId}

    async def button_handler(self, update, context):
        global LMEMBERS
        global LPROJECT
        global LBOARDS
        global LCOLUM
        global LTASK
        try:
            query = update.callback_query
            query.answer()

            if query.data == "auth":
            # Perform authorization logic
                query.message.reply_text("Вы вошли в систему.")
                await self.start(update, context)
            elif query.data == "main_menu":
                user_dict = self.DB.get_user_data(self.TGID)
                company_id = NM.login(user_dict["password"], user_dict["email"], user_dict["company"])
                if company_id:
                    self.companyID = self.DB.add_company(company_id, user_dict["company"])
                    self.DB.add_ApiKey(self.TGID, company_id)
                    await self.main_menu(update, context)
                else:
                    await self.start(update, context, FlagAuth=False)
            elif query.data == "employees":
                try:
                    if self.state != None:
                        self.state = None
                except:
                    pass
                await self.employees_menu(update, context)
            elif "BoardsButRight" in query.data:
                prId = query.data[query.data.find('Right')+5:]
                LBOARDS += 1
                await self.board_list(update, context, prId=prId)
            elif "BoardsButLeft" in query.data:    
                prId = query.data[query.data.find('Left')+4:]
                LBOARDS -= 1
                await self.board_list(update, context, prId=prId)
            elif "ColumButRight" in query.data:
                ColumId = query.data[query.data.find('Right')+5:]
                LCOLUM += 1
                await self.colum_list(update, context, ColumId=ColumId)
            elif "ColumButLeft" in query.data:    
                ColumId = query.data[query.data.find('Left')+4:]
                LCOLUM -= 1
                await self.colum_list(update, context, ColumId=ColumId)
            elif "TaskButRight" in query.data:
                ColumId = query.data[query.data.find('Right')+5:]
                LTASK += 1
                await self.task_list(update, context, ColumId=ColumId)
            elif "TaskButLeft" in query.data:    
                ColumId = query.data[query.data.find('Left')+4:]
                LTASK -= 1
                await self.task_list(update, context, ColumId=ColumId)
            elif query.data == "projects":
                await self.project_menu(update, context)
            elif "UsersByProjectId" in query.data:
                prId = query.data[query.data.find('Id')+2:]
                await self.members_list(update, context, projectId=prId)
            elif "CreateColumId" in query.data:
                BoId = query.data[query.data.find('Id')+2:]
                await self.create_colum(update, context, BoId=BoId)
            elif "ListBoardsById" in query.data:
                prId = query.data[query.data.find('Id')+2:]
                await self.board_list(update, context, prId=prId)
            #elif "CreateTask" in query.data:

            elif "CreateBoardsById" in query.data:
                prId = query.data[query.data.find('Id')+2:]
                await self.board_create(update, context, prId=prId)
            elif 'change_projectId' in query.data:
                prId = query.data[query.data.find('Id')+2:]
                await self.Change_Project(update, context, prId)
            elif "СolumListId" in query.data:
                ClId = query.data[query.data.find('Id')+2:]
                await self.colum_list(update, context, ColumId=ClId)
            elif "DeleteBoardId" in query.data:
                await self.deleate_board(update, context, BoardId=query.data)
            elif "RenameBoardId" in query.data:
                BoId = query.data[query.data.find('Id')+2:]
                await self.rename_board(update, context, BoId=BoId)
            elif 'renameProject' in query.data:
                await self.rename_project(update, context, query.data)
            elif 'AddUserInProject' in query.data:
                prId = query.data[query.data.find('Project')+7:]
                await self.members_list(update, context, projectIdForAdd=prId)
            elif 'DeleateUserInProject' in query.data:
                prId = query.data[query.data.find('Project')+7:]
                await self.members_list(update, context, projectId=prId, projectIdForAdd=prId, FlagDel=True)
            elif "employeesBoardAddId" in query.data:
                prId = query.data[query.data.find('Id')+2:]
                await self.edit_project(update, context, users={prId: 'worker'})
            elif "ChangeBoardId" in query.data:
                BoId = query.data[query.data.find('Id')+2:]
                await self.edit_board(update, context, BoId)
            elif "employeesBoardDeleteId" in query.data:
                prId = query.data[query.data.find('Id')+2:]
                await self.edit_project(update, context, users={prId: '-'})
            elif 'ChangeUserRoleListInProject' in query.data:
                prId = query.data[query.data.find('Project')+7:]
                await self.members_list(update, context, projectId=prId, projectIdForChangeRole=prId)
            elif "BoardChangeUserRoleId" in query.data:
                prId = query.data[query.data.find('Id')+2:]
                await self.user_roles(update, context, prId)
            elif "TaskById" in query.data:
                LskId = query.data[query.data.find('Id')+2:]
                await self.task_info(update, context, LskId)
            elif "RoleProject" in query.data:
                prId = query.data[query.data.find('Project')+7:].split('_')
                await self.edit_project(update, context, users={prId[0]: prId[1]})
            elif 'boardsId' in query.data:
                prId = query.data[query.data.find('Id')+2:]
                await self.boards_menu(update, context, prId=prId)
            elif 'ColumById' in query.data:
                CLId = query.data[query.data.find('Id')+2:]
                await self.task_list(update, context, ColumId=CLId)
            elif 'BoardsById' in query.data:
                BoardId = query.data[query.data.find('Id')+2:]
                await self.board_by_id(update, context, BoardId=BoardId)
            elif query.data == "members_list":
                await self.members_list(update, context)
            elif query.data == "MembersButRight":
                LMEMBERS += 1
                await self.members_list(update, context)
            elif query.data == "MembersButLeft":
                LMEMBERS -= 1
                await self.members_list(update, context)
            elif query.data == "projects_list":
                await self.projects_list(update, context)
            elif query.data == "ProjectsButRight":
                LPROJECT += 1
                await self.projects_list(update, context)
            elif query.data == "ProjectsButLeft":
                LPROJECT -= 1
                await self.projects_list(update, context)
            elif query.data == "login":
                await self.changeLogin(update, context)
            elif query.data == "company":
                await self.changeCompany(update, context)
            elif query.data == "password":
                await self.changePassword(update, context)
            elif "employeesBoardId" in query.data:
                await self.employeesBoardId(update, context, query.data)
            elif "ProjectId" in query.data:
                await self.projectId(update, context, query.data)
            elif query.data == "search_email":
                await self.searchEmploeesByEmail(update, context)
            elif query.data == "invite_people":
                await self.inviteEploeesByEmail(update, context)
            elif query.data == "deletUser":
                await self.deletUser(update, context)
            elif query.data == "giveAdminRule":
                await self.giveAdminRule(update, context)
            elif query.data == "takeAdminRule":
                await self.takeAdminRule(update, context)
            elif query.data == "project_create":
                await self.project_create(update, context)
            elif query.data == "ChangeUser":
                await self.ChangeUser(update, context)
            elif "deleate_projectId" in query.data:
                await self.edit_project(update=update, context=context, title=query.data, isDeleate=True)
            

                
            else:
                print("Неизвестнная кнопка")
        except:
            if self.state:
                await self.handle_message(update, context)
            else:
                print("Неизвестнная кнопка")

        # Add handling for other buttons if needed

    def run(self):
        self.updater.add_handler(CommandHandler("start", self.start))
        self.updater.add_handler(CallbackQueryHandler(self.button_handler))
        self.updater.add_handler(MessageHandler(filters.TEXT, self.button_handler))

 



        self.updater.run_polling()

