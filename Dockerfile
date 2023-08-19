# Используйте базовый образ Python
FROM python:3

# Установите рабочую директорию внутри контейнера
WORKDIR /code

# Копируйте зависимости проекта
COPY ./requirements.txt .

# Установите зависимости
RUN pip install -r requirements.txt

# Копируйте весь проект внутрь контейнера
COPY . .