from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Application

TOKEN = "6500071185:AAEQ_ChvOVjhwJLaJxwBN9JDqDbrDhNrnyc"

class TelegramBot:
    def __init__(self):
        self.updater = Application.builder().token(TOKEN).build()
        
        self.users = {}  # Dictionary to store user information

    async def start(self, update, context):
        keyboard = [
            [InlineKeyboardButton("Авторизация", callback_data="auth")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Добро пожаловать! Выберите действие:", reply_markup=reply_markup)

    async def main_menu(self, update, context):
        keyboard = [
            [InlineKeyboardButton("Сменить пользователя", callback_data="auth")],
            [InlineKeyboardButton("Сменить компанию", callback_data="auth")],
            [InlineKeyboardButton("Сотрудники", callback_data="employees")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      text="Главное меню:",
                                      reply_markup=reply_markup)

    async def employees_menu(self, update, context):
        keyboard = [
            [InlineKeyboardButton("Поиск по email", callback_data="search_email")],
            [InlineKeyboardButton("Поиск по проекту", callback_data="search_project")],
            [InlineKeyboardButton("Дать/Забрать админку", callback_data="admin")],
            [InlineKeyboardButton("Удалить сотрудника", callback_data="delete")],
            [InlineKeyboardButton("Назад", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      text="Меню сотрудников:",
                                      reply_markup=reply_markup)

    async def button_handler(self, update, context):
        query = update.callback_query
        query.answer()

        if query.data == "auth":
            # Perform authorization logic
            query.message.reply_text("Вы вошли в систему.")
            await self.main_menu(update, context)
        elif query.data == "employees":
            await self.employees_menu(update, context)
        elif query.data == "back":
            await self.main_menu(update, context)
        # Add handling for other buttons if needed

    def run(self):
        self.updater.add_handler(CommandHandler("start", self.start))
        self.updater.add_handler(CallbackQueryHandler(self.button_handler))

        self.updater.run_polling()

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()