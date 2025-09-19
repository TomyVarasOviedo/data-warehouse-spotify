import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import requests

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
    "Authorization Bearer": "",
}


# Modelo de petición a la API de Spotify
class SpotifyAPIRequest(BaseModel):
    def __init__(self, client_id: str | None, client_secret: str | None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    def set_token(self, token: str):
        self.token = token

    def get_token(self) -> str | None:
        crendentials = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        try:
            token = requests.post(
                "https://accounts.spotify.com/api/token",
                headers=headers,
                json=crendentials,
            )
            if token.status_code == 200:
                token_json = token.json()
                self.set_token(token_json["access_token"])
                headers["Authorization Bearer"] = f"{self.token}"
                return self.token
            else:
                raise HTTPException(token.status_code)

        except HTTPException as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None

        except Exception as e:
            print(f"Error al obtener token: {e}")
            return None


app = FastAPI()


@app.get("/track-id/{track_id}")
async def get_track_info(track_id: str):
    pass


@app.get("/artist-id/{artist_id}")
async def get_artist_info(artist_id: str):
    # Implementar API de Spotify para buscar id de artista
    pass


if __name__ == "__main__":
    import uvicorn

    load_dotenv()
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    print(client_id, client_secret)
    TOKEN = SpotifyAPIRequest(str(client_id), str(client_secret))
    TOKEN.get_token()
    uvicorn.run(app, host="0.0.0.0", port=8000)
