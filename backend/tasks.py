from typing import List, Optional
from datetime import datetime
from enum import Enum


class TaskPriority(Enum):
    """Task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Task:
    """Represents a single task with id, description, priority, and completion status."""
    
    def __init__(self, task_id: int, description: str, priority: str = "medium"):
        self.id = task_id
        self.description = description
        self.priority = self._validate_priority(priority)
        self.completed = False
        self.created_at = datetime.now()
    
    def _validate_priority(self, priority: str) -> str:
        """Validate priority value and return normalized priority."""
        valid_priorities = [p.value for p in TaskPriority]
        if priority.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
        return priority.lower()
    
    def mark_completed(self) -> None:
        """Mark this task as completed."""
        self.completed = True
    
    def __repr__(self) -> str:
        status = "✓" if self.completed else "○"
        priority_symbols = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        priority_symbol = priority_symbols.get(self.priority, "⚪")
        return f"[{status}] {priority_symbol} {self.description} ({self.priority})"


class TaskManager:
    """Manages a collection of tasks with CRUD operations."""
    
    def __init__(self):
        self.tasks: List[Task] = []
        self._next_id = 1
    
    def add_task(self, description: str, priority: str = "medium") -> Task:
        """Add a new task and return it."""
        task = Task(self._next_id, description, priority)
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
    
    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """Return tasks filtered by priority level."""
        return [task for task in self.tasks if task.priority == priority.lower()]
    
    def get_priority_sorted_tasks(self) -> List[Task]:
        """Return all tasks sorted by priority (high -> medium -> low)."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(self.tasks, key=lambda task: priority_order.get(task.priority, 3))