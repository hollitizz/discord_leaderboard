from typing import NewType

class User():
    def __init__(self, tag, name, id):
        self.tag: str = tag
        self.name: str = name
        self.tier: int = 0
        self.rank: int = 1
        self.lp: int = 0
        self.id: str = id

userList = NewType("userList", list[User])
