import environ
import time
from jwt import JWT, jwk_from_pem

env = environ.Env()
environ.Env.read_env()

APP_ID = env("GITHUB_APP_ID")
PEM_FILE = env("PEM_FILE")


def get_jwt_token():
    with open(PEM_FILE, "rb") as pem_file:
        signing_key = jwk_from_pem(pem_file.read())

        payload = {
            # Issued at time
            'iat': int(time.time()),
            # JWT expiration time (10 minutes maximum)
            'exp': int(time.time()) + 600,
            # GitHub App's identifier
            'iss': APP_ID
        }

        # Create JWT
        jwt_instance = JWT()
        encoded_jwt = jwt_instance.encode(payload, signing_key, alg='RS256')
    return encoded_jwt