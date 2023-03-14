FROM python:3

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8888

CMD [ "python", "app.py"]