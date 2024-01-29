import database


def amount_of_exp_to_next_rank(rank):
    """
    Returns the amount of experience needed to get to next rank

    @params:
        rank    - Required  :   current rank of user (Int)

    @return:
        int:    Amount of experience to get to next rank.
    """
    return int(round(1000 * 1.5 ** (rank)))


def change_user_experience(user_id, amount):
    """
    Change user's experience. Works only for admin.

    @params:
        user    - Required  :   user for changing (Str)
        amount  - Required  :   amount of experience to change. can be negative (Int)
    """
    _user = database.User.select().where(database.User.id == user_id).get()
    _user.exp += amount
    try:
        _user.save()
    except Exception as e:
        print(e)
    
    
def print_progress_bar(iteration, total, prefix = '', suffix = '', decimals = 0, length = 25, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        
    @return:
        str:    Progress bar of user's experience.
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    return (f'\r{prefix} |{bar}| {percent}% {suffix}')


if __name__ == '__main__':
    print(amount_of_exp_to_next_rank(0))
    print(amount_of_exp_to_next_rank(2))
    print(amount_of_exp_to_next_rank(5))
    print(amount_of_exp_to_next_rank(10))
    