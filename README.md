# TelegramYtDl
A small and easy Telegram bot with the Python SAMT framework.
https://github.com/neunzehnhundert97/SAMT

All videos will be saved in /app/data

docker build -t tytbot .
docker run --name bot \
        -e telegramId="AllowdId1,AllowdId2,AllowdId3" \
        -e telegramBotToken="TOKEN" \
        tytbot
