class MissingCookieError(Exception):
    pass

class MissingRoleError(Exception):
    def __init__(self, role:str):
        self.role = role

class UpdatePasswordError(Exception):
    pass