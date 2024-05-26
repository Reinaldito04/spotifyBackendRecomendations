import requests

# Paso 1: Obtener la URL de autorización de Spotify
def get_authorization_url():
    response = requests.get("http://localhost:8000/search/user123")  # Reemplaza "user123" con el ID de usuario real o ficticio
    return response.json()["authorization_url"]

# Paso 2: Autorizar la aplicación en Spotify
def authorize_spotify():
    authorization_url = get_authorization_url()
    print("Por favor, visita esta URL para autorizar la aplicación en Spotify:")
    print(authorization_url)
    authorization_code = input("Después de autorizar, introduce el código de autorización: ")
    return authorization_code

# Paso 3: Intercambiar el código de autorización por un token de acceso
def get_access_token(authorization_code):
    response = requests.get(f"http://localhost:8000/callback/?code={authorization_code}")
    if response.status_code == 200:
        response_json = response.json()
        print("Respuesta JSON recibida:")
        print(response_json)
        try:
            access_token = response_json["access_token"]
            return access_token
        except KeyError:
            print("Error: No se pudo encontrar el token de acceso en la respuesta.")
            return None
    else:
        print("Error al obtener el token de acceso.")
        return None

# Paso 4: Probar la API para obtener recomendaciones de canciones
def test_api(access_token):
    if access_token:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get("http://localhost:8000/callback/", headers=headers)
        if response.status_code == 200:
            print("Canciones recientes y recomendaciones:")
            print(response.json())
        else:
            print("Error al obtener recomendaciones.")
    else:
        print("No se pudo obtener el token de acceso.")

if __name__ == "__main__":
    authorization_code = authorize_spotify()
    access_token = get_access_token(authorization_code)
    test_api(access_token)
