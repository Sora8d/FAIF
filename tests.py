from datetime import datetime, timedelta
import unittest
from application import create_app, db
from application.models import User, Post, Message
from test_config import Test_Config

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app= create_app(Test_Config)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u=User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), 'https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128')

    def test_follow(self):
        u1= User(username='john', email='john@example.com')
        u2= User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        u1= User(username='john', email='john@example.com')
        u2= User(username='susan', email='susan@example.com')
        u3= User(username='mary', email='mary@example.com')
        u4= User(username='david', email='david@example.com')
        db.session.add_all([u1,u2,u3,u4])

        now= datetime.utcnow()
        p= []
        t = 1
        for x in [u1,u2,u3,u4]:
            p.append(Post(body=f'post from {x.username}', author=x, timestamp=now + timedelta(seconds=t)))
            t+=1
        db.session.add_all(p)
        db.session.commit()

        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u3)
        u3.follow(u4)
        db.session.commit()

        f= []
        for x in [u1,u2,u3,u4]:
            f.append(x.followed_posts().all())
        self.assertEqual(f[0], [p[3], p[1], p[0]])
        self.assertEqual(f[1], [p[2], p[1],])
        self.assertEqual(f[2], [p[3], p[2]])
        self.assertEqual(f[3], [p[3]])

    def test_messages(self):
        u1= User(username='john', email='john@example.com')
        u2= User(username='susan', email='susan@example.com')
        u3= User(username='mary', email='mary@example.com')
        u4= User(username='david', email='david@example.com')
        db.session.add_all([u1,u2,u3,u4])
        db.session.commit()

        now= datetime.utcnow()
        m1= Message(body='Test1', author=u1, recipient=u2, timestamp=now + timedelta(seconds=1))
        m2= Message(body='Test2', author=u2, recipient=u1, timestamp=now + timedelta(seconds=2))
        m3= Message(body='Test3', author=u2, recipient=u4, timestamp=now + timedelta(seconds=3))
        m4= Message(body='Test4', author=u4, recipient=u1, timestamp=now + timedelta(seconds=4))
        m5= Message(body='Test5', author=u1, recipient=u2, timestamp=now)
        db.session.add_all([m1,m2,m3,m4,m5])
        db.session.commit()

        print(u1.Get_Chats())
        print(u1.Get_Messages(u2).all())


if __name__ == '__main__':
    unittest.main(verbosity=2)
