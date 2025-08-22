# sample.py
AUTH_TOKEN_PROD = None

def set_auth_token(token: str):
    global AUTH_TOKEN_PROD
    AUTH_TOKEN_PROD = token
    print("Token set in sample.py:", AUTH_TOKEN_PROD)

def print_auth_data(auth_data: dict):
    print("Full auth data received in sample.py:", auth_data)
