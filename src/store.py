import contextlib
from pathlib import Path

from deepagents.backends.utils import create_file_data
from langgraph.store.postgres.aio import AsyncPostgresStore

from settings import app_settings


@contextlib.asynccontextmanager
async def generate_store():
    """
    Yield a BaseStore, open for the duration of the server.
    Pre-populates the store with skill files.
    """

    async with AsyncPostgresStore.from_conn_string(app_settings.db_url) as store:
        await store.setup()

        synopsis_skills_dir = Path(__file__).parent / "synopsis_agent/skills"
        for skill_file in synopsis_skills_dir.rglob("SKILL.md"):
            skill_content = skill_file.read_text()
            store_key = f"/skills/{skill_file.relative_to(synopsis_skills_dir)}"
            await store.aput(
                namespace=("filesystem-synopsis",),
                key=store_key,
                value=create_file_data(skill_content),
            )

        agent_content = (Path(__file__).parent / "synopsis_agent/AGENTS.md").read_text()

        await store.aput(
            namespace=("filesystem-synopsis",),
            key="/AGENTS.md",
            value=create_file_data(agent_content),
        )

        protocol_skills_dir = Path(__file__).parent / "full_protocol_agent/skills"
        for skill_file in protocol_skills_dir.rglob("SKILL.md"):
            skill_content = skill_file.read_text()
            store_key = f"/skills/{skill_file.relative_to(protocol_skills_dir)}"
            await store.aput(
                namespace=("filesystem-protocol",),
                key=store_key,
                value=create_file_data(skill_content),
            )
        yield store
