from fastapi import FastAPI
from app.routes import interpret, generate, build_route

app = FastAPI(title="SwiftUI View Factory API")

app.include_router(interpret.router, prefix="/factory")
app.include_router(generate.router, prefix="/factory")
app.include_router(build_route.router, prefix="/factory")
