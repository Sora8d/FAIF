import socketio
from application.socketo import bp
from flask import redirect, url_for, current_app, render_template
from flask_login import login_required
from application import create_app, sio
from application.socketo.roclasses import ro_manager
from socketio import Namespace

#games nad stuff
from application.socketo.games.gameclasses import ro_gameTTT
import json

@bp.route('/socketo1')
@login_required
def WORK():
    return render_template('socketo/SIO.html', namesp='/socketo10')

@bp.route('/socketo2')
@login_required
def WORKt():
    return render_template('socketo/SIO.html', namesp='/socketo10')

@bp.route('/socketo1/Tic-Tac-Toe')
def ttt():
    return render_template('socketo/SIO_TTT.html', namesp='/play_cunt')

values= {
    'slider1': 25,
    'slider2': 0,
}

M_N = ro_manager()
M_G= ro_gameTTT()
class ThaServer(Namespace):
    def __init__(self, *args, **kwargs):
        super().__init__(* args, **kwargs)
        self.s1 = M_N
    def on_connect(self, sid, environ):
        print('We noticed something, yhea we did')
        print(sid, 'connected')
        self.emit('after_connect', {'msg': 'holy f'})

    def on_c_room(self, sid, c_name):
        R = self.s1.check_room(c_name)
        room = self.s1.put_users(c_name, sid, R)
        self.enter_room(sid, room)
        self.emit('room_entry', {'msg': 'Welcome to {}'.format(R), 'room': R}, room=R)
        return R

    def on_disconnect(self, sid):
        self.leave_room(sid, self.s1.members[sid][1])
        self.s1.pop_user(sid, self.s1.members[sid][1])
        print(sid, ' disconnected')

    def on_s_v_c(self, sid, message):
        print('Something changed')
        values[message['who']] = message['data']
        self.emit('update_value', message, room=self.s1.members[sid][1])

    def on_m_t_n(self, sid, data):
        print('sending message')
        self.emit('receive_msg', {'msg': data['autor'] + ' said ' + data['msg'] }, room=self.s1.members[sid][1])
        print(self.get_session(sid))
        print(self.rooms(sid))

class Game_TTT(ThaServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.s1= M_G

    def on_c_room(self, sid, c_name):
        print('Trying this')
        room = super().on_c_room(sid, sid)
        if len(self.s1.games[room]['members']) == 2:
            type(self.s1.games[room]['members'])
            Game = self.s1.start_game(room, self.s1.games[room]['members'])
            print('Game starting')
            self.emit('start_game', Game)

    def on_move(self, sid, move, who_moved):
        State = self.s1.Move(self.s1.members[sid][1], move, who_moved)
        self.emit('state', State)

    def on_disconnect(self, sid):
        if self.s1.games[self.s1.members[sid][1]]['game_state']:
            super().on_disconnect(sid)
        else:
            print(sid, ' disconnected, but game aint over so we waiting')



sio.register_namespace(ThaServer('/socketo10'))
sio.register_namespace(Game_TTT('/play_cunt'))
