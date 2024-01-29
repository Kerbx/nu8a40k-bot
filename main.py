import config
import database
import globals

import telebot.async_telebot


bot = telebot.async_telebot.AsyncTeleBot(config.BOT_TOKEN)
database.db.connect()


@bot.message_handler(commands=['start'])
async def send_start(message):
    await bot.reply_to(message, 'Приветствую.')
    

@bot.message_handler(commands=['register'])
async def register_user(message):
    for user in database.User.select():
        if user.id == str(message.from_user.id):
            return            
    
    admins = await bot.get_chat_administrators(message.chat.id)
    
    for admin in admins:
        if admin.user.id == message.from_user.id:
            USER_IS_ADMIN = True
            USER_RANK = -1
            USER_EXP = 20000
        else:
            USER_IS_ADMIN = False
            USER_RANK = 0
            USER_EXP = 0
            
    USER_ID = message.from_user.id
    USER_NAME = message.from_user.first_name
    USER_WARNS = 0
    USER_STATE = 0
    try:
        user = database.User.create(id=str(USER_ID),
                            name=str(USER_NAME),
                            rank=USER_RANK,
                            admin=USER_IS_ADMIN,
                            exp=USER_EXP,
                            warns=USER_WARNS,
                            state=USER_STATE)
    except Exception as e:
        print(e)
    
    
@bot.message_handler(commands=['user', 'info'])
async def get_user_info(message):
    for user in database.User.select():
        if message.reply_to_message:
            message.from_user.id = message.reply_to_message.from_user.id
        if user.id == str(message.from_user.id):
            info = f"""
            Имя: {user.name}
            Статус: {globals.USER_STATES.get(user.state)}
            Ранг: {globals.USER_RANKS.get(user.rank)}
            """
            await bot.send_message(message.chat.id, f'Информация о пользователе:\n{info}')


@bot.message_handler(func=lambda message: True)
async def send_any(message):
    print(message)
    await bot.send_message(message.chat.id, 'Гойда')
    

@bot.message_handler(content_types=['new_chat_members'])
async def send_welcome_message(message):
    print(message)
    await bot.send_message(message.chat.id, 'НОВАЯ ГОЙДА')
    
    
@bot.message_handler(content_types=['left_chat_member'])
async def send_fuck_off_message(message):
    print(message)
    await bot.send_message(message.chat.id, 'Без тебя нам будет лучше.')
    
    
import asyncio
asyncio.run(bot.polling())


