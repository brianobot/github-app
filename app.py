import requests
import environ

env = environ.Env()
environ.Env.read_env()

APP_ID = env("GITHUB_APP_ID")
CLIENT_ID = env("GITHUB_CLIENT_ID")
CLIENT_SECRET = env("GITHUB_CLIENT_SECRET")
