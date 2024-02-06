import database


def check_user_get_new_rank(user):
    """
    Check if user get new rank on exp increase.

    @params:
        user:    - Requires  :   user to check (telebot.types.User)

    @return:
        None
    """
    if user.admin:
        print('ADMIN ALARM')
        return

    while True:
        print(f'curr: {user.exp}    |   need: {amount_of_exp_to_next_rank(user.rank)}   |   rank: {user.rank}')
        if user.exp >= amount_of_exp_to_next_rank(user.rank):
            user.rank += 1
            print(f'new rank: {user.rank}')
            try:
                user.save()

            except Exception as e:
                print(e)
        else:
            return


def amount_of_exp_to_next_rank(rank):
    """
    Returns the amount of experience needed to get to next rank

    @params:
        rank    - Required  :   current rank of user (Int)

    @return:
        int:    Amount of experience to get to next rank.
    """
    return int(round(1000 * 1.5 ** rank))


def change_user_experience(user_id, amount):
    """
    Change user's experience. Works only for admin.

    @params:
        user    - Required  :   user for changing (Str)
        amount  - Required  :   amount of experience to change. can be negative (Int)
    """
    print(database.User.select().where(database.User.id == user_id).get().exp)

    _user = database.User.select().where(database.User.id == user_id).get()
    _user.exp += amount

    try:
        _user.save()
        print(f'saved: {_user.exp}')
    except Exception as e:
        print(e)

    print(database.User.select().where(database.User.id == user_id).get().exp)

    check_user_get_new_rank(_user)

    
def print_progress_bar(user, iteration, total, prefix='', suffix='', decimals=0, length=15, fill='o'):
    """
    Call in a loop to create terminal progress bar
    @params:
        user        - Required  : uses to check if user is admin (telebot.types.User)
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)

    @return:
        str:    Progress bar of user's experience.
    """
    if not user.admin:
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        return f'\r{prefix} |{bar}| {percent}% {suffix}'
    else:
        return f'Больше совершенствоваться некуда.'


if __name__ == '__main__':
    print(amount_of_exp_to_next_rank(0))
    print(amount_of_exp_to_next_rank(2))
    print(amount_of_exp_to_next_rank(5))
    print(amount_of_exp_to_next_rank(10))
    