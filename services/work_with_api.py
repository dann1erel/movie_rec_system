import requests
import pandas as pd

data_w_descr = []

df = pd.read_csv('./data/kp_cut.csv')
ids = df['movie_id'].tolist()

list = [] # смотри в блокноте)))

API_KEY = list[0]
i = 0
j = 0

for id in ids:
    i += 1
    url = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}'
    headers = {
        'X-API-KEY': API_KEY,
        'Content-Type': 'application/json',
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверяем статус ответа
        data = response.json()  # Преобразуем ответ в JSON
        print(data)  # Выводим полученные данные
    except requests.exceptions.RequestException as err:
        print(f'Произошла ошибка при запросе: {err}')

    data_w_descr.append({'movie_id': id, 'description': data['description'], 'poster': data['posterUrl']})

    if i == 500:
        print('-' * 15)
        j += 1
        API_KEY = list[j]
        df_w_descr = pd.DataFrame(data_w_descr)
        df_w_descr.to_csv('./data/kp_id_descr.csv')
        i = 0

df_w_descr = pd.DataFrame(data_w_descr)
df_w_descr.to_csv('./data/kp_id_descr.csv')