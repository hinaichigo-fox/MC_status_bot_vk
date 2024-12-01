#бесконечный мониторинг сервера.
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
        while True:
            r = requests.get('https://api.mcstatus.io/v2/status/java/btrcaft.mcmem.ru')
            response = r.json()
            nicknames = []
            if response['players']['online'] >= 1:
                for player in response['players']['list']:
                    nickname = player['name_raw']
                    nicknames.append(nickname)  # Добавляем никнейм в список
                    #вместо 2000000002 ставьте свое
                self.send(2000000002, 'Количество игроков ' + str(response['players']['online']) + '. Ники: [' + ', '.join(nicknames) + ']')
            time.sleep(600)

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

