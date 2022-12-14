

def cut_down_photo_from_pets_json(json):
    try:
        list_of_pets = json["pets"]
    except KeyError:
        list_of_pets = []
        list_of_pets.append(json)
    for i in list_of_pets:
        if len(i["pet_photo"]) > 22:
            i["pet_photo"] = i["pet_photo"][:22]
    for i in list_of_pets:
        if len(i["age"])>4:
            i['age'] = i['age'][:4]
    for i in list_of_pets:
        if len(i["animal_type"])>10:
            i['animal_type'] = i['animal_type'][:10]
    for i in list_of_pets:
        if len(i["name"])>10:
            i['name'] = i['name'][:10]
    return json


def post_api_logger(func):
    def wrapper(*args, **kwargs):
        with open('log.txt', 'a', encoding="CP1251") as f:
            print("============= ЗАПРОС =============", file=f)
            print(f"Делаем POST запрос к {args[0]})", file=f)
            try:
                print(f"Параметры пути: {kwargs['params']}", file=f)
            except KeyError:
                print(f"Параметров пути нет.")
            print(f"Заголовки запроса: {kwargs['headers']}", file=f)
            data_repr = repr(kwargs['data'])
            print(f"Тело запроса: {data_repr}", file=f)
            value = func(*args, **kwargs)
            print("============= ОТВЕТ =============", file=f)
            response_code = repr(value)[10:-1]
            print(f"Код ответа на запрос - {response_code}", file=f)
            if value.status_code != 200:
                print(f"Тело ответа: {value.text}")
            else:
                try:
                    print(f"Тело ответа: {cut_down_photo_from_pets_json(value.json())}", file=f)
                except KeyError:
                    print(f"Тело ответа: {value.json()}", file=f)
            return value
    return wrapper


def get_api_logger(func):
    def wrapper(*args, **kwargs):
        with open('log.txt', 'a', encoding="CP1251") as f:
            print("============= ЗАПРОС =============", file=f)
            print(f"Делаем GET запрос к {args[0]}")
            try:
                print(f"Параметры пути: {kwargs['filter']}", file=f)
            except KeyError:
                print(f"Filter нет.")
            print(f"Заголовки запроса: {kwargs['headers']}", file=f)
            value = func(*args, **kwargs)
            print("============= ОТВЕТ =============", file=f)
            response_code = repr(value)
            print(f"Код ответа на запрос - {response_code}", file=f)
            if value.status_code != 200:
                print(f"Тело ответа: {value.text}", file=f)
            else:
                try:
                    print(f"Тело ответа: {cut_down_photo_from_pets_json(value.json())}", file=f)
                except KeyError:
                    print(f"Тело ответа: {value.json()}", file=f)
            return value

    return wrapper


def put_api_logger(func):
    def wrapper(*args, **kwargs):
        with open('log.txt', 'a', encoding="CP1251") as f:
            print("============= ЗАПРОС =============", file=f)
            print(f"Делаем PUT запрос к {args[0]}", file=f)
            print(f"Заголовки запроса: {kwargs['headers']}", file=f)
            print(f"Параметр пути запроса pet_id: {kwargs['path']}", file=f)
            data_repr = repr(kwargs['data'])
            print(f"Тело запроса: {data_repr}", file=f)
            value = func(*args, **kwargs)
            print("============= ОТВЕТ =============")
            response_code = repr(value)
            print(f"Код ответа на запрос - {response_code}", file=f)
            if value.status_code != 200:
                print(f"Тело ответа: {value.text}", file=f)
            else:
                try:
                    print(f"Тело ответа: {cut_down_photo_from_pets_json(value.json())}", file=f)
                except KeyError:
                    print(f"Тело ответа: {value.json()}", file=f)
            return value
    return wrapper

def delete_api_logger(func):
    def wrapper(*args, **kwargs):
        with open('log.txt', 'a', encoding="CP1251") as f:
            print("============= ЗАПРОС =============")
            print(f"Делаем DELETE запрос к {args[0]}", file=f)
            print(f"Заголовки запроса: {kwargs['headers']}", file=f)
            print(f"Параметр пути запроса pet_id: {kwargs['path']}", file=f)
            value = func(*args, **kwargs)
            print("============= ОТВЕТ =============")
            response_code = repr(value)
            print(f"Код ответа на запрос - {response_code}", file=f)
            return value
    return wrapper
