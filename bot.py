import telebot
import sqlite3
import os
import shutil


DELETE_CONFIRMATION_TEXT = 'Yes, I am totally sure.'
LIST_NAMES = ['in', 'next', 'waiting', 'projects', 'someday']
PARSE_ERROR_MSG = """Неверное использование команды!
"""
INSTRUCTIONS = {
    "del": """/done N LIST - удаляет задачу N из списка LIST""",
    "done": """/done N LIST - помечает задачу N из списка LIST выполненной"""
}

with open("token.txt", "r") as token_file:
    TOKEN = token_file.read()

TMP = os.path.join(os.getcwd(), 'tmp')

if not os.path.exists(TMP):
    os.mkdir('tmp')

con = sqlite3.connect('notes.db')
cur = con.cursor()
tables = cur.execute("SELECT name FROM sqlite_master").fetchall()

if ('notes', ) not in tables:
    cur.execute("CREATE TABLE notes(user_id, list, note, add_time, done)")
if ('menus', ) not in tables:
    cur.execute("CREATE TABLE menus(user_id, username, menu)")
con.commit()

bot = telebot.TeleBot(TOKEN, threaded=False)


def register(user):
    menu = "default"
    cur.execute("INSERT INTO menus VALUES(?, ?, ?)",
                (user.id, user.username,  menu))
    con.commit()
    return menu


def get_menu(user_id):
    exec = cur.execute("""SELECT menu
                        FROM menus
                        WHERE user_id = ?""",
                       (user_id, ))

    res = exec.fetchone()
    return None if res is None else res[0]


def get_user_id(user_id):
    exec = cur.execute("""SELECT user_id
                        FROM menus
                        WHERE username = ?""",
                       (user_id, ))

    res = exec.fetchone()
    return None if res is None else res[0]


def set_menu(user_id, menu):
    cur.execute("""UPDATE menus
                SET menu = ?
                WHERE user_id = ?""", (menu, user_id))
    con.commit()


def resetall(user_id):
    cur.execute("""DELETE FROM notes
                WHERE user_id = ?""", (user_id, ))
    con.commit()


def get_list(user_id, list_name):
    exec = cur.execute("""SELECT note, add_time, done
                        FROM notes
                        WHERE user_id = ? AND list = ? 
                        ORDER BY add_time""",
                       (user_id, list_name))
    return exec.fetchall()


def insert(user_id, list_name, note, timestamp):
    data = (user_id, list_name, note, timestamp, 0)
    cur.execute("INSERT INTO notes VALUES(?, ?, ?, ?, ?)", data)
    con.commit()


def delete(user_id, list_name=None, pos=None, values=None, timestamp=None):
    if timestamp is None:
        if values is None:
            values = get_list(user_id, list_name)
        item = values[pos - 1]
        timestamp = item[1]
    cur.execute("""DELETE 
                FROM notes
                WHERE user_id = ? AND add_time = ?""",
                (user_id, timestamp))
    con.commit()


def change_done(user_id, is_done, list_name=None, pos=None, values=None, timestamp=None):
    if timestamp is None:
        if values is None:
            values = get_list(user_id, list_name)
        timestamp = values[pos - 1][1]
    cur.execute("""UPDATE notes
                SET done = ?
                WHERE user_id = ? AND add_time = ?""", (is_done, user_id, timestamp))
    con.commit()


def create_archive(user_id, user_dir):
    files_dir = os.path.join(user_dir, "files")
    os.mkdir(files_dir)
    lst = get_list(user_id, "in")
    for num, note in enumerate(lst):
        file_name = os.path.join(files_dir, "file" + str(num) + ".txt")
        with open(file_name, 'w') as file:
            file.write(note[0])

    archive_name = os.path.join(user_dir, "export")
    shutil.make_archive(archive_name, 'zip', files_dir)
    shutil.rmtree(files_dir)
    return os.path.join(user_dir, "export.zip")


@bot.message_handler(commands=['start'])
def on_start(message):
    user = message.from_user
    if get_menu(user.id) is None:
        register(user)
    bot.reply_to(message, "Hello! I am GTD tracker!")  # TODO: Change message


@bot.message_handler(commands=['export'])
def on_start(message):
    user = message.from_user
    user_dir = os.path.join(TMP, "dir" + str(user.id))
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)

    archive_path = create_archive(user.id, user_dir)
    with open(archive_path, 'rb') as archive:
        bot.send_document(user.id, archive)
    os.remove(archive_path)


@bot.message_handler(commands=LIST_NAMES)
def receive_get_list(message):
    user_id = message.from_user.id
    command = message.text.split()[0][1:]
    res = get_list(user_id, command)
    values = [str(id + 1) + ". " + note[0] + ("✔" if note[2] else "")
              for id, note in enumerate(res)]
    bot.send_message(user_id, "IN:\n" + '\n'.join(values))


@bot.message_handler(commands=['resetall'])
def receive_resetall(message):
    user_id = message.from_user.id
    set_menu(user_id, "confirm_resetall")
    con.commit()
    bot.send_message(user_id, """Are you sure you want to delete ALL notes in EVERY list?

Send '""" + DELETE_CONFIRMATION_TEXT + """' to confirm you really want to delete all the info.""")


@bot.message_handler(commands=['done'])
def receive_done(message):
    user_id = message.from_user.id
    words = message.text.split()
    if len(words) < 3 or not words[1].isnumeric() or not words[2] in LIST_NAMES:
        cmd = words[0][1:]
        bot.send_message(user_id, PARSE_ERROR_MSG + INSTRUCTIONS[cmd])
        return
    pos = int(words[1])
    list_name = words[2]
    change_done(user_id, 1, list_name=list_name, pos=pos)
    bot.send_message(user_id, "Marked as done")


@bot.message_handler(commands=['del'])
def receive_delete(message):
    user_id = message.from_user.id
    words = message.text.split()
    if len(words) < 3 or not words[1].isnumeric() or not words[2] in LIST_NAMES:
        cmd = words[0][1:]
        bot.send_message(user_id, PARSE_ERROR_MSG + INSTRUCTIONS[cmd])
        return
    pos = int(words[1])
    list_name = words[2]
    delete(user_id, list_name=list_name, pos=pos)
    bot.send_message(user_id, "Deleted")


def share(receiver_id, sender_login, note):
    bot.send_message(receiver_id, "@" + sender_login +
                     " предложил вам задачу:\n" + note)


@bot.message_handler(commands=['share'])
def receive_share(message):
    user_id = message.from_user.id
    words = message.text.split()
    if len(words) < 4 or not words[1].isnumeric() or not words[2] in LIST_NAMES:
        cmd = words[0][1:]
        bot.send_message(user_id, PARSE_ERROR_MSG + INSTRUCTIONS[cmd])
        return
    receiver = words[3]
    receiver_id = get_user_id(receiver)
    if receiver_id is None:
        bot.send_message(
            user_id, "Не удалось поделиться задачей: @" + receiver + "не использует бота")
    else:
        share(receiver_id, message.from_user.username, "note")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    user = message.from_user
    user_id = user.id
    menu = get_menu(user_id)
    if menu is None:
        menu = register(user)

    if menu == "default":
        insert(user_id, "in", message.text, message.date)
        bot.reply_to(message, 'Задача добавлена в список "in"!')

    elif menu == "confirm_resetall":
        if message.text == DELETE_CONFIRMATION_TEXT:
            resetall(user_id)
        else:
            bot.send_message(user_id, "Удаление отменено")
        set_menu(user_id, "default")
        con.commit()


bot.infinity_polling()
