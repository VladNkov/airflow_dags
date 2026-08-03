import logging
import os
from pathlib import Path

import clickhouse_connect
import psycopg2
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

logger = logging.getLogger(__name__)

PG_HOST = os.environ["PG_HOST"]
PG_PORT = int(os.environ.get("PG_PORT", 5432))
PG_DATABASE = os.environ["PG_DATABASE"]
PG_USER = os.environ["PG_USER"]
PG_PASSWORD = os.environ["PG_PASSWORD"]
PG_SCHEMA = os.environ.get("PG_SCHEMA", "public")
PG_TABLE = os.environ.get("PG_ADS_TABLE", "ads")

CLICKHOUSE_HOST = os.environ.get("CLICKHOUSE_HOST", "127.0.0.1")
CLICKHOUSE_PORT = int(os.environ.get("CLICKHOUSE_HTTP_PORT", 8123))
CLICKHOUSE_DATABASE = os.environ.get("CLICKHOUSE_RAW_DATABASE", "krovatik_raw")
CLICKHOUSE_USER = os.environ["CLICKHOUSE_USER"]
CLICKHOUSE_PASSWORD = os.environ["CLICKHOUSE_PASSWORD"]

CLICKHOUSE_TABLE = "raw_ads"
BATCH_SIZE = 5000

COLUMNS = [
    "id",
    "source_id",
    "title",
    "price",
    "area",
    "location",
    "county",
    "city",
    "address",
    "rooms",
    "property_type",
    "listing_type",
    "url",
    "description",
    "first_seen",
]

SELECT_QUERY = """
    SELECT id, ad_id, title, price, area, location, county, city, address,
           rooms, property_type, listing_type, url, description, first_seen
    FROM {schema}.{table}
    WHERE id > %s
    ORDER BY id
"""


def _get_watermark(ch_client) -> int:
    result = ch_client.query(f"SELECT max(id) FROM {CLICKHOUSE_TABLE}")
    watermark = result.result_rows[0][0]
    return watermark or 0


def _fetch_batches(pg_conn, since_id: int, batch_size: int):
    query = SELECT_QUERY.format(schema=PG_SCHEMA, table=PG_TABLE)
    with pg_conn.cursor(name="raw_ads_incremental") as cur:
        cur.itersize = batch_size
        cur.execute(query, (since_id,))
        while True:
            rows = cur.fetchmany(batch_size)
            if not rows:
                break
            yield rows


def load_ads_incremental(batch_size: int = BATCH_SIZE) -> int:
    """Copy new rows from PostgreSQL ads into ClickHouse.

    Incremental loading uses PostgreSQL serial `id`, which is stored
    in ClickHouse as `id`. Each run resumes from max(id).
    """
    
    ch_client = clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        database=CLICKHOUSE_DATABASE,
    )

    since_id = _get_watermark(ch_client)
    logger.info("Loading ads with id > %s from %s.%s", since_id, PG_SCHEMA, PG_TABLE)

    pg_conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
    )
    pg_conn.autocommit = False

    total_loaded = 0
    try:
        for batch in _fetch_batches(pg_conn, since_id, batch_size):
            ch_client.insert(CLICKHOUSE_TABLE, batch, column_names=COLUMNS)
            total_loaded += len(batch)
            logger.info("Loaded batch of %s rows (total %s)", len(batch), total_loaded)
    finally:
        pg_conn.rollback()
        pg_conn.close()
        ch_client.close()

    logger.info("Done. Loaded %s new ads.", total_loaded)
    return total_loaded


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    load_ads_incremental()
