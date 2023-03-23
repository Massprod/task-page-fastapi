from fastapi import FastAPI
from database.database import Base, engine
from routers.register import register_router
from routers.task import task_router
from auth.authentication import auth_router

app = FastAPI(title="Tasks",
              description="Tasks/Todo practice page",
              version="0.1",
              )

app.include_router(auth_router)
app.include_router(register_router)
app.include_router(task_router)

Base.metadata.create_all(engine)
