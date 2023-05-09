import telebot
import os
from database import DataBase
from archiver import create_archive
from message_consts import *
from plot import create_done_plot

LIST_NAMES = ['in', 'next', 'wait', 'projects', 'someday']

base = DataBase()

TMP = os.path.join(os.getcwd(), 'tmp')
if not os.path.exists(TMP):
    os.mkdir('tmp')

with open("token.txt", "r") as token_file:
    TOKEN = token_file.read()

bot = telebot.TeleBot(TOKEN, threaded=False)


@bot.message_handler(commands=['start'])
def on_start(message):
    user = message.from_user
    if base.get_menu(user.id) is None:
        base.register(user)
    bot.reply_to(message, START_MSG)


@bot.message_handler(commands=['export'])
def on_export(message):
    user = message.from_user
    user_dir = os.path.join(TMP, "dir" + str(user.id))
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)

    archive_path = create_archive(user_dir, base.get_list(user.id, "in"))
    with open(archive_path, 'rb') as archive:
        bot.send_document(user.id, archive)
    os.remove(archive_path)


@bot.message_handler(commands=LIST_NAMES)
def on_get_list(message):
    user = message.from_user
    command = message.text.split()[0][1:]
    res = base.get_list(user.id, command)
    values = [str(id + 1) + ". " + note[0] + ("✔" if note[2] else "")
              for id, note in enumerate(res)]
    bot.send_message(user.id, command + ":\n\n" + '\n'.join(values))


@bot.message_handler(commands=['resetall'])
def receive_resetall(message):
    user_id = message.from_user.id
    base.set_menu(user_id, "confirm_resetall")
    bot.send_message(user_id, ASK_DELETE)


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
    base.set_done_time(user_id, message.date, list_name=list_name, pos=pos)
    bot.send_message(user_id, TASK_DONE)


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
    base.delete_note(user_id, list_name=list_name, pos=pos)
    bot.send_message(user_id, TASK_DELETED)


@bot.message_handler(commands=['move'])
def receive_delete(message):
    user_id = message.from_user.id
    words = message.text.split()
    if len(words) < 4 or not words[1].isnumeric() or not words[2] in LIST_NAMES or not words[3] in LIST_NAMES:
        cmd = words[0][1:]
        bot.send_message(user_id, PARSE_ERROR_MSG + INSTRUCTIONS[cmd])
        return
    pos = int(words[1])
    list_a = words[2]
    list_b = words[3]
    lst = base.get_list(user_id, list_a)
    note = lst[pos - 1][0]
    base.delete_note(user_id, list_name=list_a, pos=pos)
    base.insert_note(user_id, list_b, note, message.date)
    bot.send_message(user_id, TASK_MOVED + list_b)


def share(receiver_id, sender_login, note):
    bot.send_message(
        receiver_id, TASK_SHARE_NOTIFICATION.format(username=sender_login) + note)


@bot.message_handler(commands=['share'])
def receive_share(message):
    user_id = message.from_user.id
    words = message.text.split()
    if len(words) < 4 or not words[1].isnumeric() or not words[2] in LIST_NAMES:
        cmd = words[0][1:]
        bot.send_message(user_id, PARSE_ERROR_MSG + INSTRUCTIONS[cmd])
        return
    receiver = words[3]
    receiver_id = base.get_user_id(receiver)
    if receiver_id is None:
        bot.send_message(
            user_id, SHARE_WITH_UNACCESSIBLE.format(receiver))
    else:
        list_name = words[2]
        pos = int(words[1])
        lst = base.get_list(user_id, list_name)
        note = lst[pos - 1][0]
        share(receiver_id, message.from_user.username, note)


@bot.message_handler(commands=['stats'])
def on_get_stats(message):
    user = message.from_user

    user_dir = os.path.join(TMP, "dir" + str(user.id))
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)

    notes = base.get_all_notes(user.id)

    plot_path = create_done_plot(notes, user_dir)
    with open(plot_path, 'rb') as plot_picture:
        bot.send_document(user.id, plot_picture)
    os.remove(plot_path)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    user = message.from_user
    user_id = user.id
    menu = base.get_menu(user_id)
    if menu is None:
        menu = base.register(user)

    if menu == "default":
        base.insert_note(user_id, "in", message.text, message.date)
        bot.reply_to(message, TASK_ADDED.format('in'))

    elif menu == "confirm_resetall":
        if message.text == DELETE_CONFIRMATION_TEXT:
            base.reset_all_notes(user_id)
            bot.send_message(user_id, ALL_DELETED)
        else:
            bot.send_message(user_id, DELETION_CANCELLED)
        base.set_menu(user_id, "default")


bot.infinity_polling()
