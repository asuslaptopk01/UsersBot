from dataclasses import dataclass

from database.settings import CRUD


@dataclass
class User(CRUD):
    id : int = None
    name : str = None
    age : int = None
    gender : str = None
    username : str = None
    saved_at : str = None