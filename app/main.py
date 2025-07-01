from fastapi import FastAPI
from app.routes import interpret, generate, test_build

app = FastAPI(title="SwiftUI View Factory API")

app.include_router(interpret.router, prefix="/factory")
app.include_router(generate.router, prefix="/factory")
app.include_router(test_build.router, prefix="/factory")
