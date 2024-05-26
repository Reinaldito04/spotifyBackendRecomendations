from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from Assets.spotify import sp_oauth
import spotipy
from Assets.geminiClient import GeminiAi
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Aquí puedes especificar los orígenes permitidos en lugar de "*"
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
geminiInstance = GeminiAi()
@app.get("/")
def hello():
    return {"hola":"hi"}

@app.get("/search/{user_id}")
def search_songs(user_id: str):
    try:
        auth_url = sp_oauth.get_authorize_url()
        return JSONResponse(content={"authorization_url": auth_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/callback/")
def spotify_callback(code: str):
    try:
        token_info = sp_oauth.get_access_token(code)
        if token_info:
            access_token = token_info['access_token']
            sp = spotipy.Spotify(auth=access_token)
            canciones = []
            results = sp.current_user_recently_played()
            for idx, item in enumerate(results['items']):
                track = item['track']
                canciones.append(track['name'])
            pregunta = geminiInstance.Question("¿Me puedes recomendar canciones en base a esta lista, que sea del mismo género?,solo dame la lista de las canciones,no me digas el genero ni alguna otra información", canciones)
            recomendaciones = pregunta.split('\n')

            # Realizar otra búsqueda para obtener las imágenes de las canciones recomendadas
            songs_with_images = []
            for song in recomendaciones:
                # Realizar búsqueda en Spotify para obtener la información de la canción
                results = sp.search(q=f"track:{song}", type='track', limit=1)
                if results['tracks']['items']:
                    track_info = results['tracks']['items'][0]
                    if 'album' in track_info and 'images' in track_info['album'] and len(track_info['album']['images']) > 0:
                        # La URL de la imagen del álbum se encuentra en la primera imagen (generalmente la más grande)
                        image_url = track_info['album']['images'][0]['url']
                        song_url = track_info['external_urls']['spotify']
                        song_name = track_info['name']
                        artists = track_info['artists']
                        # Extraer el nombre del primer artista de la lista
                        artist_name = artists[0]['name']
                        songs_with_images.append({'name': song_name,"artist":artist_name, 'image_url': image_url,"song_url":song_url})

            return JSONResponse(content={"recommendation": recomendaciones, "songs_with_images": songs_with_images})
        else:
            raise HTTPException(status_code=401, detail="No se pudo obtener el token de acceso")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
