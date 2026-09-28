from flask_login import UserMixin


class Usuario(UserMixin):
    def __init__(self, id_usuario, username, password_hash):
        self.id_usuario = id_usuario
        self.username = username
        self.password_hash = password_hash

    def get_id(self):
        return str(self.id_usuario)