from models import Model
from utils import formatted_time
import time

Model = Model


class Reply(Model):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('content', str, ''),
            ('topic_id', str, 0),
            ('user_id', str, 0),
            ('ct', str, formatted_time(int(time.time()))),
        ]
        return names

    def user(self):
        from .user import User
        u = User.find(self.user_id)
        return u
