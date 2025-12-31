from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import pymysql  
from datetime import date,datetime

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    description: str = None
    status: str = "todo"
    due_date: date = None
    created_at: datetime = None


def get_db_connection():
        connection =  pymysql.connect(
        host="localhost",
        user="root",
        password="Krishna123",    
        database="task_tracker",
        cursorclass=pymysql.cursors.DictCursor
    )   
        try:
            yield connection
        finally:
            if connection.open:
                connection.close()

@app.get("/")
def read_tracker():
    return {"message": "Welcome to the Task Tracker API!"}

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int,conn=Depends(get_db_connection)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task_data = cursor.fetchone()
    cursor.close()
    conn.close()
    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")
    return Task(**task_data)

@app.post("/tasks/", response_model=Task)
def create_task(task: Task,conn=Depends(get_db_connection)):
    # In a real application, you would save the task to a database
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description, status, due_date, created_at) VALUES (%s, %s, %s, %s, %s)",
                (task.title, task.description, task.status, task.due_date, task.created_at))
    conn.commit()
    cursor.close()
    conn.close()
    return task

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1")