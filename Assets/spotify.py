import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from Assets.geminiClient import GeminiAi
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('clientID')
client_secret = os.getenv('clientSecret')
# Debes añadir esta URL en la configuración de tu app en Spotify
redirect_uri = 'https://6jjvf5b7-5173.use2.devtunnels.ms/recomendations'

scope = 'user-read-recently-played'

# Crea un objeto de autenticación de SpotifyOAuth
sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                        redirect_uri=redirect_uri, scope=scope)

# Obtén el URL de autorización para que cualquier usuario autorice tu aplicación
auth_url = sp_oauth.get_authorize_url()

# Muestra el URL de autorización
print("Por favor, visita esta URL para autorizar la aplicación: \n", auth_url)

# Obtiene el código de autorización directamente (por ejemplo, desde la consola o un formulario web)

# Intercambia el código de autorización por un token de acceso
token_info = sp_oauth.get_cached_token()


geminiAiInstance = GeminiAi()
# Comprueba si se ha obtenido el token de acceso correctamente
if token_info:
    access_token = token_info['access_token']
    # Crea un objeto de cliente de Spotify con el token de acceso
    sp = spotipy.Spotify(auth=access_token)
    canciones = []
    # Usa el objeto de cliente de Spotify para obtener las últimas canciones reproducidas
    results = sp.current_user_recently_played()
    for idx, item in enumerate(results['items']):
        track = item['track']
        canciones.append(track['name'])

    print("canciones", canciones)
    pregunta = geminiAiInstance.Question(
        "Basado en tu historial de reproducción, ¿podrías sugerirme canciones similares a estas?",
        canciones
    )

    print(pregunta)
else:
    print("No se pudo obtener el token de acceso")
