### Описание
Проект социальной сети foodgram.

###тестовый readme, будет дополнен после загрузки на сервер

### Как запустить проект:

Клонировать репозиторий:

```
git clone git@github.com:t1m4k/foodgram-project-react.git
```

Измените свою текущую рабочую директорию:

```
cd foodgram-project-react/infra
```

Создайте образ через Docker:

```
docker-compose up -d --build
```

Примените миграции:

```
docker-compose exec web python manage.py migrate
```
