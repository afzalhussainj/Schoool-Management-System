from enum import Enum

class RoleChoicesUsers(Enum):
    admin = 0
    owner = 1
    manager = 2

class RoleChoicesMembers(Enum):
    guardian = 0
    student = 1