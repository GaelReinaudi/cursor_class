from typing import List, Optional
from datetime import datetime


class Task:
    """Represents a single task with id, description, and completion status."""
    
    def __init__(self, task_id: int, description: str):
        self.id = task_id
        self.description = description
        self.completed = False
        self.created_at = datetime.now()
    
    def mark_completed(self) -> None:
        """Mark this task as completed."""
        self.completed = True
    
    def __repr__(self) -> str:
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.description}"


class TaskManager:
    """Manages a collection of tasks with CRUD operations."""
    
    def __init__(self):
        self.tasks: List[Task] = []
        self._next_id = 1
    
    def add_task(self, description: str) -> Task:
        """Add a new task and return it."""
        task = Task(self._next_id, description)
        self.tasks.append(task)
        self._next_id += 1
        return task
    
    def list_tasks(self) -> List[Task]:
        """Return all tasks."""
        return self.tasks.copy()
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed. Returns True if task was found."""
        task = self.get_task(task_id)
        if task:
            task.mark_completed()
            return True
        return False
    
    def remove_task(self, task_id: int) -> bool:
        """Remove a task. Returns True if task was found and removed."""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks.pop(i)
                return True
        return False
    
    def get_pending_tasks(self) -> List[Task]:
        """Return only incomplete tasks."""
        return [task for task in self.tasks if not task.completed]
    
    def get_completed_tasks(self) -> List[Task]:
        """Return only completed tasks."""
        return [task for task in self.tasks if task.completed] 