class MissingCookieError(Exception):
    pass

class MissingRoleError(Exception):
    roles: list[str]
    
    def __init__(self, roles:str):
        self.roles = roles

class UpdatePasswordError(Exception):
    pass