# базовый образ
FROM python:3.10-slim

# устанавливаем внутри pipenv
RUN pip install pipenv

# определяем рабочую директорию для запуска приложения
WORKDIR /my_app

# копируем в нее файлы с зависимостями
COPY ["Pipfile", "Pipfile.lock", "./"]

# устанавливавем библиотеки (само окружение создавать не нужно, так как docker и так изолирован)
RUN pipenv install --system --deploy

# fix for lgbm OSError inside docker container
# https://stackoverflow.com/questions/55036740/lightgbm-inside-docker-libgomp-so-1-cannot-open-shared-object-file
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get -y install curl
RUN apt-get install libgomp1

# копируем файлы приложения
COPY ["my_service.py", "model.cbm", "./"]

# определяем порт для запуска
EXPOSE 666

# команда для запуска приложения
# ENTRYPOINT [ "gunicorn", "-b 0.0.0.0:9696", "predict:app" ]
ENTRYPOINT [ "python3", "my_service.py" ]