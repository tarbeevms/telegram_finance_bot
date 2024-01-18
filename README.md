Телеграмм бот для учета финансов на базе `aiogram`. Бот написан мною в качестве проектной работы одного из моих учеников на репетиторстве, поэтому имеет ограниченный и довольно простой функционал.


## Запуск
1. Для запуска пропишите параметр `TELEGRAM_API_TOKEN` своео бота в файл `.env` (Пример есть в файле `.env_example`) 
2. Запустите файл `start.bat`

## Команды бота
1. Команда `/start` - выводит приветственное сообщение

![image](https://github.com/tarbeevms/telegram_finance_bot/assets/145577110/1e05ae0c-3b35-4135-bc4c-670422a193c0)


2. Команда `/categories` - выводит список категорий трат с разделением на базовые и второстепенные расходы (категориии создаются и записываются в БД в createdb.sql)

![image](https://github.com/tarbeevms/telegram_finance_bot/assets/145577110/2c2d0109-5cb1-432e-be93-bab96734bdb6)

3. Команда добавления расходов. Пример: `250 такси`

![image](https://github.com/tarbeevms/telegram_finance_bot/assets/145577110/a9fc37ef-0f67-44a6-873c-d093995f368e)

![image](https://github.com/tarbeevms/telegram_finance_bot/assets/145577110/e9e5a063-0e5c-4aa9-9a31-7de41cacd96e)

4. Команда `/month` - выводит статистику расходов в текущем месяце с подсчётом лимита на текущее число месяца

![image](https://github.com/tarbeevms/telegram_finance_bot/assets/145577110/c6e387ac-b48f-43ea-b41a-3b14fbdc8c3d)

4. Команда `/today` - выводит статистику расходов за сегодня

![image](https://github.com/tarbeevms/telegram_finance_bot/assets/145577110/fc4320d9-2ead-4908-ab89-bc2430c1638c)

5. Команда `/expenses` - выводит последние добавленные траты пользователя с выводом категории и подсветкой базовых/второстепенных расходов (красные - второстепенные, зелёный - базовые). Позволяет удалять последние добавленные расходы.

![image](https://github.com/tarbeevms/telegram_finance_bot/assets/145577110/7cf1ae91-a656-41f4-81a9-6598d5e78bbb)

6. Команда `/limit` - позволяет устанавливать ежедневный лимит трат.

![image](https://github.com/tarbeevms/telegram_finance_bot/assets/145577110/ec6967c3-12e2-466c-a433-6460da73658a)

