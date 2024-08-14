from celery import Celery
import requests
import cachetools
from requests.exceptions import HTTPError, RequestException

app = Celery('tasks', broker='redis://localhost:6379/0')

# Lista de tokens de API (sustituye por tus tokens válidos)
TOKENS = ['token1', 'token2', 'token3']

# Cache para los perfiles
cache = cachetools.TTLCache(maxsize=100, ttl=600)

# Función para manejar la rotación de tokens
def get_token():
    token = TOKENS.pop(0)
    TOKENS.append(token)
    return token

# Tarea para obtener datos de LinkedIn
@app.task(bind=True)
def fetch_linkedin_profile_task(self, profile_id):
    token = get_token()
    API_URL = f'https://api.linkedin.com/v2/me/{profile_id}'
    HEADERS = {
        'Authorization': f'Bearer {token}',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    if profile_id in cache:
        return cache[profile_id]

    try:
        response = requests.get(API_URL, headers=HEADERS)
        response.raise_for_status()
        profile_data = response.json()
        cache[profile_id] = profile_data
        return profile_data
    except HTTPError as http_err:
        self.retry(countdown=60, exc=http_err)
    except RequestException as req_err:
        raise self.retry(exc=req_err, countdown=60)
    except Exception as err:
        print(f"Error inesperado: {err}")
    return None
