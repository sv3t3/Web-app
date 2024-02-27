from kinde_sdk.kinde_api_client import GrantType


SITE_HOST = "localhost"
SITE_PORT = "5000"
SITE_URL = f"http://{SITE_HOST}:{SITE_PORT}"
LOGOUT_REDIRECT_URL = f"http://{SITE_HOST}:{SITE_PORT}/api/auth/logout"
KINDE_CALLBACK_URL = f"http://{SITE_HOST}:{SITE_PORT}/api/auth/kinde_callback"
CLIENT_ID = "a0fecd908d72434ebeba56f1a05e0bce"
CLIENT_SECRET = "LXj6Xsd9N8acawKca20ReOsYGre2vMzMGoadUD76qzehOUWwPp6RW"
KINDE_ISSUER_URL = "https://coinlumy0.kinde.com"
GRANT_TYPE = GrantType.AUTHORIZATION_CODE_WITH_PKCE
CODE_VERIFIER = "joasd923nsad09823noaguesr9u3qtewrnaio90eutgersgdsfg" # A suitably long string > 43 chars
TEMPLATES_AUTO_RELOAD = True
SESSION_TYPE = "filesystem"
SESSION_PERMANENT = False
SECRET_KEY = "joasd923nsad09823noaguesr9u3qtewrnaio90eutgersgdsfgs" # Secret used for session management
