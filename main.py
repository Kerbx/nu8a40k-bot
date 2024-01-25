import config

import telebot.async_telebot


bot = telebot.async_telebot.AsyncTeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
async def send_start(message):
    await bot.reply_to(message, 'Приветствую.')
    

@bot.message_handler(func=lambda message: True)
async def send_any(message):
    await bot.reply_to(message, 'Гойда')
    
    
import asyncio
asyncio.run(bot.polling())


