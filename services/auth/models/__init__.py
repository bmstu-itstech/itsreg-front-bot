"""Contains all the data models used in inputs/outputs"""

from .authenticated import Authenticated
from .error import Error
from .post_login import PostLogin
from .post_register import PostRegister
from .user import User

__all__ = (
    "Authenticated",
    "Error",
    "PostLogin",
    "PostRegister",
    "User",
)
