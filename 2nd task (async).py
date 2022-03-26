'''
Приведите код из синхронного вида к ассинхронному
'''

import asyncio
import time
import requests as r


def fetch_url_data(url):
    '''
    Получение ответа от источника
    '''
    try:
        resp = r.get(url)
    except Exception as e:
        print(e)
    else:
        return  resp
    return


async def fetch_async(r):
    '''
    Отправка запросов к источнику
    '''
    url = "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p={}&region=1&room1=1&room2=1&type=4"
    tasks = []
    '''
    Очень полезной оказался следующий пост на stackoverflow:
    https://stackoverflow.com/questions/22190403/how-could-i-use-requests-in-asyncio
    
    А так же вот это обучающее видео:
    https://www.youtube.com/watch?v=t5Bo1Je9EmE
    
    Реализация проста, создаем задачи и ждем пока они все выполняться при помощи await
    '''
    loop = asyncio.get_event_loop()
    for i in range(r):
        tmp = url
        task = loop.run_in_executor(None,fetch_url_data,tmp.format(i))
        tasks.append(task)

    responses = await asyncio.gather(*tasks)
    return responses


if __name__ == '__main__':
    '''
    Точка входа в программу
    '''
    for i in range(100):
        start_time = time.time()
        # Не забываем использовать asyncio.run для вызова асинхронной функции (await для jupyter notebook)
        responses = asyncio.run(fetch_async(i))
        print(f'Получено {i} результатов запроса за {time.time() - start_time} секунд')


'''
  Сравним скорость обработки n запросов для синхронного и асинхронного метода
'''
def fetch_sync(r):
    '''
    Отправка запросов к источнику
    '''
    url = "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p={}&region=1&room1=1&room2=1&type=4"
    tasks = []
    for i in range(r):
        tmp = url
        task = fetch_url_data(tmp.format(i))
        tasks.append(task)
    responses = tasks
    return responses


t_sync = []
t_async = []
n = 20
for i in range(n):
    start_time = time.time()
    responses = asyncio.run(fetch_async(i))
    t_async.append(time.time() - start_time)
    print(f'Получено {i} результатов запроса за {time.time() - start_time} секунд')

for i in range(n):
    start_time = time.time()
    responses = fetch_sync(i)
    t_sync.append(time.time() - start_time)
    print(f'Получено {i} результатов запроса за {time.time() - start_time} секунд')

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6), dpi=80)

plt.plot(range(n), t_sync, label="Sync")
plt.plot(range(n), t_async, label="Async")
plt.title("Сравнение скорости обработки n запросов")
plt.xlabel('Количество запросов')
plt.ylabel('Время в секундах')
plt.xticks(range(0, n, 5))
plt.legend()
plt.show()