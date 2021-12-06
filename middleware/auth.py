from config import SECRET_KEY
def Authenticate(token=""):
    if token == SECRET_KEY:
        return True
    return False