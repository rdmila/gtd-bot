DELETE_CONFIRMATION_TEXT = "Yes, I am totally sure."

ASK_DELETE = """Are you sure you want to delete ALL notes in EVERY list?

Send '{}' to confirm you really want to delete all the info.""".format(DELETE_CONFIRMATION_TEXT)

ALL_DELETED = "Все задачи удалены"

DELETION_CANCELLED = "Удаление отменено"

PARSE_ERROR_MSG = "Неверное использование команды!"

INSTRUCTIONS = {
    "del": """/done N LIST - удаляет задачу N из списка LIST""",
    "done": """/done N LIST - помечает задачу N из списка LIST выполненной"""
}

HELP_MSG = """Type / to see command list. 
Any message without a command would be interpreted as note and added to "in" list."""

START_MSG = "Hi!\n" + HELP_MSG

TASK_ADDED = 'Задача добавлена в список {}!'

TASK_SHARE_NOTIFICATION = "@{username} предложил вам задачу:\n"

SHARE_WITH_UNACCESSIBLE = "Не удалось поделиться задачей: @{} не использует бота"

TASK_MOVED = "Задача перемещена в список "

TASK_DELETED = "Задача удалена"

TASK_DONE = "Задача выполнена!"

