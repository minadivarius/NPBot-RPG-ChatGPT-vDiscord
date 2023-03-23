FROM python:3.10-alpine

WORKDIR /npbot_discord

COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps build-base && \
    pip install -r requirements.txt && \
    apk del .build-deps

COPY npbot_discord.py .

COPY mycontext.py .

COPY mdtojson.py .

CMD ["python", "npbot_discord.py", "mycontext.py"].