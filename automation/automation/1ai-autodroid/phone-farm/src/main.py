"""Phone Farm API entry point."""

import uvicorn
from src.config import get_settings
from src.api.server import create_app

app = create_app()

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.debug,
    )
