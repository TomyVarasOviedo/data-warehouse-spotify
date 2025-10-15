import json
import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import requests

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
}


def get_token(client_id: str, client_secret: str) -> str | None:
    try:
        token = requests.post(
            "https://accounts.spotify.com/api/token",
            headers=headers,
            data={"grant_type": "client_credentials"},
            auth=(client_id, client_secret),
        )
        token.raise_for_status()
        token = token.json()
        token = token["access_token"]
        headers["Authorization"] = f"Bearer {token}"
        return token

    except HTTPException as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None

    except requests.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return None


# Cargar variables de entorno
load_dotenv()
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
TOKEN = get_token(str(client_id), str(client_secret))

app = FastAPI()
# ------------------------#
# --- Rutas de la API --- #
# ------------------------#


@app.get("/track-id/{track_id}")
async def get_track_info(track_id: str):
    try:
        peticion = requests.get(
            f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers
        )
        if peticion.status_code == 200:
            response = json.loads(peticion.text)

            return {
                "track_id": response["id"],
                "track_name": response["name"],
                "artists": [artist["id"] for artist in response["artists"]],
                "album_id": response["album"]["id"],
                "duration_ms": response["duration_ms"],
            }

    except HTTPException as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    except Exception as e:
        print(f"Error al realizar la petición: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@app.get("/artist-id/{artist_id}")
async def get_artist_info(artist_id: str):
    # Implementar API de Spotify para buscar id de artista
    try:
        peticion = requests.get(
            f"https://api.spotify.com/v1/artists/{artist_id}", headers=headers
        )
        if peticion.status_code == 200:
            response = json.loads(peticion.text)
            return {
                "artist_id": response["id"],
                "artist_name": response["name"],
                "followers": response["followers"]["total"],
            }

    except HTTPException as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    except Exception as e:
        print(f"Error al realizar la petición: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@app.get("/album-id/{album_id}")
async def get_album_info(album_id: str):
    # Implementar API de Spotify para buscar por id de album
    try:
        peticion = requests.get(
            f"https://api.spotify.com/v1/albums/{album_id}", headers=headers
        )
        if peticion.status_code == 200:
            response = json.loads(peticion.text)
            return {
                "album_id": response["id"],
                "album_name": response["name"],
                "release_date": response["release_date"],
            }
    except HTTPException as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    except Exception as e:
        print(f"Error al realizar la petición: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# ------------------------#
# --- Rutas de la API --- #
# ------------------------#

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
