# Getting Things Done (GTD) телеграм-бот
## Что такое GTD?

**GTD** - это система планирования задач, идей и проектов. Идея в том, чтобы завести несколько списков, у каждого из которых есть своя функция.

- Каждая задача или идея, пришедшая в голову, заносится в список **in**. На этом этапе не приветствуется думать - только записывать всё подряд.
- Требуется с определенной регулярностью перечитывать список **in** и распределять задачи оттуда по другим спискам (а неудачные идеи - удалять).
- Задачи, которые решено сделать в ближайшее время (сейчас, сегодня), заносятся в список **next actions**. Их должно быть немного и они должны быть одношаговые (иначе это задача для списка *projects*).
- Список **waiting for** - для задач, выполнение которых остановилось из-за внешних факторов (ждём ответа на письмо, ждём помощи друга и т.д.)
- Список **projects** - задачи, которые включают в себя много шагов. Нужно перечитывать этот список и для каждого проекта вносить его следующий шаг в список *next actions*.
- Список **some day/maybe**. Для желаемых задач, на которые сейчас нет времени.
- Список **reading list**. Чтобы не спамить в **next actions**. Чтобы в очереди читать что-то крутое, а не ~~считать манулов в чатике~~.
- Кроме списков есть также **календарь** - для задач, у которых *действительно* есть дедлайн. 


Хотя бы раз в неделю перечитывать все списки и перекидывать задачи между ними. Желательно всегда делать это ревью в одно и то же время.

Более подробно можно почитать [здесь](https://hamberg.no/gtd).

## Возможности бота
- Написать боту задачу - она будет внесена в **in**.
- Команда **/move** TASK_NUMBER FROM TO - для перемещения задач между списками.
- Команда **/done** TARK_NUMBER LIST.
- Запросить список задач (для каждого списка - своя команда). Список будет выведен в виде сообщения. Задачи пронумерованы, начиная с 1 - это и есть TASK_NUMBER для команд.
- Режим разбора задач:
    1. Пользователь выбирает список.
    2. Каждый шаг бот называет задачу из списка.
    3. Пользователь выбирает, куда переместить задачу.
    4. Можно завершить разбор досрочно.
- При добавлении в календарь просит указать дату.

### Дополнительно
- Запросить список задач, передав ключ **i**. Список будет показан в виде кнопок. Тык на задачу - открыть её описание. В режиме описания есть кнопки удалить, перенести в другой список.
- Помогает поддерживать инвариант проекта (для каждого есть задача в **next actions**). При добавлении проекта просит указать его первый шаг, который в **next actions**. Теперь этот шаг привязан к проекту. При его выполнении просит указать следующий шаг. 
- Напоминание о ревью списков.