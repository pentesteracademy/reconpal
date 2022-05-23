#! /bin/bash
sed -i 's/TOKEN_API/'$TELEGRAM_BOT_TOKEN'/g' ./app.py
python3 ./app.py
