from application.socketo.roclasses import ro_manager
from application.socketo.games import Tic_Tac_Toe as ttt

class ro_gameTTT(ro_manager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.games = {}

    def put_users(self, username, sid, room):
        room_t= super().put_users(username, sid, room)
        if not room_t in self.games:
            self.games[room_t] = {}
            self.games[room_t]['members'] = set()
        self.games[room_t]['members'].add(username)
        return room_t

    def start_game(self, room, set_of_p):
        self.games[room]['game_state'] = 0
        self.games[room]['game'] = ttt.Board
        self.games[room]['X'] = ttt.pickX(list(set_of_p))
        self.games[room]['turn'] = 1
        return {'Board': self.games[room]['game'], 'X': self.games[room]['X'], 'state': self.games[room]['game_state']}

    def Move(self, room, move, who_moved):
        if who_moved == 1:
            self.games[room]['game'][move] = 'X'
            self.games[room]['game_state'] = ttt.check('X', self.games[room]['game'])
            if self.games[room]['game_state'] == 1:
                self.games[room]['Winner'] = 'X'
                return {'Board': self.games[room]['game'], 't_or_w':'X','state': self.games[room]['game_state']}
            self.games[room]['turn'] = 0

        else:
            self.games[room]['game'][move] = 'O'
            self.games[room]['game_state'] = ttt.check('O', self.games[room]['game'])
            if self.games[room]['game_state'] == 1:
                self.games[room]['Winner'] = 'O'
                return {'Board': self.games[room]['game'], 't_or_w':'O','state': self.games[room]['game_state']}
            self.games[room]['turn'] = 1
        return {'Board': self.games[room]['game'], 't_or_w':self.games[room]['turn'] ,'state': self.games[room]['game_state']}
