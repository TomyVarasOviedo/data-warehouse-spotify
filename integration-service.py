import pandas as pd
from models_db import (
    Base,
    Dim_cancion,
    Dim_artista,
    Dim_album,
    Dim_razon,
    Dim_concierto,
    Dim_plataforma,
    # Dim_fecha,
    Session,
)
import requests
# import db_connection as db

spotify_df = pd.read_csv("spotify_history.csv")  # , chunksize=2000)
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


def set_another_models():
    plataformas = spotify_df["platform"].value_counts()
    plataformas = plataformas[plataformas >= 1]
    razones = pd.concat([spotify_df["reason_start"], spotify_df["reason_end"]])
    razones = razones.value_counts()
    razones = razones[razones >= 1]
    insert = ""
    # Insertar dimensiones de plataforma
    for _, plataforma in plataformas:
        insert += f"(NULL, '{plataforma}')"
    consulta = text(
        "INSERT INTO dim_plataforma (id_plataforma, nombre) VALUES " + insert
    )
    with engine.connect() as conn:
        conn.execute(consulta)
        conn.commit()
    # Insertar dimensiones de razon
    for _, razon in razones:
        insert += f"(NULL, '{razon}')"
    consulta = text("INSERT INTO dim_razon (id_razon, nombre) VALUES " + insert)
    with engine.connect() as conn:
        conn.execute(consulta)
        conn.commit()


if __name__ == "__main__":
    pass
    # for chunk in spotify_df:

    # for index, row in chunk.iterrows():
    # Insertar dimensiones
    #        razon, plataforma, concierto = set_another_models(
    #            row["razon"],
    #            row["plataforma"],
    #            row["concierto_id"],
    #            row["concierto_nombre"],
    #            row["concierto_pais"],
    #            row["concierto_capacidad"],
    #        )

    # Insertar dimensiones

    # Insertar datos de facts
