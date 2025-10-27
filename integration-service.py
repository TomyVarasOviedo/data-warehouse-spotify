from datetime import datetime
import pandas as pd
from tqdm import tqdm
from models_db import (
    Dim_cancion,
    Dim_artista,
    Dim_album,
    Dim_fecha,
    Dim_razon,
    Dim_concierto,
    Dim_plataforma,
    Facts_spotify,
    engine,
    Session,
)
import requests

spotify_df = pd.read_csv("spotify_history.csv", chunksize=20)
conciertos_df = pd.read_csv("spotify_conciertos.csv", chunksize=2000)


def set_api_models(track_id: str):
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
        duracion=int(track_data["duration_ms"]),
    )

    artista = Dim_artista(
        id_artista=track_data["artists"][0],
        nombre=artist_data["artist_name"],
    )
    fecha_stage = datetime.strptime(album_data["release_date"], "%Y-%m-%d").date()
    album = Dim_album(
        id_album=album_data["album_id"],
        nombre=album_data["album_name"],
        artista_id=artist_data["artist_id"],
        fecha_publicacion=fecha_stage,
    )

    return cancion, artista, album


def find_data_with_name(
    platform_name=None, razon_llegada_name=None, razon_salida_name=None
):
    with Session(bind=engine) as session:
        if platform_name:
            plataforma = (
                session.query(Dim_plataforma)
                .filter(Dim_plataforma.nombre == platform_name)
                .first()
            )
        if razon_llegada_name:
            razon_llegada = (
                session.query(Dim_razon)
                .filter(Dim_razon.nombre == razon_llegada_name)
                .first()
            )
        if razon_salida_name:
            razon_salida = (
                session.query(Dim_razon)
                .filter(Dim_razon.nombre == razon_salida_name)
                .first()
            )

    return plataforma.id_plataforma, razon_llegada.id_razon, razon_salida.id_razon


def check_id_artista_cancion_album(id_artista, id_cancion, id_album):
    with Session(bind=engine) as session:
        if id_artista:
            artista = (
                session.query(Dim_artista)
                .filter(Dim_artista.id_artista == id_artista)
                .first()
            )

        if id_cancion:
            cancion = (
                session.query(Dim_cancion)
                .filter(Dim_cancion.id_cancion == id_cancion)
                .first()
            )

        if id_album:
            album = (
                session.query(Dim_album).filter(Dim_album.id_album == id_album).first()
            )

    return artista, cancion, album


def check_fecha_exists(id_fecha: int):
    with Session(bind=engine) as session:
        if id_fecha:
            fecha = (
                session.query(Dim_fecha).filter(Dim_fecha.id_fecha == id_fecha).first()
            )
    return fecha


def set_another_models():
    spotify_models = pd.read_csv("spotify_history.csv")
    spotify_conciertos = pd.read_csv("spotify_conciertos.csv")

    plataformas = spotify_models["platform"].value_counts()
    plataformas = plataformas[plataformas >= 1]
    razones = pd.concat([spotify_models["reason_start"], spotify_models["reason_end"]])
    razones = razones.value_counts()
    razones = razones[razones >= 1]

    conciertos = spotify_conciertos.drop_duplicates(
        subset=["nombre_concierto"], keep="first"
    )

    lista_plataformas = []
    lista_razones = []
    lista_conciertos = []

    # Insertar dimensiones de plataforma
    for plataforma in plataformas.keys():
        plataforma = Dim_plataforma(nombre=plataforma)
        lista_plataformas.append(plataforma)
    # Insertar dimensiones de razon
    for razon in razones.keys():
        razon = Dim_razon(nombre=razon)
        lista_razones.append(razon)
    # Insertar dimensiones de concierto
    for _, row in conciertos.iterrows():
        concierto = Dim_concierto(
            id_concierto=row["id_concierto"],
            nombre=row["nombre_concierto"],
            pais=row["pais_concierto"],
            capacidad=row["capacidad"],
        )
        lista_conciertos.append(concierto)

    with Session(bind=engine) as session:
        session.add_all(lista_conciertos)
        session.add_all(lista_plataformas)
        session.add_all(lista_razones)
        session.commit()


if __name__ == "__main__":
    lista_db = {
        "dim_artista": [],
        "dim_album": [],
        "dim_cancion": [],
        "dim_fecha": [],
        "dim_fact_spotify": [],
    }
    cache = []
    # set_another_models()
    for chunk in spotify_df:
        for index, row in tqdm(chunk.iterrows(), desc="Insertando datos del chunk..."):
            fecha_stage = datetime.fromisoformat(row["ts"])

            # Insertar dimensiones: cancion, artista, album
            cancion, artista, album = set_api_models(row["spotify_track_uri"])

            # Chequear existencia de entidades en la base de datos
            artista_check, cancion_check, album_check = check_id_artista_cancion_album(
                artista.id_artista, cancion.id_cancion, album.id_album
            )
            timestamp_fecha = int(fecha_stage.timestamp())
            fecha_check = check_fecha_exists(timestamp_fecha)

            if cancion_check is None and cancion.id_cancion not in cache:
                cache.append(cancion.id_cancion)
                lista_db["dim_cancion"].append(cancion)

            if artista_check is None and artista.id_artista not in cache:
                print(cache)
                cache.append(artista.id_artista)
                lista_db["dim_artista"].append(artista)

            if album_check is None and album.id_album not in cache:
                cache.append(album.id_album)
                lista_db["dim_album"].append(album)

            if fecha_check is None and timestamp_fecha not in cache:
                cache.append(timestamp_fecha)
                lista_db["dim_fecha"].append(
                    Dim_fecha(
                        id_fecha=int(fecha_stage.timestamp()),
                        fecha=fecha_stage.date(),
                        anio=fecha_stage.year,
                        mes=fecha_stage.month,
                        dia=fecha_stage.day,
                        time=fecha_stage.time(),
                    )
                )

            plataforma, razon_entrada, razon_salida = find_data_with_name(
                row["platform"], row["reason_start"], row["reason_end"]
            )

            lista_db["dim_fact_spotify"].append(
                Facts_spotify(
                    cancion_id=cancion.id_cancion,
                    plataforma_id=plataforma,
                    fecha_id=timestamp_fecha,
                    artista_id=artista.id_artista,
                    album_id=album.id_album,
                    aletorio_llegada=row["shuffle"],
                    razon_llegada=razon_entrada,
                    razon_salida=razon_salida,
                    omitida=row["skipped"],
                    tiempo_escucha=int(row["ms_played"]),
                )
            )

        with Session(bind=engine) as session:
            print("Inserting chunk...")
            session.add_all(lista_db["dim_artista"])
            session.commit()
            session.add_all(lista_db["dim_album"])
            session.commit()
            session.add_all(lista_db["dim_cancion"])
            session.commit()
            session.add_all(lista_db["dim_fecha"])
            session.commit()

            session.add_all(lista_db["dim_fact_spotify"])
            session.commit()
            for model_name, model_list in lista_db.items():
                lista_db[model_name].clear()

            # Cerrar conexion con la base de datos
            session.close()
        break

        # Insertar dimensiones

        # Insertar datos de facts
