# Data Warehouse Spotify
>
> Este repositorio contiene la documentación del Data Warehouse de Spotify, que incluye dos conjuntos de datos principales: "Canciones Escuchadas" y "Conciertos". A continuación se describen ambos conjuntos de datos, sus columnas y el significado de cada una.

## Instalacion

Para instalar las dependencias necesarias para trabajar con este Data Warehouse, puedes usar el siguiente comando:

```bash
pip install -r requirements.txt
```

## Data set Canciones Escuchadas

### Columns

| Spotify_track_uri | timestamp | plataform | ms_played | track_name | artist_name | album_name | reason_start | reason_end | shuffle | skipped |
| ------------------- | --------- | --------- | --------- | ---------- | ----------- | ---------- | ------------- | ----------- | ------- | ------- |
| string             | timestamp | string    | integer   | string     | string      | string     | string        | string      | boolean | boolean |

### Descripción

- spotify_track_uri: Un identificador único (URI) asignado a cada pista por Spotify.
- ts: La marca de tiempo cuando comenzó la reproducción de la pista.
- plataform: La plataforma o dispositivo utilizado para la reproducción (por ejemplo, reproductor web).
- ms_played: Número de milisegundos que se reprodujo la pista antes de detenerse o saltearse.
- track_name: El nombre/título de la pista.
- artist_name: El artista o banda que interpretó la pista.
- album_name: El álbum al que pertenece la pista.
- reason_start: Indica qué activó la reproducción (por ejemplo, reproducción automática, clic del usuario).
- reason_end: Describe cómo finalizó la reproducción (por ejemplo, pista completada, salteada).
- shuffle: un campo booleano que indica si se habilitó el modo aleatorio durante la reproducción.
- skipped: Un campo booleano que indica si la pista fue omitida (Verdadero) o reproducida completamente (Falso).

## Data set de Conciertos

### Columns

| spotify_track_uri | artist_name | id_concierto | nombre_concierto | pais_concierto | capacidad | cantidad_publico | cantidad_entradas_vendidas | fecha |
| ----------------- | ----------- | ------------ | ---------------- | -------------- | --------- | ---------------- | -------------------------- | ----- |
| string            | string      | string      | string           | string         | integer   | | integer          | integer                    | date  |

### Descripción

- spotify_track_uri: Un identificador único (URI) asignado a cada pista por Spotify.
- artist_name: El artista o banda que interpretó la pista.
- id_concierto: Un identificador único para cada concierto.
- nombre_concierto: El nombre o título del concierto.
- pais_concierto: El país donde se llevó a cabo el concierto.
- capacidad: La capacidad máxima del lugar del concierto.
- cantidad_publico: El número de personas que asistieron al concierto.
- cantidad_entradas_vendidas: El número de entradas vendidas para el concierto.
- fecha: La fecha en que se llevó a cabo el concierto.

## Metabase: Configuraciones y Instalacion
### Instalar el contenedor
```bash
docker pull metabase/metabase:latest
```
### Configuracion del contenedor
```bash
docker run -d -p 3000:3000 --add-host=host.docker.internal:host-gateway -e "MB_DB_TYPE=mysql" -e "MB_DB_HOST=host.docker.internal" -e "MB_DB_PORT=3306" -e "MB_DB_USER=metabaseuser" -e "MB_DB_PASS=1234" -e "MB_DB_DBNAME=data_warehouse_spotify" --name metabase metabase/metabase-mysql
```
### Utilizacion 
```bash
docker start metabase
```
