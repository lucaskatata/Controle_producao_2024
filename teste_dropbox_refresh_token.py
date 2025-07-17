# %%
from requests_oauthlib import OAuth2Session
import json

# Credenciais do seu aplicativo
CLIENT_ID = "e4v3cerv1tdezzy"
CLIENT_SECRET = "e0lm5xjovud4neh"
REDIRECT_URI = "http://localhost:8080"
TOKEN_URL = "https://api.dropboxapi.com/oauth2/token"

# Criar uma sessão OAuth2
oauth2_session = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)

# URL de autorização
authorization_url, state = oauth2_session.authorization_url(
    "https://www.dropbox.com/oauth2/authorize",
    access_type="offline",  # Isso deve pedir explicitamente o refresh token
)

print(f"Por favor, acesse esta URL para autorizar: {authorization_url}")

# Após autorização, o usuário será redirecionado para a REDIRECT_URI com um código
authorization_response = input("Cole aqui a URL completa após a autorização: ")

# Solicitar tokens usando o código obtido
token = oauth2_session.fetch_token(
    TOKEN_URL,
    authorization_response=authorization_response,
    client_secret=CLIENT_SECRET,
    # Informe que você quer o refresh token
    include_client_id=True,
)

# Exiba ou armazene os tokens, incluindo o refresh token
print("Access Token:", token["access_token"])
print("Refresh Token:", token.get("refresh_token"))
