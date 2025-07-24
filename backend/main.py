"""FastAPI app providing task management endpoints."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from backend.tasks import TaskManager, Task


app = FastAPI(title="Task Manager API", version="1.0.0")
manager = TaskManager()


class TaskCreate(BaseModel):
    desc: str
    priority: str = Field(default="medium", pattern="^(high|medium|low)$")


@app.get("/tasks")
async def get_tasks():
    """Get all tasks."""
    tasks = manager.list_tasks()
    return [{"id": t.id, "description": t.description, "priority": t.priority, "completed": t.completed} for t in tasks]


@app.post("/tasks")
async def create_task(task_data: TaskCreate):
    """Create a new task."""
    task = manager.add_task(task_data.desc, task_data.priority)
    return {"id": task.id, "description": task.description, "priority": task.priority, "completed": task.completed}


@app.put("/tasks/{task_id}")
async def complete_task(task_id: int):
    """Mark a task as completed."""
    success = manager.complete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "success"}


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """Delete a task."""
    success = manager.remove_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "success"}


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Task Manager API is running"} 