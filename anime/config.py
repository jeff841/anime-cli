from os import environ

from dotenv import load_dotenv

load_dotenv()

def get_mal_client_id():
    return environ.get("MAL_CLIENT_ID")
