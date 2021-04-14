from application import create_app, db
from application.models import User, Post, Message, Active_Chats
from test_config import Test_Config
import socketio
from application import sio

asp = create_app()


app= socketio.WSGIApp(sio, asp)
#    socketio.run(app)
# To start: gunicorn -k eventlet -w 1 --thread 50 --reload FAIF1:app

@asp.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User, 'Post':Post, 'Message': Message, 'AC': Active_Chats, 'test_config':Test_Config, 'CA': create_app}
