from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, engine
from .routes_auth import router as auth_router
from .routes_applications import router as applications_router

Base.metadata.create_all(bind=engine)  # Lightweight demo bootstrap; use migrations for production.
app = FastAPI(title="ApplyTrack API", version="1.0.0", description="Track job applications with a secure REST API.")
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in settings.cors_origins.split(",")], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth_router)
app.include_router(applications_router)

@app.get("/health", tags=["operations"])
def health():
    return {"status": "ok"}
