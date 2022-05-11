From python:3.7-buster

WORKDIR /npa

COPY 62070088-bot.py .
COPY 62070088-netmiko.py .
COPY keyfile.py .
COPY requirement.txt .

RUN pip install -r requirement.txt

COPY . .

CMD ["python3", "62070088-bot.py"]