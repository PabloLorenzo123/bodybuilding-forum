from . import main
from ..helpers import apology


# This will handle errors from any request in the App. Use blueprint error handler otherwise.
@main.app_errorhandler(404)
def page_not_found(e):
    return apology(code=404, message='Page not found')

@main.app_errorhandler(500)
def internal_server_error(e):
    return apology(code=500, message='Internal server error')

@main.app_errorhandler(429)
def internal_server_error(e):
    return apology(code=429, message='Too many requests')

@main.app_errorhandler(403)
def forbidden(e):
    return apology(code=403, message="You don't have the permission to access the requested resource. It is either read-protected or not readable by the server.")