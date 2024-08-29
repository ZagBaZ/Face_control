# Контроль прихода сотрудников с отправкой сообщения в Telegram

## OpenCV + face_recognition + sqlite3 + telegram_bot

![example](https://github.com/ZagBaZ/Face_control/blob/main/images/example.jpg)

### Описание

Используя ip-камеру, распознаем сохраненые лица, записываем в БД информацию о дате и времени прихода на работу. В заданный час приходит сообщение в телеграм во сколько пришёл каждый сотрудник.

![db](https://github.com/ZagBaZ/Face_control/blob/main/images/database.jpg)

![telegram](https://github.com/ZagBaZ/Face_control/blob/main/images/telegram.jpg)

### Установка, настройка и запуск
Для работы требуется установить microsoft visual c++  
далее устанавливаем зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

переменные:  
```
TOKEN - токен телеграм бота
USER_BOT - твой id в телеграме
HOUR_MAX - до скольки часов записывать вновь прибывших работников
TIME_SEND_MESSAGE - во сколько отправить сообщение в телеграм
```
