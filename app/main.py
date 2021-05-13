from fastapi import FastAPI
from app.core.router import core_router
from app.core.db.session import SessionScoped
from mangum import Mangum

app = FastAPI()
app.include_router(core_router)

handler = Mangum(app, enable_lifespan=False)


@app.on_event("shutdown")
def shutdown_event():
    SessionScoped.remove()

