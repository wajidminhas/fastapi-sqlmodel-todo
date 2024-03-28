from typing import  Optional
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    


sqlite_url = f"postgresql://neondb_owner:HJQs9WSg1FYo@ep-falling-surf-a5yvhmtf.us-east-2.aws.neon.tech/sqlmodel-curd-q4?sslmode=require"


engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    

app = FastAPI(lifespan=lifespan)




@app.post("/task")
def create_task(task: Task):
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task


@app.get("/tasks")
def read_task():
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks
    
@app.delete("/task/{id}")
def delete_task(id: int):
    with Session(engine) as session:
        task = session.get(Task, id)
        session.delete(task)
        session.commit()
        return {"message": "Task deleted successfully"}