from fastapi.testclient import TestClient
from fastapi import status
import _thread as th
import time
import random
import requests
from enum import Enum
import string


def random_mail(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


heroku_path = "https://secret-voldemort-back.herokuapp.com/api/"
local_path = "http://localhost:8000/api/"


is_local = True
basepath = local_path
if not is_local:
    basepath = heroku_path


class Bot():
    def __init__(
            self,
            nickname: str,
            email: str,
            password: str,
            token: str = ""):
        self.uid = 0
        self.nickname = nickname
        self.email = email
        self.password = password
        self.token = token
        self.active = False

    def register_bot(self):

        response = requests.post(basepath + "register/",
                                 headers={
                                     "Content-Type": "application/json"},
                                 json={
                                     "nickname": self.nickname,
                                     "email": self.email,
                                     "password": self.password})
        assert response.status_code == 201
        self.uid = response.json()

    def bot_login(self):
        response = requests.post(
            basepath + "login/",
            headers={
                "Content-Type": "application/json"},
            json={
                "email": self.email,
                "password": self.password})
        assert response.status_code == 200
        # tokens
        self.token = "Bearer " + response.json()["access_token"]
        return

    def bot_join_lobby(self, lobby_id: int):
        response = requests.post(
            basepath + "lobbies/{}/join/".format(lobby_id),
            headers={
                "Authorization": self.token})
        return response

    def bot_leave_match(self, game_id: int):
        response = requests.post(
            basepath + "lobbies/{}/leave/".format(game_id),
            headers={
                "Authorization": self.token})
        idle_bots.append(self)

    def bot_get_lobby_info(self, game_id: int):
        response = requests.get(
            basepath + "lobbies/{}".format(game_id),
            headers={
                "Authorization": self.token})

        return response

    def bot_get_game_info(self, game_id: int):
        response = requests.get(
            basepath + "games/{}/".format(game_id),
            headers={
                "Authorization": self.token})
        return response

    def bot_post_vote(self, game_id: int, vote: bool):
        response = requests.post(
            basepath + "games/{}/vote/".format(game_id),
            headers={
                "Content-Type": "application/json",
                "Authorization": self.token},
            json={
                "vote": vote})
        return response

    def bot_post_spell(self, game_id: int, target: int):
        response = requests.post(
            basepath + "games/{}/spell/".format(game_id),
            headers={
                "Content-Type": "application/json",
                "Authorization": self.token},
            json={
                "target": target})
        return response

    def bot_get_proclamation_cards(self, game_id: int):
        response = requests.get(
            basepath + "games/{}/proc/".format(game_id),
            headers={
                "Authorization": self.token})
        return response

    def bot_post_proclamation_cards(self,
                                    game_id: int,
                                    election: int,
                                    expelliarmus: bool):
        response = requests.post(
            basepath + "games/{}/proc/".format(game_id),
            headers={
                "Content-Type": "application/json",
                "Authorization": self.token},
            json={
                "election": election,
                "expelliarmus": expelliarmus})
        return response

    def bot_post_new_candidate(self, game_id: int, candidate_id: int):
        response = requests.post(
            basepath + "games/{}/director/{}/".format(
                game_id, candidate_id), headers={
                "Authorization": self.token})
        return response


idle_bots = []


def create_new_bot(nickname, email, password):

    bot = Bot(nickname=nickname, email=email, password=password)
    bot.register_bot()
    bot.bot_login()
    idle_bots.append(bot)
    return bot


def bot_random_logic(bot: Bot, game_id: int):
    start = time.time()
    while True:
        response = bot.bot_get_lobby_info(game_id=game_id)
        if response.status_code != 200:
            time.sleep(3)
            continue
        rjson = response.json()
        if not rjson["started"]:
            end = time.time()
            if (end -start) > 120:
                idle_bots.append(bot)
                break
            time.sleep(3)
            continue
        response = bot.bot_get_game_info(game_id=game_id)
        if response.status_code != 200:
            time.sleep(3)
            continue
        rjson = response.json()
        end = time.time()
        if ("end" in rjson.keys() and rjson["end"])or  (end - start) > 3600:
            idle_bots.append(bot)
            break
    
        targets = []
        for p in rjson["player_list"]:  # no implementado todavia
            if p["alive"]:  # and not p["crucied"] :
                targets.append(p["player_id"])
        if rjson["voting"]:
            bot.bot_post_vote(game_id=game_id, vote=True)
        if rjson["in_session"] and rjson["director_proclaimed"]:
            bot.bot_post_spell(game_id=game_id, target=random.choice(targets))
        if not rjson["in_session"] and not rjson["voting"]:
            bot.bot_post_new_candidate(game_id=game_id,
                                   candidate_id=random.choice(targets))
        bot.bot_login()
        if rjson["in_session"]:
            procls = bot.bot_get_proclamation_cards(game_id=game_id)
            if procls.status_code == 200:
                try:
                    bot.bot_post_proclamation_cards(game_id=game_id,
                                                    election=procls.json()[
                                                        0]["card_pos"],
                                                    expelliarmus=False)
                except BaseException:
                    print("error")
        time.sleep(3)

nombres = ["Harry", "Hermione", "Ron", "Draco", "Neville", "Bot", "Diegote"]
def add_bot_to_game(game_id):


    if 0 == len(idle_bots):
        nickname = random.choice(nombres) + str(random.randint(0, 10000))
        email = random_mail(8) + "@m.com"
        password = "12341234"
        create_new_bot(nickname, email, password)

    bot = idle_bots.pop()
    bot.bot_join_lobby(lobby_id=game_id)
    th.start_new_thread(bot_random_logic, (bot, game_id))
