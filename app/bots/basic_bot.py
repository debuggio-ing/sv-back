from fastapi.testclient import TestClient
from fastapi import status
import _thread as th
import time
import random
import requests
from enum import Enum
import string 

data = {"ip": "1.1.2.3"}
headers = {"Authorization": "Bearer MYREALLYLONGTOKENIGOT"}


def random_mail(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

class Endpoint(Enum):
    Login = "http://localhost:8000/api/user/login"
    Register = "http://localhost:8000/api/user/register"
    Base = "http://localhost:8000/api/"



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

def register_bot(bot: Bot):

    response = requests.post("http://localhost:8000/api/register/",
    headers={
        "Content-Type": "application/json"},
    json={
        "nickname": bot.nickname,
        "email": bot.email,
        "password": bot.password})
    assert response.status_code == 201
    bot.uid = response.json()

def bot_login(bot: Bot):
    response = requests.post(
        "http://localhost:8000/api/login/",
        headers={
            "Content-Type": "application/json"},
        json={
            "email": bot.email,
            "password": bot.password})
    assert response.status_code == 200
    # tokens
    bot.token = "Bearer " + response.json()["access_token"]
    return

def bot_join_lobby(lobby_id: int, bot: Bot):
    response = requests.post(
        "http://localhost:8000/api/lobbies/{}/join/".format(lobby_id),
        headers={
            "Authorization": bot.token})
    return response


idle_bots = []
playing_bots = []

def create_new_bot(nickname, email, password):

   bot = Bot(nickname=nickname, email=email, password=password)
   register_bot(bot=bot)
   bot_login(bot=bot)
   idle_bots.append(bot)

def add_bot_to_game(game_id):

    if 0 == len(idle_bots):
        nickname = "BOT" + str(random.randint(0,10000))
        email = random_mail(8)+"@m.com"
        password = "12341234"
        create_new_bot(nickname, email, password)

    bot = idle_bots.pop() 
    bot_join_lobby(lobby_id=game_id, bot=bot)
    playing_bots.append([bot, game_id])

def bot_leave_match(game_id:int, bot: Bot):
    response = requests.post("http://localhost:8000/api/lobbies/{}/leave/".format(game_id),
                        headers={"Authorization": bot.token})
    idle_bots.append(bot)
    playing_bots.remove([bot, game_id])

def bot_get_lobby_info(game_id: int, bot: Bot):
    response = requests.get(
        "http://localhost:8000/api/lobbies/{}".format(game_id),
        headers={
            "Authorization": bot.token})

    return response

def bot_get_game_info(game_id: int, bot: Bot):
    response = requests.get(
        "http://localhost:8000/api/games/{}/".format(game_id),
        headers={
            "Authorization": bot.token})
    return response



def bot_post_vote(game_id: int, vote: bool, bot: Bot):
    response = requests.post(
        "http://localhost:8000/api/games/{}/vote/".format(game_id),
        headers={
            "Content-Type": "application/json",
            "Authorization": bot.token},
        json={
            "vote": vote})
    return response

def bot_post_spell(game_id: int, bot: Bot, target: int):
    response = requests.post(
        "http://localhost:8000/api/games/{}/spell/".format(game_id),
        headers={
            "Content-Type": "application/json",
            "Authorization": bot.token},
        json={
            "target": target})
    return response


def bot_get_proclamation_cards(game_id: int, bot: Bot):
    response = requests.get(
        "http://localhost:8000/api/games/{}/proc/".format(game_id),
        headers={
            "Authorization": bot.token})
    return response


def bot_post_proclamation_cards(
        game_id: int,
        election: int,
        expelliarmus: bool,
        bot: Bot):
    response = requests.post(
        "http://localhost:8000/api/games/{}/proc/".format(game_id),
        headers={
            "Content-Type": "application/json",
            "Authorization": bot.token},
        json={
            "election": election,
            "expelliarmus": expelliarmus})
    return response



def bot_post_new_candidate(game_id: int, candidate_id: int, bot: Bot):
    response = requests.post(
        "http://localhost:8000/api/games/{}/director/{}/".format(
            game_id, candidate_id), headers={
            "Authorization": bot.token})
    return response



def bots_play():

    while True:
    
        for par in playing_bots:
            response = bot_get_lobby_info(game_id=par[1], bot=par[0])
            if not response.json()["started"]:
                time.sleep(1)
                break
            bot_login(par[0])
            response = bot_get_game_info(game_id=par[1], bot=par[0])
            targets = []
            for p in response.json()["player_list"]:             #no implementado todavia
                if p["alive"]: #and not p["crucied"] :
                    targets.append(p["player_id"])
            bot_post_vote(bot=par[0], game_id=par[1], vote=True)
            bot_post_spell(bot=par[0], game_id=par[1], target=random.choice(targets))
            bot_post_proclamation_cards(game_id=par[1],
                election=random.randint(0,2),
                expelliarmus=False,
                bot=par[0])
            bot_post_new_candidate(game_id=par[1],
                candidate_id=random.choice(targets),
                bot=par[0])
            time.sleep(2)


th.start_new_thread(bots_play, ())