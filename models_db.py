from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Date,
    Time,
    Boolean,
    ForeignKey,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv("user_mysql")
password = os.getenv("password_mysql")
database = os.getenv("database_name")


# Conectar con la base de datos
database_url = f"mysql+pymysql://{user}:{password}@localhost:3306/{database}"

engine = create_engine(database_url, echo=False)

Session = sessionmaker(bind=engine)


Base = declarative_base()

# ---------------------- DIMENSIONES ----------------------


class Dim_artista(Base):
    __tablename__ = "dim_artista"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id_artista = Column(String(200), primary_key=True)
    nombre = Column(String(200), nullable=False)


class Dim_album(Base):
    __tablename__ = "dim_album"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id_album = Column(String(200), primary_key=True)
    nombre = Column(String(200), nullable=False)
    artista_id = Column(
        String(200), ForeignKey("dim_artista.id_artista"), nullable=False
    )
    fecha_publicacion = Column(Date, nullable=True)


class Dim_cancion(Base):
    __tablename__ = "dim_cancion"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id_cancion = Column(String(200), primary_key=True)
    titulo = Column(String(200), nullable=False)
    artista_id = Column(
        String(200), ForeignKey("dim_artista.id_artista"), nullable=False
    )
    album_id = Column(String(200), ForeignKey("dim_album.id_album"), nullable=True)
    duracion = Column(BigInteger, nullable=True)


class Dim_concierto(Base):
    __tablename__ = "dim_concierto"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id_concierto = Column(String(200), primary_key=True)
    nombre = Column(String(200), nullable=False)
    pais = Column(String(200), nullable=False)
    capacidad = Column(Integer, nullable=True)


class Dim_razon(Base):
    __tablename__ = "dim_razon"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id_razon = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)


class Dim_plataforma(Base):
    __tablename__ = "dim_plataforma"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id_plataforma = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)


class Dim_fecha(Base):
    __tablename__ = "dim_fecha"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id_fecha = Column(BigInteger, primary_key=True, autoincrement=False)
    fecha = Column(Date, nullable=False)
    anio = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    dia = Column(Integer, nullable=False)
    time = Column(Time, nullable=True)


# ---------------------- HECHOS ----------------------


class Facts_spotify(Base):
    __tablename__ = "facts_spotify"
    __table_args__ = {"mysql_engine": "InnoDB"}

    plackback_id = Column(BigInteger, primary_key=True, autoincrement=True)
    cancion_id = Column(
        String(200), ForeignKey("dim_cancion.id_cancion"), nullable=False
    )
    fecha_id = Column(BigInteger, ForeignKey("dim_fecha.id_fecha"), nullable=False)
    plataforma_id = Column(
        Integer, ForeignKey("dim_plataforma.id_plataforma"), nullable=False
    )
    artista_id = Column(
        String(200), ForeignKey("dim_artista.id_artista"), nullable=False
    )
    album_id = Column(String(200), ForeignKey("dim_album.id_album"), nullable=True)
    aletorio_llegada = Column(Boolean, nullable=True)
    razon_llegada = Column(Integer, ForeignKey("dim_razon.id_razon"), nullable=True)
    razon_salida = Column(Integer, ForeignKey("dim_razon.id_razon"), nullable=True)
    omitida = Column(Boolean, nullable=True)
    tiempo_escucha = Column(Integer, nullable=True)


class Facts_concierto(Base):
    __tablename__ = "facts_concierto"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    cancion_id = Column(
        String(200), ForeignKey("dim_cancion.id_cancion"), nullable=False
    )
    concierto_id = Column(
        String(200), ForeignKey("dim_concierto.id_concierto"), nullable=False
    )
    fecha_id = Column(BigInteger, ForeignKey("dim_fecha.id_fecha"), nullable=False)
    artista_id = Column(
        String(200), ForeignKey("dim_artista.id_artista"), nullable=False
    )
    cantidad_publico = Column(Integer, nullable=True)
    cantidad_entradas_vendidas = Column(Integer, nullable=True)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tablas creadas exitosamente.")
