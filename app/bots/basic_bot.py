from fastapi.testclient import TestClient
from fastapi import status
from app import main

import random as rand

def random_mail(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

client = TestClient(main.svapi)

class Bot(User):
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
    
idle_bots = []
playing_bots = {}

def create_new_bot(nickname, email, password):

   bot = User(nickname=nickname, email=email, password=password)
   register_usert(user=bot)
   login(user=bot)
   idle_bots.append(bot)

def add_bot_to_game(game_id):

    if 0 < len(idle_bots):
        nickname = "BOT" + str(len(idle_bots))
        email = random_mail(8)+"@m.com"
        password = "12341234"
        create_new_bot(nickname, email, password)
    
    bot = idle_bots.pop()   
    join_lobby(lobby_id=game_id, user=bot)
    playing_bots.append([bot, game_id])

def bot_leave_match(game_id:int, bot: Bot):
    leave_match(lobby_id=game_id, user=bot)
    idle_bots.append(bot)
    playing_bots.remove([bot, game_id])

while True:
    for par in playing_bots:
        response = get_game_info(game_id=par[1], user=par[0])
        valid_target = -1
        for p in response["player_list"]:
            if response["player_list"][0]["alive"]:
                valid_target = response["player_list"][0][""]
        post_vote(user=par[0], game_id=par[1], vote=True)
        post_spell(user=par[0], game_id=par[1], target=2)
        post_proclamation_cards(game_id=par[1],
        election=2,
        expelliarmus=True,
        user=par[0])
        post_new_candidate(game_id=par[1],
        candidate_id=2,
        user=par[0])