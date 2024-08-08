import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command, CommandObject
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from aiogram.utils.deep_linking import create_start_link

from botHD.botHD import settings

bot = Bot(token=settings.BOT_TOKEN)
ADMIN_ID = int(settings.ADMIN_ID)
dispatcher = Dispatcher()


async def generate_start_link(our_bot: Bot):
    return await create_start_link(our_bot, settings.ACCESS_KEY)


@dispatcher.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Основные команды для работы:\n"
        "/register - команда для регистрации пользователя.\n"
        "/new_ticket - команда для создания новой заявки.\n"
        "/tickets - команда для проверки ваших заявок.\n"
        "/cancel - команда для отмены заявки.\n",
        parse_mode=ParseMode.HTML,
    )


@dispatcher.message(Command("start"))
async def cmd_start(message: types.Message, command: CommandObject):
    if command.args == settings.ACCESS_KEY:
        is_admin = message.chat.id == ADMIN_ID
        await set_commands(is_admin)
        await message.answer(f"{is_admin}")
        await message.answer(
            "Добро пожаловать в бот!\nДля продолжения пройдите регистрацию /register или воспользуйтесь "
            "помощью по командам /help."
        )
        return


async def set_commands(is_admin):
    if is_admin:
        commands = [
            BotCommand(command="register", description="Команда для регистрации пользователя"),
            BotCommand(command="new_ticket", description="Команда для создания новой заявки"),
            BotCommand(command="tickets", description="Команда для проверки ваших заявок"),
            BotCommand(command="cancel", description="Команда для отмены заявки"),
            BotCommand(command="complete", description="Команда для самостоятельного закрытия заявки"),
            BotCommand(command="help", description="Справка по командам"),
            BotCommand(command="tickets", description="Команда для создания новой заявки"),
            BotCommand(command="check_admin", description="Команда для проверки статуса Admin"),
            BotCommand(command="block", description="Команда для блокировки пользователя"),
            BotCommand(command="unblock", description="Команда для разблокировки пользователя"),
        ]
        await bot.set_my_commands(commands, BotCommandScopeChat(chat_id=ADMIN_ID))

    else:
        commands = [
            BotCommand(command="register", description="Команда для регистрации пользователя"),
            BotCommand(command="new_ticket", description="Команда для создания новой заявки"),
            BotCommand(command="tickets", description="Команда для проверки ваших заявок"),
            BotCommand(command="cancel", description="Команда для отмены заявки"),
            BotCommand(command="complete", description="Команда для самостоятельного закрытия заявки"),
            BotCommand(command="help", description="Справка по командам"),
        ]
        await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Бот запущен, приглашение работает по ссылке {await generate_start_link(bot)}",
    )
    await dispatcher.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] - %(filename)s:%(lineno)d #%(levelname)-s - %(name)s - %(message)s",
        filename="bot.log",
        filemode="w",
    )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Остановка сервера!")
