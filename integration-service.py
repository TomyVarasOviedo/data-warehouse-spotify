import pandas as pd
from models_db import (
    Dim_cancion,
    Dim_artista,
    Dim_album,
    Dim_razon,
    Dim_concierto,
    Dim_plataforma,
    # Dim_fecha,
)
import requests
# import db_connection as db

spotify_df = pd.read_csv("spotify_history.csv", chunksize=2000)
conciertos_df = pd.read_csv("spotify_conciertos.csv", chunksize=2000)


def fetch_to_api(track_id: str):
    track_data = requests.get(f"http://localhost:8000/track-id/{track_id}").json()
    artist_data = requests.get(
        f"http://localhost:8000/artist-id/{track_data['artists'][0]}"
    ).json()
    album_data = requests.get(
        f"http://localhost:8000/album-id/{track_data['album_id']}"
    ).json()

    cancion = Dim_cancion(
        id_cancion=track_data["track_id"],
        titulo=track_data["track_name"],
        artista_id=track_data["artists"][0],
        album_id=track_data["album_id"],
        duracion=track_data["duration_ms"],
    )

    artista = Dim_artista(
        id_artista=track_data["artists"][0],
        nombre=artist_data["artist_name"],
    )
    album = Dim_album(
        id_album=album_data["album_id"],
        nombre=album_data["album_name"],
        artista_id=artist_data["artist_id"],
        fecha_publicacion=album_data["release_date"],
    )

    return cancion, artista, album


def set_another_models(
    razon,
    plataforma,
    concierto_id,
    concierto_nombre,
    concierto_pais,
    concierto_capacidad,
):
    razon = Dim_razon(nombre=razon)

    plataforma = Dim_plataforma(nombre=plataforma)

    concierto = Dim_concierto(
        id_concierto=concierto_id,
        nombre=concierto_nombre,
        pais=concierto_pais,
        capacidad=concierto_capacidad,
    )

    return razon, plataforma, concierto


if __name__ == "__main__":
    for chunk in conciertos_df:
        for index, row in chunk.iterrows():
            # Insertar dimensiones
            razon, plataforma, concierto = set_another_models(
                row["razon"],
                row["plataforma"],
                row["concierto_id"],
                row["concierto_nombre"],
                row["concierto_pais"],
                row["concierto_capacidad"],
            )

            # Insertar dimensiones

            # Insertar datos de facts
            #
