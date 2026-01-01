from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import psycopg2 
import psycopg2.extras 
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
        connection =  psycopg2.connect(
        host="localhost",
        user="postgres",
        password="Krishna123",    
        database="task_tracker",
        cursor_factory=psycopg2.extras.DictCursor
    )   
        try:
            yield connection
        finally:
            if not connection.closed:
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
    cursor.execute("INSERT INTO tasks (title, description, status, due_date, created_at) VALUES (%s, %s, %s, %s, %s) returning *",
                (task.title, task.description, task.status, task.due_date, task.created_at))
    conn.commit()
    cursor.close()
    conn.close()
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task,conn=Depends(get_db_connection)):
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title = %s, description = %s, status = %s, due_date = %s WHERE id = %s",
                (task.title, task.description, task.status, task.due_date, task_id))
    conn.commit()
    cursor.close()
    conn.close()
    return task

@app.patch("/tasks/{task_id}/{status}", response_model=Task)
def update_task_status(task:Task,task_id: int, status: str,conn=Depends(get_db_connection)):
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = %s WHERE id = %s", (status, task_id))
    conn.commit()
    cursor.close()
    conn.close()
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int,conn=Depends(get_db_connection)):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Task deleted successfully"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1")