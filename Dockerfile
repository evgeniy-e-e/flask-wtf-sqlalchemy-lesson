FROM python:3.8

WORKDIR /usr/src/flask-lesson

# > Зачем отдельно копировать requirements.txt
# Поскольку Docker кеширует слои, то, при условии, что меняется только код приложения (без
# reqirements.txt), установка зависимостей заново производиться не будет, ведь изменения файлов
# не затронут этот слой.

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . ./
RUN echo http://localhost:5000/

EXPOSE 5000

