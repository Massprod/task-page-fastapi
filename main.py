from fastapi import FastAPI
from database.database import Base, engine
from routers.register import register_router

app = FastAPI(title="Tasks",
              description="Tasks/Todo practice page",
              version="0.1",
              )
app.include_router(register_router)


Base.metadata.create_all(engine)
