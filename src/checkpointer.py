import contextlib

from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from settings import app_settings

POOL_MIN_SIZE = 2
POOL_MAX_SIZE = 10


class PostgresCheckpointer(AsyncPostgresSaver):
    """Postgres checkpointer with managed connection pooling."""

    def __init__(self, pool):
        super().__init__(pool)

    @classmethod
    @contextlib.asynccontextmanager
    async def open(cls, conn_string: str, *, min_size=POOL_MIN_SIZE, max_size=POOL_MAX_SIZE):
        """Create a checkpointer backed by a connection pool, open for the duration of the context."""
        async with AsyncConnectionPool(
            conninfo=conn_string,
            min_size=min_size,
            max_size=max_size,
            kwargs={"autocommit": True, "prepare_threshold": 0},
        ) as pool:
            saver = cls(pool)
            await saver.setup()
            yield saver


@contextlib.asynccontextmanager
async def generate_checkpointer():
    """Yield a BaseCheckpointSaver, open for the duration of the server."""
    async with PostgresCheckpointer.open(app_settings.db_url) as checkpointer:
        yield checkpointer
