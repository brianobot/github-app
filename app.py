import requests
import environ
from utils import get_jwt_token

env = environ.Env()
environ.Env.read_env()

APP_ID = env("GITHUB_APP_ID")
CLIENT_ID = env("GITHUB_CLIENT_ID")
CLIENT_SECRET = env("GITHUB_CLIENT_SECRET")

def get_headers(token: str) -> dict:
    return {
        'X-GitHub-Api-Version': '2022-11-28',
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
    }

token = get_jwt_token()


