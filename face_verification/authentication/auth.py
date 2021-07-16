from flask import request


def check_auth_header():
    username, password = (
        request.authorization.get("username", None),
        request.authorization.get("password", None),
    )
    if not username or not password:
        return False, "Unable to authenticate user"
    if username != "admin" or password != "admin":
        return False, "Invalid authentication header"
    return True, "Successfully authenticated"
