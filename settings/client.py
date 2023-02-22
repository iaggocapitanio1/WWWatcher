from requests_auth import OAuth2ClientCredentials, OAuth2, JsonTokenFileCache
from settings import settings


OAuth2.token_cache = JsonTokenFileCache('./cache.json')

oauth = OAuth2ClientCredentials(
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    token_url=settings.TOKEN_URL,
)
