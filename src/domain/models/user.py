class User:
    def __init__(
        self,
        email: str,
        full_name: str,
        phone: str = None,
        avatar_url: str = None,
        role: str = "customer",
        status: str = "active"
    ):
        self.id = None
        self.email = email
        self.full_name = full_name
        self.phone = phone
        self.avatar_url = avatar_url
        self.role = role
        self.status = status
        self.created_at = None
        self.updated_at = None