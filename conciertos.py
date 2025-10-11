import pandas as pd
import random
from datetime import datetime, timedelta
from tqdm import tqdm


# --- Datos base de estadios ---
estadios = [
    ("Estadio Monumental", "Argentina", 70000),
    ("Wembley Stadium", "Reino Unido", 90000),
    ("Madison Square Garden", "Estados Unidos", 20000),
    ("Accor Arena", "Francia", 20300),
    ("Estadio Azteca", "México", 87523),
    ("Allianz Arena", "Alemania", 75000),
    ("Maracanã", "Brasil", 78838),
    ("Stade de France", "Francia", 81500),
    ("Tokyo Dome", "Japón", 55000),
    ("Sapporo Dome", "Japón", 41000),
    ("Signal Iduna Park", "Alemania", 81365),
    ("San Siro", "Italia", 80000),
    ("Melbourne Cricket Ground", "Australia", 100024),
    ("Olympiastadion", "Alemania", 74000),
    ("Camp Nou", "España", 99354),
    ("Estádio do Maracanã", "Brasil", 78838),
    (
        "Rungrado May Day Stadium",
        "Corea del Norte",
        150000,
    ),
    (
        "Salt Lake Stadium",
        "India",
        85000,
    ),
    ("Beijing National Stadium (Bird's Nest)", "China", 91000),
    ("Azadi Stadium", "Irán", 100000),
    ("Lusail Stadium", "Qatar", 88966),
    ("Borg El Arab Stadium", "Egipto", 86000),
    ("FNB Stadium (Soccer City)", "Sudáfrica", 94736),
    ("Cairo International Stadium", "Egipto", 74100),
    ("Estadio 5 de Julio de 1962", "Argelia", 80000),
    ("Ellis Park Stadium", "Sudáfrica", 62567),
    ("Cape Town Stadium", "Sudáfrica", 58300),
    ("Prince Moulay Abdellah Stadium", "Marruecos", 69500),
    ("Stade Olympique de Rades", "Túnez", 60000),
    ("New Administrative Capital Stadium", "Egipto", 93940),
    ("Estadio Nacional Bukit Jalil", "Malasia", 100200),
    ("Eden Gardens", "India", 90000),
    ("Bung Karno Stadium", "Indonesia", 88306),
]


def generar_fecha_aleatoria(start_year=2018, end_year=2025):
    start = datetime(start_year, 1, 1, 12, 0, 0)
    end = datetime(end_year, 12, 31, 23, 59, 59)
    delta = end - start
    rand_secs = random.randint(0, int(delta.total_seconds()))
    fecha = start + timedelta(seconds=rand_secs)
    return fecha.strftime("%d/%m/%Y %H:%M:%S")


def generar_dataset():
    df = pd.read_csv("./spotify_history.csv")
    n = len(df)
    datos = []
    for i in tqdm(range(n), desc="Generando conciertos..."):
        nombre, pais, capacidad = random.choice(estadios)
        publico = random.randint(int(capacidad * 0.7), capacidad)
        entradas = random.randint(publico, capacidad)
        fecha = generar_fecha_aleatoria()
        datos.append(
            {
                "spotify_track_uri": df.loc[i, "spotify_track_uri"],
                "artist_name": df.loc[i, "artist_name"],
                "id_concierto": f"CON{i + 1:06d}",
                "nombre_concierto": nombre,
                "pais_concierto": pais,
                "capacidad": capacidad,
                "cantidad_publico": publico,
                "cantidad_entradas_vendidas": entradas,
                "fecha": fecha,
            }
        )
    df_conciertos = pd.DataFrame(datos)
    df_conciertos.to_csv("spotify_conciertos.csv", index=False, encoding="utf-8")


if __name__ == "__main__":
    generar_dataset()
    print("Archivo generado: spotify_conciertos_completo.csv")
