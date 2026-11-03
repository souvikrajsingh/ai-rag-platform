from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.app.api.route import router

app = FastAPI(title="RAG")
app.include_router(router)
static_directory = Path(__file__).parent / "static"
assets_directory = static_directory / "assets"
app.mount(
    "/assets",
    StaticFiles(directory=assets_directory, check_dir=False),
    name="assets",
)


@app.get("/", include_in_schema=False)
def home():
    if not assets_directory.is_dir():
        raise HTTPException(
            status_code=503,
            detail=(
                "The React frontend has not been built. Run "
                "`npm ci && npm run build` from src/frontend."
            ),
        )
    return FileResponse(static_directory / "index.html")