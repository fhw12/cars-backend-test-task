# cars-backend-test-task

## Установка
```shell
pip3 install
```

## Использование API
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
let car_id = 5; // Для примера id автомобиля = 5
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
let car_id = 5; // Для примера id автомобиля = 5
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
let username = ""; // имя пользователя
let password = ""; // пароль
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
let username = ""; // имя пользователя
let password = ""; // пароль
fetch('http://127.0.0.1:8000/api/cars/14/', {
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
let username = ""; // имя пользователя
let password = ""; // пароль
fetch('http://127.0.0.1:8000/api/cars/14/', {
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
let car_id = 1; // id публикации под которой будет дабавлен комментарий
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
```