import config
import database
import experience
import globals

import regex
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
            USER_EXP = -1
        else:
            USER_IS_ADMIN = False
            USER_RANK = 0
            USER_EXP = 0
            
    USER_ID = message.from_user.id
    USER_NAME = message.from_user.first_name
    USER_USERNAME = message.from_user.username
    USER_WARNS = 0
    USER_STATE = 0
    try:
        user = database.User.create(id=str(USER_ID),
                            name=str(USER_NAME),
                            rank=USER_RANK,
                            admin=USER_IS_ADMIN,
                            exp=USER_EXP,
                            username=USER_USERNAME,
                            warns=USER_WARNS,
                            state=USER_STATE)
    except Exception as e:
        print(e)
    
    
@bot.message_handler(commands=['user', 'info'])
async def get_user_info(message):
    if not database.User.select():
        await bot.send_message(message.chat.id, "_Пока что никто не зарегистрирован\.\.\._", "MarkdownV2")
        
    users = []
    for user in database.User.select():
        users.append(user.id)
    
    id = ''
    if message.reply_to_message:
        id = message.reply_to_message.from_user.id
        if message.reply_to_message.from_user.is_bot:
            await bot.send_message(message.chat.id, "_Боты не могут зарегистрироваться, о них нельзя получить информацию\!_", "MarkdownV2")
            return
        
    if str(message.from_user.id if not id else id) in users:
        user = database.User.select().where(database.User.id == str(message.from_user.id if not id else id)).get()
        info = f"""
        Имя: {user.name}
        Статус: {globals.USER_STATES.get(user.state)}
        Ранг: {globals.USER_RANKS.get(user.rank)}
        Текущее количество опыта: {user.exp}
        Прогресс опыта до следующего уровня:
        {experience.print_progress_bar(user.exp, experience.amount_of_exp_to_next_rank(user.rank))}
        """
        await bot.send_message(message.chat.id, f'Информация о пользователе:\n{info}')
    else:
        await bot.send_message(message.chat.id, "_Пользователю необходимо зарегистрироваться в боте для просмотра информации\._", "MarkdownV2")


@bot.message_handler(commands=['give_exp', 'exp', 'experience'])
async def give_experience(message):
    for user in database.User.select():
        if str(message.from_user.id) == user.id and user.admin:
            if '@' in message.text:
                usernames = regex.findall(r'@\w+', message.text)
                amount = regex.findall(r'\d+', message.text)
                for username in usernames:
                    _user = database.User.select().where(database.User.username == username[1:]).get()
                    experience.change_user_experience(_user.id, int(amount[0]))
                    return
            else:
                pass
        else:
            await bot.reply_to(message, '_Данная команда доступна только для администраторов\._', parse_mode='MarkdownV2')
            
            
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


