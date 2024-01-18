"""Сервер Telegram бота, запускаемый непосредственно"""
# Подгрузка библиотек
import logging
import os
from dotenv import load_dotenv
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

import db
import exceptions
import expenses
from categories import Categories


# Подгружаем файл с настройками (переменные окружения)
load_dotenv()

logging.basicConfig(level=logging.INFO)
# Подгружаем ключ нашего бота
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

# Запуск бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Инструкции для приветственных сообщений
@dp.message_handler(commands=['start', 'help', 'alesya'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    if not (expenses.check_budget_exists(message.from_user.id)):
        db.insert("budget", {"user_id": message.from_user.id, "daily_limit": 700})
    await message.answer(
        "Бот для учёта финансов\n\n"
        "Добавить расход: 250 такси\n"
        "Сегодняшняя статистика: /today\n"
        "За текущий месяц: /month\n"
        "Последние внесённые расходы: /expenses\n"
        "Категории трат: /categories\n\n"
        "Установить дневной лимит: /limit *число*\n"
        f"Текущий дневной лимит: {expenses._get_budget_limit(message.from_user.id)} руб.")


@dp.message_handler(commands=['limit'])
async def set_budget_limit(message: types.Message):
    command = message.get_args()
    if command is None:
        await message.answer(
            "Ошибка: не введено число.\nПожалуйста, введите команду в формате: /limit число"
        )
    else:
        try:
            dlimit = int(command)
            expenses._set_budget_limit(dlimit, message.from_user.id)
            await message.answer(
                "Дневной лимит установлен.\n"
                f"Текущий дневной лимит: {expenses._get_budget_limit(message.from_user.id)} руб.")
        except ValueError:
            await message.answer(
                "Ошибка: неправильный формат команды.\n"
                "Пожалуйста, введите команду в формате: /limit число\n"
                f"Текущий дневной лимит: {expenses._get_budget_limit(message.from_user.id)}"
            )


# Инструкции по удалению траты
@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Удаляет одну запись о расходе по её идентификатору"""
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    answer_message = "Удалил"
    await message.answer(answer_message)


# Вывод категорий
@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    """Отправляет список категорий расходов"""
    categories = Categories().get_all_categories()
    answer_message = "Категории трат:\nБазовые:"

    for c in categories:
        if c.is_base_expense:
            answer_message += "\n🟢 " + c.name + ' (' + ", ".join(c.aliases) + ')'
    answer_message += "\nВторостепенные:"
    for c in categories:
        if not (c.is_base_expense):
            answer_message += "\n🔴 " + c.name + ' (' + ", ".join(c.aliases) + ')'
    # answer_message = ("Категории трат:\n\n* " +
    # ("\n* ".join([c.name+' ('+", ".join(c.aliases)+')' for c in categories])))
    await message.answer(answer_message)


# Вывод сегодняшней статистики
@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    answer_message = expenses.get_today_statistics(message.from_user.id)
    await message.answer(answer_message)


# Вывод месячной статистики
@dp.message_handler(commands=['month'])
async def month_statistics(message: types.Message):
    """Отправляет статистику трат текущего месяца"""
    answer_message = expenses.get_month_statistics(message.from_user.id)
    await message.answer(answer_message)


# Вывод последних расходов
@dp.message_handler(commands=['expenses'])
async def list_expenses(message: types.Message):
    """Отправляет последние несколько записей о расходах"""
    last_expenses = expenses.last(message.from_user.id)
    if not last_expenses:
        await message.answer("Расходы ещё не заведены")
        return
    '''
    last_expenses_rows = [
        f"{expense.amount} руб. на {expense.category_name} — нажми "
        f"/del{expense.id} для удаления"
        for expense in last_expenses]
    '''
    last_expenses_rows = []
    cat = []
    for i in Categories().get_all_categories():
        if i.is_base_expense == True:
            cat.append(i.name)
    for expense in last_expenses:
        if expense.category_name in cat:
            last_expenses_rows.append(
                f"🟢 {expense.amount} руб. на {expense.category_name} — нажми /del{expense.id} для удаления")
        else:
            last_expenses_rows.append(
                f"🔴 {expense.amount} руб. на {expense.category_name} — нажми /del{expense.id} для удаления")

    answer_message = "Последние сохранённые траты:\n\n " + "\n\n " \
        .join(last_expenses_rows)
    await message.answer(answer_message)


# Добавление нового расхода
@dp.message_handler()
async def add_expense(message: types.Message):
    """Добавляет новый расход"""
    try:
        expense = expenses.add_expense(message)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Добавлены траты {expense.amount} руб на {expense.category_name}.\n\n"
        f"{expenses.get_today_statistics(message.from_user.id)}")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
