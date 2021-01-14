import os

TIMEOUT = 30

RUN_LOCALLY = True

URLS = {
    'stage': 'https://staging.emissary.io/'
}

BASE_URL = os.getenv('ENV') if os.getenv('ENV') else URLS.get('stage')

USER_EMAIL = 'dmytro@emissary.io'
USER_PASSWORD = os.getenv('USER_PASSWORD')
