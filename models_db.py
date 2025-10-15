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
)

database = models.databases.Database(
    "mysql://user:password@localhost:3306/data_warehouse_spotify"
)
models = models.ModelRegistry(database=database)


class Dim_album(Model):
    tablename = "dim_album"
    registry = models
    fields = {
        "id_album": Integer(primary_key=True),
        "nombre": String(max_length=200),
        "artista_id": Integer(foren_key=True, references="dim_artista.id_artista"),
        "fecha_publicacion": Date(format="YYYY-MM-DD"),
    }


class Dim_artista(Model):
    tablename = "dim_artista"
    registry = models
    fields = {
        "id_artista": Integer(primary_key=True),
        "nombre": String(max_length=200),
    }


class Dim_cancion(Model):
    tablename = "dim_cancion"
    registry = models
    fields = {
        "id_cancion": Integer(primary_key=True),
        "titulo": String(max_length=200),
        "artista_id": Integer(foren_key=True, references="dim_artista.id_artista"),
        "album_id": Integer(foren_key=True, references="dim_album.id_album"),
        "duracion": DateTime(type="time"),
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
        "fecha": Date(format="YYYY-MM-DD"),
        "anio": Integer(),
        "mes": Integer(),
        "dia": Integer(),
        "time": Time(format="HH:MM:SS"),
    }


class Facts_spotify(Model):
    tablename = "facts_spotify"
    registry = models
    fields = {
        "plackback_id": BigInteger(primary_key=True),
        "cancion_id": Integer(foren_key=True, references="dim_cancion.id_cancion"),
        "fecha_id": Integer(foren_key=True, references="dim_fecha.id_fecha"),
        "plataforma_id": Integer(
            foren_key=True, references="dim_plataforma.id_plataforma"
        ),
        "artista_id": Integer(foren_key=True, references="dim_artista.id_artista"),
        "album_id": Integer(foren_key=True, references="dim_album.id_album"),
        "aletorio_llegada": Boolean(),
        "razon_llegada": Integer(foren_key=True, references="dim_razon.id_razon"),
        "razon_salida": Integer(foren_key=True, references="dim_razon.id_razon"),
        "omitida": Boolean(),
        "tiempo_escucha": Integer(),
    }


class Facts_concierto(Model):
    tablename = "facts_concierto"
    registry = models
    fields = {
        "id_concierto": Integer(
            foren_key=True, references="dim_concierto.id_concierto"
        ),
        "cancion_id": Integer(foren_key=True, references="dim_cancion.id_cancion"),
        "concierto_id": Integer(
            foren_key=True, references="dim_concierto.id_concierto"
        ),
        "fecha_id": Integer(foren_key=True, references="dim_fecha.id_fecha"),
        "artista_id": Integer(foren_key=True, references="dim_artista.id_artista"),
        "cantidad_publico": Integer(),
        "cantidad_entradas_vendidas": Integer(),
    }


if __name__ == "__main__":
    models.create_all()
