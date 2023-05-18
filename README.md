![example workflow](https://github.com/t1m4k/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Проект Foodgram

### Описание
Благодаря проекту Foodgram пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в "Избранное" и скачивать в формате .txt список продуктов необходимый для приготовления выбранных блюд. 

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

Загрузите ингредиенты:

```
docker-compose exec web python manage.py load_ingredients
```

Создайте суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

По адресу http://158.160.19.213/api/docs/ подключена документация API.

Проект доступен по адресу: 158.160.19.213
Данные для доступа в admin-панель:

login: admin

password: admin


### Примеры запроса к API

```
/api/users/
```
```
POST: регистрация пользователя

{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "Qwerty123"
}
```
```
/api/users/me/
```
```
GET: получение профиля пользователя

{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": false
}
```
```
/api/recipes/
```
```
GET: получение списка рецептов

{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```
```
/api/ingredients/
```
```
GET: получение списка ингредиентов

[
  {
    "id": 0,
    "name": "Капуста",
    "measurement_unit": "кг"
  }
]
```
