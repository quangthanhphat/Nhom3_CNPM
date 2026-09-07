from abc import ABC, abstractmethod
from typing import Optional

from .auth import Auth


class IAuthRepository(ABC):

    @abstractmethod
    def login(self, auth: Auth) -> Auth:
        pass

    @abstractmethod
    def register(self, auth: Auth) -> Optional[Auth]:
        pass

    @abstractmethod
    def remember_password(self) -> Optional[Auth]:
        pass

    @abstractmethod
    def look_account(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def un_look_account(self, user_id: int) -> None:
        pass

    @abstractmethod
    def check_exist(self, username: str) -> bool:
        pass