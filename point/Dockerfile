FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1
WORKDIR /point_app
COPY requirements.txt /point_app/requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /point_app/

CMD ["python3", "/point_app/app.py" ]
