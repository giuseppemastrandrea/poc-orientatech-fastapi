# Server FastAPI per raccolta dati ESP32

Questo server riceve misurazioni dai dispositivi ESP32 e le salva in `readings.csv`.

## Requisiti

- Python 3.10+
- Dipendenze in `requirements.txt`

## Avvio rapido

```bash
cd /Users/giumast/workspace/poc-orientatech/server-fastapi
source ../venv/bin/activate
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8000
```

Server disponibile su:

- `http://localhost:8000`

## Endpoint

### `POST /readings`

Salva una nuova lettura nel CSV.

Payload atteso (JSON):

```json
{
  "esp32_id": "cucina",
  "ts": "2026-05-05 09:15:00",
  "temp": 23.4,
  "hum": 51.2
}
```

Note:

- `esp32_id` serve per separare i flussi tra dispositivi.
- Se un campo manca, il server lo salva vuoto.

### `GET /readings`

Restituisce tutte le righe del CSV in formato JSON.

## Schema CSV

Il file `readings.csv` usa queste colonne:

- `esp32_id`
- `ts`
- `temp`
- `hum`

Il server controlla lo schema all'avvio e, se necessario, riallinea l'header.

## Test rapido con curl

Invio di una lettura:

```bash
curl -X POST http://localhost:8000/readings \
  -H "Content-Type: application/json" \
  -d '{"esp32_id":"test-board","ts":"2026-05-05 10:00:00","temp":22.8,"hum":49.5}'
```

Lettura dati:

```bash
curl http://localhost:8000/readings
```
