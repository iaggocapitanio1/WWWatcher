from requests_auth import OAuth2ClientCredentials, OAuth2, JsonTokenFileCache
import settings


OAuth2.token_cache = JsonTokenFileCache(settings.CACHE_FILE.__str__())

oauth = OAuth2ClientCredentials(
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    token_url=settings.TOKEN_URL,
)