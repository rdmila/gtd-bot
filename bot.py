import telebot
import sqlite3


con = sqlite3.connect('notes.db')
cur = con.cursor()
tables = cur.execute("SELECT name FROM sqlite_master").fetchall()
print(tables)
if ('notes', ) not in tables:
    cur.execute("CREATE TABLE notes(user, list, note, add_time)")
    con.commit()

with open("token.txt", "r") as token_file:
    token = token_file.read()

bot = telebot.TeleBot(token, threaded=False)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


def get_list(user_id, notes_list):
    exec = cur.execute("""SELECT note
                        FROM notes
                        WHERE user = ? AND list = ? 
                        ORDER BY add_time""",
                       (user_id, notes_list))
    return exec.fetchall()


@bot.message_handler(commands=['in'])
def send_welcome(message):
    user_id = message.from_user.id
    res = get_list(user_id, "in")
    values = [str(id + 1) + ". " + note[0] for id, note in enumerate(res)]
    bot.send_message(user_id, "IN:\n" + '\n'.join(values))


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    data = (message.from_user.id, "in", message.text, message.date)
    cur.execute("INSERT INTO notes VALUES(?, ?, ?, ?)", data)
    con.commit()
    bot.reply_to(message, "Задача добавлена в список \"in\"!")


bot.infinity_polling()
