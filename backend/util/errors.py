class MissingCookieError(Exception):
    pass

class MissingRoleError(Exception):
    roles: list[str]
    
    def __init__(self, roles:str):
        self.roles = roles

class UpdatePasswordError(Exception):
    pass

class PaginationError(Exception):
    pass

class ExtensionNotAllowedError(Exception):
    allowed: list
    deniedExt: str

    def __init__(self, allowed:list, deniedExt: str):
        self.allowed = allowed
        self.deniedExt = deniedExt