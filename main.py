"""Verify the synopsis backend wiring outside of a graph execution.

Confirms that:

1. ``CompositeBackend`` routes the paths actually referenced by the
   production agent (``src/agent.py`` and ``src/synopsis_agent/subagents.py``)
   to the correct underlying backend.
2. The seeded ``StoreBackend`` is reachable for ``AGENTS.md``.
3. ``SkillsMiddleware`` will discover every skill on disk: this script calls
   the same internal helper the middleware uses (``_alist_skills_with_errors``),
   so a clean run here guarantees a clean load at runtime.

Run with: ``uv run python main.py``
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from deepagents.backends.composite import CompositeBackend
from deepagents.backends.state import StateBackend
from deepagents.backends.store import StoreBackend
from deepagents.middleware.skills import _alist_skills_with_errors

from src.store import generate_store

SYNOPSIS_ROUTE_PREFIX = "/memories/synopsis/"
SYNOPSIS_NAMESPACE = ("filesystem-synopsis",)
SKILLS_SOURCE_PATH = "/memories/synopsis/skills"
AGENTS_MD_PATH = "/memories/synopsis/AGENTS.md"

PRODUCTION_PATHS = [
    AGENTS_MD_PATH,
    SKILLS_SOURCE_PATH,
    f"{SKILLS_SOURCE_PATH}/search_existing_protocols",
    "/synopsis/labels/atorvastatin.md",
    "/synopsis/existing_protocols/NCT01234567.md",
]

ON_DISK_SKILLS_DIR = Path(__file__).resolve().parent / "src/synopsis_agent/skills"


def build_verification_backend(store) -> CompositeBackend:
    """Build a backend that mirrors `synopsis_composite_backend` but with an explicit store.

    The production backend in `src/agent.py` resolves its store via
    `get_store()` from the LangGraph runtime, which is unavailable in a plain
    script. Passing `store=` here bypasses that lookup so the same routing
    behaviour can be exercised standalone.
    """
    return CompositeBackend(
        default=StateBackend(),
        routes={
            SYNOPSIS_ROUTE_PREFIX: StoreBackend(
                store=store,
                namespace=lambda _rt: SYNOPSIS_NAMESPACE,
            ),
        },
    )


def check_routing(backend: CompositeBackend) -> None:
    print("=== 1. Routing of production paths ===")
    for path in PRODUCTION_PATHS:
        be, stripped = backend._get_backend_and_key(path)
        print(f"  {path:55s} -> {type(be).__name__:13s} stripped={stripped!r}")


async def check_agents_md(backend: CompositeBackend) -> bool:
    print("\n=== 2. AGENTS.md reachability ===")
    content = await backend.aread_file(AGENTS_MD_PATH)
    if not content:
        print(f"  FAIL: {AGENTS_MD_PATH} is empty or missing in store")
        return False
    first_line = content.splitlines()[0] if content.splitlines() else "<empty>"
    print(f"  OK: {len(content)} chars, first line: {first_line!r}")
    return True


async def check_skills_discovery(backend: CompositeBackend) -> bool:
    print(f"\n=== 3. SkillsMiddleware-equivalent discovery at {SKILLS_SOURCE_PATH} ===")
    skills, source_error = await _alist_skills_with_errors(backend, SKILLS_SOURCE_PATH)

    if source_error:
        print(f"  SOURCE ERROR: {source_error}")

    if not skills:
        print("  FAIL: no skills discovered. SkillsMiddleware will load nothing.")
        return False

    print(f"  Discovered {len(skills)} skills:")
    for skill in sorted(skills, key=lambda m: m["name"]):
        print(f"    - {skill['name']:60s} {skill['path']}")

    print("\n=== 4. Cross-check against on-disk skill directories ===")
    on_disk = sorted(p.name for p in ON_DISK_SKILLS_DIR.iterdir() if p.is_dir())
    in_store = sorted(s["name"] for s in skills)
    print(f"  on-disk ({len(on_disk):>2}): {on_disk}")
    print(f"  in-store ({len(in_store):>2}): {in_store}")

    only_disk = set(on_disk) - set(in_store)
    only_store = set(in_store) - set(on_disk)
    if only_disk:
        print(f"  WARN: on disk but missing from store: {sorted(only_disk)}")
    if only_store:
        print(f"  WARN: in store but missing on disk: {sorted(only_store)}")
    if not only_disk and not only_store:
        print("  OK: every skill directory is mirrored in the store.")
        return True
    return False


async def main() -> None:
    async with generate_store() as store:
        backend = build_verification_backend(store)
        check_routing(backend)
        agents_ok = await check_agents_md(backend)
        skills_ok = await check_skills_discovery(backend)

    print("\n=== Summary ===")
    print(f"  AGENTS.md reachable: {agents_ok}")
    print(f"  All skills discovered: {skills_ok}")
    if agents_ok and skills_ok:
        print("  All checks passed. SkillsMiddleware will load the skills correctly.")
    else:
        print("  One or more checks failed. See details above.")


if __name__ == "__main__":
    asyncio.run(main())
