# README #

### Запуск локально

1.
```
virtualenv venv -p python3.5
source venv/bin/activate
git clone https://github.com/Marge-m/olx-parser/
cd olx-parser/olx_stats
```

В settings.py пишем токен бота (переменная TOKEN)

2. Устанавливаем ngrok (Качаем https://ngrok.com/download + unzip) и запускаем

```
./ngrok http 8080
```

Адрес вносим в settings.py в переменную NGROK.

3. Делаем webhook:

Заходим на 
https://api.telegram.org/bot{ТОКЕНБОТА}/setwebhook?url=https://{****}.ngrok.io/


```
4. pip install -r requirements.txt
```

5. Запускаем в 4х окнах терминала команды:

```
sudo rabbitmq-server

./prepare.sh

python -m celery -A olx_stats.celery  beat --loglevel INFO --scheduler=django_celery_beat.schedulers:DatabaseScheduler

python -m celery -A olx_stats.celery worker --loglevel INFO

```

6. Добавляем бота в Телеграмм  t.me/olxfeeds_bot

7. Команды - /start, /subscribe - подписаться

8. Подписываемся и наслаждаемся спамом. 

9. Команды для очистки Celery и RabbitMQ:

```
celery -A olx_stats purge 

rabbitmqadmin list queues name

rabbitmqadmin delete queue name='{DAT_NAME}'

ps aux|grep celery
ps aux|grep rabbit
sudo kill -9 {PID}
```
