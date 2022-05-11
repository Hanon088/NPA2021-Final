From python:3.7-buster

WORKDIR /npa

COPY 62070088-bot.py .
COPY 62070088-netmiko.py .
COPY keyfile .

RUN pip install requirement.txt

COPY . .

CMD ["python3", "62070088-bot.py"]