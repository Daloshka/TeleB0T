import time
import datetime
import os
import asyncio
import vk_api
import random
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
import database
import info

tokens = []

def get_tokens():
    tokens = database.get_active_tokes()
    return tokens

def minus_hour():
    database.minus_hour()

async def vk_farm(token):
    session = vk_api.VkApi(token= token)
    vk = session.get_api()
    value_time = 0
    groups_id_likes = info.groups_id  # vk взаимные лайки  https://vk.com/likeees https://vk.com/vzaimno_likess
    msg = info.messages
    while value_time < 3600:
        try:
            groups_id_likes = sorted(groups_id_likes, key=lambda A: random.random())
            for group_id in groups_id_likes:
                try:
                    session.method('wall.post', {'owner_id' : group_id, 'message' : msg[random.randint(0, len(msg))], 'random_id' : random.randint(1000, 99999)})
                    print(f"{token} Сообщение отправленно в группу {group_id}")
                    await asyncio.sleep(30)
                    value_time += 30
                except:
                    pass
        except:
            pass
        await asyncio.sleep(100)
        value_time += 100
        print(f"Прошло {value_time} секунд")
    value_time = 0
    get_tokens()
    print(f"Обнуление таймера {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

while True:
    try:
        tokens = get_tokens()
        minus_hour()
        funs = []
        for token in tokens:
            funs.append(asyncio.ensure_future(vk_farm(token)))  
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(asyncio.gather(*funs))
        time.sleep(60)
        print("repeat")
    except Exception as e:
        print(f"ERROR - {e}")


