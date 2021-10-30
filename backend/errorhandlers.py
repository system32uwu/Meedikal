from flask import redirect
from flask.templating import render_template
from routers import apiRouter, frontendRouter
from util.returnMessages import *
from util.errors import *
from sqlite3.dbapi2 import IntegrityError
from util.createDb import getDb
import jwt

@apiRouter.errorhandler(jwt.ExpiredSignatureError)
def expiredToken(e):
    return genericErrorReturn('Signature expired. Please log in again.', code=401)

@apiRouter.errorhandler(jwt.InvalidTokenError)
def invalidToken(e):
    return genericErrorReturn('Invalid token. Please log in again.', code=401)
        
@apiRouter.errorhandler(MissingCookieError)
def missingCookieError(e):
    return genericErrorReturn('Not authenticated (missing cookie)', code=401)

@apiRouter.errorhandler(MissingRoleError)
def missingRoleError(e: MissingRoleError):
    return genericErrorReturn(f'Insufficient permissions to perfom action. It should be done by: {",".join(e.roles)} users', code=403)

@apiRouter.errorhandler(UpdatePasswordError)
def updatePasswordError(e):
    return genericErrorReturn(f"can't update password with this method. PUT or PATCH the api/auth/updatePassword endpoint instead.", code=403)

@apiRouter.errorhandler(TypeError)
def typeError(e:TypeError):
    err = repr(e)

    if 'missing' in err:
        field = err.split(': ')[1].split('")')[0]
        return provideData(f'missing key field: {field}')
    else:
        return provideData()

@apiRouter.errorhandler(KeyError)
def keyError(e:KeyError):
    return provideData(f'missing required fields: {", ".join(e.args)}')

@apiRouter.errorhandler(IntegrityError)
def integrityError(e:IntegrityError):
    err = repr(e)
    getDb().rollback()

    if 'FOREIGN KEY' in err:
        return genericErrorReturn(f"foreign key error: one of the values you are referring to was deleted or never existed")
    else:       
        if 'UNIQUE' in err or 'NOT NULL' in err:
            errData = err.split(": ")
            attrs = errData[1].split("')")[0]

            if 'UNIQUE' in err:
                return recordAlreadyExists(extraMessage=attrs)
            elif 'NOT NULL' in err:
                return provideData(f'missing required fields: {attrs}')
        else:
            return provideData(str(e))

@apiRouter.errorhandler(ValueError)
def valueError(e: ValueError):
    e = str(e)
    if ('isoformat' in e):
        return provideData('invalid date')
    else:
        return genericErrorReturn(e)

@apiRouter.errorhandler(ExtensionNotAllowedError)
def extensionNotAllowed(e: ExtensionNotAllowedError):
    return genericErrorReturn(f'extension {e.deniedExt} not allowed.', f'allowed extensions: {", ".join(e.allowed)}')

@apiRouter.errorhandler(PaginationError)
def extensionNotAllowed(e: PaginationError):
    return genericErrorReturn(f'Missing pagination query parameters (offset and limit)')

@apiRouter.errorhandler(AttributeError)
def attributeError(e: AttributeError):
    err = str(e)
    if 'models' in err:
        return genericErrorReturn(f'Resource does not exist')
    else:
        return genericErrorReturn(e)

@apiRouter.errorhandler(Exception) # any other exception
def handleException(e:Exception):
    err = repr(e)
    print(err)
    getDb().rollback()
    return {"error": repr(err)}, 400

@frontendRouter.errorhandler(MissingCookieError)
@frontendRouter.errorhandler(jwt.ExpiredSignatureError)
@frontendRouter.errorhandler(jwt.InvalidTokenError)
def missingCookieError(e):
    return redirect('/login')

@frontendRouter.errorhandler(MissingRoleError)
def missingRoleErrorF(e: MissingRoleError):
    return redirect('/app')