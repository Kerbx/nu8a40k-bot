import config
import database
import experience
import globals

import asyncio
import regex
import telebot.async_telebot


bot = telebot.async_telebot.AsyncTeleBot(config.BOT_TOKEN)
database.db.connect()


async def get_message_reply_id(message):
    id = ''
    if message.reply_to_message:
        id = message.reply_to_message.from_user.id
        if message.reply_to_message.from_user.is_bot:
            await bot.send_message(message.chat.id,
                                   "_Боты не могут зарегистрироваться, о них нельзя получить информацию\!_",
                                   "MarkdownV2")
            return None
        return id


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
            user_is_admin = True
            user_rank = -1
            user_exp = -1
        else:
            user_is_admin = False
            user_rank = 0
            user_exp = 0

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_username = message.from_user.username
    user_warns = 0
    user_state = 0
    try:
        database.User.create(id=str(user_id),
                             name=str(user_name),
                             rank=user_rank,
                             admin=user_is_admin,
                             exp=user_exp,
                             username=user_username,
                             warns=user_warns,
                             state=user_state)
    except Exception as e:
        print(e)


@bot.message_handler(commands=['user', 'info'])
async def get_user_info(message):
    # Send message if there is no one in database.
    if not database.User.select():
        await bot.send_message(message.chat.id, "_Пока что никто не зарегистрирован\.\.\._", "MarkdownV2")

    # Get all user's ids.
    users = []
    for user in database.User.select():
        users.append(user.id)

    # If message is a reply then we grab a user's id in reply to manage user.
    # Also send message if user is bot.
    id = await get_message_reply_id(message)

    # Grab user's id or id of user in reply and show info about him.
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
        # Send this if user isn't in database. 
        await bot.send_message(message.chat.id,
                               "_Пользователю необходимо зарегистрироваться в боте для просмотра информации\._",
                               "MarkdownV2")


@bot.message_handler(commands=['give_exp', 'exp', 'experience'])
async def give_experience(message):
    _is_admin = False
    for user in database.User.select():
        if str(message.from_user.id) == user.id and user.admin:
            _is_admin = True

    if _is_admin:
        if '@' in message.text:
            usernames = regex.findall(r'@\w+', message.text)
            amount = regex.findall(r'-?\d+', message.text)
            print(amount)
            for username in usernames:
                _user = database.User.select().where(database.User.username == username[1:]).get()
                experience.change_user_experience(_user.id, int(amount[0]))
                return
        else:
            id = await get_message_reply_id(message)
            users = []
            for _user in database.User.select():
                users.append(_user.id)

            if str(message.from_user.id if not id else id) in users:
                _user = database.User.select().where(database.User.id == message.from_user.id if not id else id).get()
                amount = regex.findall(r'-?\d+', message.text)
                experience.change_user_experience(message.from_user.id if not id else id, int(amount[0]))
            else:
                await bot.reply_to(message, 'Пользователь не зарегистрирован.')

    else:
        await bot.reply_to(message, '_Данная команда доступна только для администраторов\._',
                           parse_mode='MarkdownV2')


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


asyncio.run(bot.polling())
