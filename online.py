#мониторинг по команде кто онлайн
import requests
import random
import time
import json
import multitasking
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import threading

token = ['токен']
group_id = [айди]

class bot:
    def __init__(self, token, group_id):
        self.token = token
        self.group_id = group_id

    def start(self): #стартовая часть
        vk_session = vk_api.VkApi(token=self.token)
        self.vk = vk_session.get_api()
        longpoll = VkBotLongPoll(vk_session, self.group_id)
        print('включен!')
        for event in longpoll.listen():  # прослушка лп
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = event.message.text.lower()
                msg_id = event.obj['message']['conversation_message_id']
                id = event.message["peer_id"]
                us_id = event.obj['message']['from_id']
                if msg in ('кто онлайн', 'кто онлайн?'): #вместо btcraft.mcmem.ru ставьте адрес своего сервера 
                    r = requests.get('https://api.mcstatus.io/v2/status/java/btcraft.mcmem.ru')
                    response = r.json()
                    nicknames = []
                    if response['players']['online'] >= 1:
                        for player in response['players']['list']:
                            nickname = player['name_raw']
                            nicknames.append(nickname)
                        self.send(id, 'Количество игроков ' + str(response['players']['online']) + '. Ники: [' + ', '.join(nicknames) + ']')
                    else:
                        self.send(id, 'сейчас онлайн 0 людей')


    def send(self, id, text): #функа отправки текста
        self.vk.messages.send(peer_id=id, message=text,random_id=0)


@multitasking.task
def recursion(token, group_id):
    while True:
        try:
            a = bot(token, group_id)
            a.start()

        except Exception as err:
            print(err)

for token, group_id in zip(token, group_id):
    recursion(token, group_id)

