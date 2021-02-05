FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1
WORKDIR /auth_app
COPY requirements.txt /auth_app/requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /auth_app/

CMD ["python3", "/auth_app/app.py" ]
