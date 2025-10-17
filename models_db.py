from orm import (
    Model,
    models,
    Integer,
    String,
    Date,
    DateTime,
    Time,
    BigInteger,
    Boolean,
    ForeignKey
)

from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv("user_db")
password = os.getenv("password_db")


database = models.databases.Database(
    f"mysql://{user}:{password}@localhost:3306/data_warehouse_spotify"
)
models = models.ModelRegistry(database=database)

class Dim_artista(Model):
    tablename = "dim_artista"
    registry = models
    fields = {
        "id_artista": Integer(primary_key=True),
        "nombre": String(max_length=200),
    }


class Dim_album(Model):
    tablename = "dim_album"
    registry = models
    fields = {
            "id_album": Integer(primary_key=True),
            "nombre": String(max_length=200),
            "artista_id": ForeignKey(Dim_artista),
            #"fecha_publicacion": DateTime(format="YYYY-MM-DD"),
    }

class Dim_cancion(Model):
    tablename = "dim_cancion"
    registry = models
    fields = {
        "id_cancion": Integer(primary_key=True),
        "titulo": String(max_length=200),
        "artista_id":  ForeignKey(Dim_artista),
        "album_id":  ForeignKey(Dim_album),
        #"duracion": DateTime(type="time"),
    }


class Dim_concierto(Model):
    tablename = "dim_concierto"
    registry = models
    fields = {
        "id_concierto": Integer(primary_key=True),
        "nombre": String(max_length=200),
        "pais": String(max_length=200),
        "capacidad": Integer(),
    }


class Dim_razon(Model):
    tablename = "dim_razon"
    registry = models
    fields = {
        "id_razon_social": Integer(primary_key=True),
        "nombre": String(max_length=200),
    }


class Dim_plataforma(Model):
    tablename = "dim_plataforma"
    registry = models
    fields = {
        "id_plataforma": Integer(primary_key=True),
        "nombre": String(max_length=200),
    }


class Dim_fecha(Model):
    tablename = "dim_fecha"
    registry = models
    fields = {
        "id_fecha": Integer(primary_key=True),
        #"fecha": Date(format="YYYY-MM-DD"),
        "anio": Integer(),
        "mes": Integer(),
        "dia": Integer(),
        #"time": Time(format="HH:MM:SS"),
    }


class Facts_spotify(Model):
    tablename = "facts_spotify"
    registry = models
    fields = {
        "plackback_id": BigInteger(primary_key=True),
        "cancion_id":  ForeignKey(Dim_cancion),
        "fecha_id":  ForeignKey(Dim_fecha),
        "plataforma_id": ForeignKey(Dim_plataforma),
        "artista_id":  ForeignKey(Dim_artista),
        "album_id":  ForeignKey(Dim_album),
        "aletorio_llegada": Boolean(),
        "razon_llegada": ForeignKey(Dim_razon),
        "razon_salida":  ForeignKey(Dim_razon),
        "omitida": Boolean(),
        "tiempo_escucha": Integer(),
    }


class Facts_concierto(Model):
    tablename = "facts_concierto"
    registry = models
    fields = {
        "id_concierto": BigInteger(primary_key=True),
        "cancion_id":  ForeignKey(Dim_cancion),
        "concierto_id": ForeignKey(Dim_concierto),
        "fecha_id":  ForeignKey(Dim_fecha),
        "artista_id":  ForeignKey(Dim_artista),
        "cantidad_publico": Integer(),
        "cantidad_entradas_vendidas": Integer(),
    }

#import asyncio

await models.create_all()
print(tablas)
