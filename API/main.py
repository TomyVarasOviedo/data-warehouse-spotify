from fastapi import FastAPI
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    "--token", type=str, required=True, help="API token for authentication"
)

app = FastAPI()

TOKEN = arg_parser.parse_args().token


@app.get("/track-id/{track_id}")
async def get_track_info(track_id: str):
    # Implementar API de Spotify para buscar id de track
    pass


@app.get("/artist-id/{artist_id}")
async def get_artist_info(artist_id: str):
    # Implementar API de Spotify para buscar id de artista
    pass
