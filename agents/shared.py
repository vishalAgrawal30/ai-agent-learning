AUTH_TOKEN_PROD = None

def set_auth_token(token: str):
    global AUTH_TOKEN_PROD
    AUTH_TOKEN_PROD = token