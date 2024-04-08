from telegram import InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Application
from keybord import KMain_menu, KEmployees_menu, start, KAuthorization_menu, KBoard_menu, KProject_menu
from createKeyboard import Kmembers_list, Kprojects_list

TOKEN = "6500071185:AAEQ_ChvOVjhwJLaJxwBN9JDqDbrDhNrnyc"
LMEMBERS = 0
LPROJECT = 0

class TelegramBot:
    def __init__(self):
        self.updater = Application.builder().token(TOKEN).build()
        
        self.users = {}  # Dictionary to store user information

    async def start(self, update, context):
        reply_markup = InlineKeyboardMarkup(KAuthorization_menu)
        try:
            await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                                message_id=update.callback_query.message.message_id,
                                                text="Добро пожаловать! Выберите действие:", 
                                                reply_markup=reply_markup)
        except AttributeError:
            await update.message.reply_text("Добро пожаловать! Выберите действие:", reply_markup=reply_markup)


    async def main_menu(self, update, context):
        reply_markup = InlineKeyboardMarkup(KMain_menu)
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      text="Главное меню:",
                                      reply_markup=reply_markup)

    async def employees_menu(self, update, context):
        reply_markup = InlineKeyboardMarkup(KEmployees_menu)
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
        
    async def board_menu(self, update, context):
        reply_markup = InlineKeyboardMarkup(KBoard_menu)
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      text="Меню досок:",
                                      reply_markup=reply_markup)
        
    async def members_list(self, update, context):

        reply_markup = InlineKeyboardMarkup(Kmembers_list(LMEMBERS))
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      text="Список сотрудников:",
                                      reply_markup=reply_markup)
        
    async def projects_list(self, update, context):

        reply_markup = InlineKeyboardMarkup(Kprojects_list(LPROJECT))
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      text="Список проектов:",
                                      reply_markup=reply_markup)

    async def button_handler(self, update, context):
        global LMEMBERS
        global LPROJECT
        query = update.callback_query
        query.answer()

        if query.data == "auth":
            # Perform authorization logic
            query.message.reply_text("Вы вошли в систему.")
            await self.start(update, context)
        elif query.data == "main_menu":
            await self.main_menu(update, context)
        elif query.data == "employees":
            await self.employees_menu(update, context)
        elif query.data == "projects":
            await self.project_menu(update, context)
        elif query.data == "boards":
            await self.employees_menu(update, context)
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
            
        else:
            print("Неизвестнная кнопка")

        # Add handling for other buttons if needed

    def run(self):
        self.updater.add_handler(CommandHandler("start", self.start))
        self.updater.add_handler(CallbackQueryHandler(self.button_handler))

        self.updater.run_polling()

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()