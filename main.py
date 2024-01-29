import config
import database

import telebot.async_telebot


bot = telebot.async_telebot.AsyncTeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
async def send_start(message):
    await bot.reply_to(message, 'Приветствую.')
    

@bot.message_handler(commands=['register'])
async def register_user(message):
    for user in database.User.select():
        if user.id == message.from_user.id:
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
    
    user = database.User(id=USER_ID, name=USER_NAME, rank=USER_RANK, admin=USER_IS_ADMIN, exp=USER_EXP, warns=USER_WARNS, state=USER_STATE)
    user.save()
    
    
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


