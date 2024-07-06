FROM python:3.12-slim


WORKDIR /app/src

COPY . /app

COPY requirements.txt /app/src

RUN pip install --no-cache-dir -r /app/src/requirements.txt

ENV BOT_TOKEN=BOT_TOKEN

RUN ls -la /app/src

CMD ["python", "main.py"]