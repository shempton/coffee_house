# **Интернет-магазин кофейни**
![coffee](https://user-images.githubusercontent.com/60391451/220145980-e2106d58-44ff-49d6-a49e-138817e514ea.jpg)
## Для чего?
Это приложение написано с целью получить стартовые знания по фреймворку [Django](https://www.djangoproject.com/).  

Задача ставилась в рамках курса **_«Backend - разработка на фреймворке Django»_** от РЭУ им.Плеханова.

## Возможности приложения
+ CRUD операции над карточкой товара
+ Пагинация
+ Избранное
+ Корзина
+ Авторизация/Регистрация
+ Прописаны права доступа и разрешения
+ CRUD REST API 
+ Тесты
+ Запуск в контейнере Docker

## Запуск
```
git clone git@github.com:shempton/coffee_house.git
python -m venv env
source ./env/bin/activate
cd coffee_house/
pip install -r requirements.txt
./manage.py migrate
./manage.py runserver
```

*Используя Docker*
```
git clone git@github.com:shempton/coffee_house.git
cd coffee_house/
docker build . -t coffee-django:v1
docker run -d -p 8000:8000 coffee-django:v1
```

*Создание супер пользователя*
```
docker exec -it <container_id> python manage.py createsuperuser
```

## Идеи
+ ~~Запуск, используя Docker~~
+ Подключить платежную систему Stripe
+ JWT authentication
+ Деплой на сервер
