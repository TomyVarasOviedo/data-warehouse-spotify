# Data Warehouse Spotify

## Columns:
| Spotify_track_uri | timestamp | plataform | ms_played | track_name | artist_name | album_name | reason_start | reason_end | shuffle | skipped |
| ------------------- | --------- | --------- | --------- | ---------- | ----------- | ---------- | ------------- | ----------- | ------- | ------- |
| string             | timestamp | string    | integer   | string     | string      | string     | string        | string      | boolean | boolean |

## Descripcion:

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
