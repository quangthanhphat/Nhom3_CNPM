class Auth:
    def __init__(
        self,
        username: str,
        password: str,
        passwordconfirm: str,
        email: str
    ):
        self.username = username
        self.password = password
        self.passwordconfirm = passwordconfirm
        self.email = email
        self.id = None