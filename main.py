import config

import telebot.async_telebot


bot = telebot.async_telebot.AsyncTeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
async def send_start(message):
    await bot.reply_to(message, 'Приветствую.')
    

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


