# cars-backend-test-task

## Установка
### Скачайте исходный код проекта
Это можно сделать через git или загрузить как zip архив через интерфейс github.
Пример загрузки через git:
```shell
git clone https://github.com/fhw12/cars-backend-test-task
```

### Необходимо перейти в каталог проекта
```shell
cd путь_к_проекту/cars-backend-test-task
```

### Установка необходимых библиотек (Linux)
```shell
pip3 install -r requirements.txt
```
Для Windows необходимо использовать команду pip вместо pip3.

### Запуск проекта
Необходимо провести миграции базы данных:
```shell
python3 manage.py migrate
```

Запуск проекта:
```shell
python3 manage.py runserver
```
Для Windows необходимо использовать команду python вместо python3.


## Использование API
Примеры представлены на языке программирования JavaScript.
Для проверки работы API перейдите на сайт с машинами и откройте консоль разработчика внутри браузера (F12 или через контекстное меню при правом клике мыши).
Для авторизации (где требутся) необходимо передавать имя и пароль пользователя в заголовке запроса (В примерах указано как именно). Перед тем как использовать авторизацию необходимо создать учетную запись пользователя (через сайт).
Для некоторых запросов необходимо использовать body для передачи данных (В примерах указано как именно).


### Получение всех машин:
```javascript
fetch('http://127.0.0.1:8000/api/cars/', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    },
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.log(error));
```

### Информация о конкретном автомобиле:
```javascript
car_id = 1; // Для примера id автомобиля = 1
fetch(`http://127.0.0.1:8000/api/cars/${car_id}`, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    },
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.log(error));
```

### Получение комментариев под конкретной публикацией об автомобиле:
```javascript
car_id = 1; // Для примера id автомобиля = 1
fetch(`http://127.0.0.1:8000/api/cars/${car_id}/comments/`, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    },
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.log(error));
```

### Добавить публикацию об автомобиле:
```javascript
username = ""; // имя пользователя
password = ""; // пароль
fetch('http://127.0.0.1:8000/api/cars/', {
    method: 'POST',
    headers: {
        'Authorization': 'Basic ' + btoa(`${username}:${password}`),
        'Content-Type': 'application/json',
    },

    body: JSON.stringify({
        "make": "SportCar",
        "model": "X10",
        "year": 2020,
        "description": "Cool Car"
    })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.log(error));
```

### Обновить публикацию об автомобиле (Доступно только автору публикации):
```javascript
username = ""; // имя пользователя
password = ""; // пароль
car_id = 1; // id обновляемой публикации
fetch(`http://127.0.0.1:8000/api/cars/{car_id}/`, {
    method: 'PUT',
    headers: {
        'Authorization': 'Basic ' + btoa(`${username}:${password}`),
        'Content-Type': 'application/json',
    },

    body: JSON.stringify({
        "make": "MyCar",
        "model": "Lightning3000",
        "year": 2024,
        "description": "Really cool car for its price"
    })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.log(error));
```

### Удалить публикацию об автомобиле (Доступно только автору публикации):
```javascript
username = ""; // имя пользователя
password = ""; // пароль
car_id = 1; // id удаляемой публикации
fetch(`http://127.0.0.1:8000/api/cars/${car_id}/`, {
    method: 'DELETE',
    headers: {
        'Authorization': 'Basic ' + btoa(`${username}:${password}`),
        'Content-Type': 'application/json',
    },
})
```

### Добавление комментария к публикации:
```javascript
let username = ""; // имя пользователя
let password = ""; // пароль
let car_id = 1; // id публикации под которой будет добавлен комментарий
fetch(`http://127.0.0.1:8000/api/cars/${car_id}/comments/`, {
    method: 'POST',
    headers: {
        'Authorization': 'Basic ' + btoa(`${username}:${password}`),
        'Content-Type': 'application/json',
    },

    body: JSON.stringify({
        "content": "Test comment via API",
    })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.log(error));
```