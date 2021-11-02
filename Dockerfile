# This is too much like saying "latest" for me to casually use it in a production pipeline, but that isn't what we have here
FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]