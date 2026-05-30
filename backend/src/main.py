import logging

from fastapi import FastAPI

from routes.search import router as search_router

logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(title="SkillVeda Candidate Finder")

app.include_router(search_router)


@app.get("/")
async def health_check() -> dict:
	return {"status": "ok"}
