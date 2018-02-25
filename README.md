# README #

### Запуск локально

1.
```
virtualenv venv -p python3.5
source venv/bin/activate
git clone https://marge-m284@bitbucket.org/marge-m284/olx-parser.git
cd olx_stats
```

В settings.py пишем токен бота (переменная TOKEN)

2. Устанавливаем ngrok

```
./ngrok http 8080
```

Адрес вносим в settings.py в переменную NGROK.

3. Делаем вебхук:

Заходим на 
https://api.telegram.org/bot{ТОКЕНБОТА}/setwebhook?url=https://{****}.ngrok.io/

4. 
```
pip install -r requirements.txt
```

5. Запускаем в 4х окнах терминала команды:

```
sudo rabbitmq-server

python -m celery -A olx_stats.celery  beat --loglevel INFO --scheduler=django_celery_beat.schedulers:DatabaseScheduler

python -m celery -A olx_stats.celery worker --loglevel INFO

./prepare.sh
```

6. Добавляем бота в Телеграмм  t.me/olxfeeds_bot

7. Команды - /start, /subscribe - подписаться

8. Подписываемся и наслаждаемся спамом. 

9. Команды для очистки:

celery -A olx_stats purge 
rabbitmqadmin list queues name
rabbitmqadmin delete queue name='{DAT_NAME}'
