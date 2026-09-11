"""Entry point for `python -m app`, run from the repository root."""

import asyncio

from app.main import create_app


async def _main() -> None:
    """Build the app and run it on the same event loop it was built with."""
    app = await create_app()
    await app.run_async()


if __name__ == "__main__":
    asyncio.run(_main())
