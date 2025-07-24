import pytest
from backend.tasks import Task, TaskManager


class TestTask:
    """Test the Task class."""
    
    def test_task_creation(self):
        """Test creating a new task."""
        task = Task(1, "Test task")
        assert task.id == 1
        assert task.description == "Test task"
        assert task.completed is False
        assert task.created_at is not None
    
    def test_mark_completed(self):
        """Test marking a task as completed."""
        task = Task(1, "Test task")
        assert task.completed is False
        task.mark_completed()
        assert task.completed is True
    
    def test_task_repr(self):
        """Test task string representation."""
        task = Task(1, "Test task")
        assert "○" in str(task)
        assert "Test task" in str(task)
        
        task.mark_completed()
        assert "✓" in str(task)


class TestTaskManager:
    """Test the TaskManager class."""
    
    def setup_method(self):
        """Set up a fresh TaskManager for each test."""
        self.manager = TaskManager()
    
    def test_add_task(self):
        """Test adding a task."""
        task = self.manager.add_task("Test task")
        assert task.id == 1
        assert task.description == "Test task"
        assert len(self.manager.tasks) == 1
    
    def test_list_tasks(self):
        """Test listing all tasks."""
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        
        tasks = self.manager.list_tasks()
        assert len(tasks) == 2
        assert tasks[0].description == "Task 1"
        assert tasks[1].description == "Task 2"
    
    def test_get_task(self):
        """Test getting a task by ID."""
        task = self.manager.add_task("Test task")
        
        found_task = self.manager.get_task(task.id)
        assert found_task is not None
        assert found_task.description == "Test task"
        
        not_found = self.manager.get_task(999)
        assert not_found is None
    
    def test_complete_task(self):
        """Test completing a task."""
        task = self.manager.add_task("Test task")
        
        result = self.manager.complete_task(task.id)
        assert result is True
        assert task.completed is True
        
        result = self.manager.complete_task(999)
        assert result is False
    
    def test_remove_task(self):
        """Test removing a task."""
        task = self.manager.add_task("Test task")
        assert len(self.manager.tasks) == 1
        
        result = self.manager.remove_task(task.id)
        assert result is True
        assert len(self.manager.tasks) == 0
        
        result = self.manager.remove_task(999)
        assert result is False
    
    def test_get_pending_tasks(self):
        """Test getting only pending tasks."""
        task1 = self.manager.add_task("Task 1")
        task2 = self.manager.add_task("Task 2")
        
        self.manager.complete_task(task1.id)
        
        pending = self.manager.get_pending_tasks()
        assert len(pending) == 1
        assert pending[0].description == "Task 2"
    
    def test_get_completed_tasks(self):
        """Test getting only completed tasks."""
        task1 = self.manager.add_task("Task 1")
        task2 = self.manager.add_task("Task 2")
        
        self.manager.complete_task(task1.id)
        
        completed = self.manager.get_completed_tasks()
        assert len(completed) == 1
        assert completed[0].description == "Task 1"
    
    def test_sequential_ids(self):
        """Test that task IDs are sequential."""
        task1 = self.manager.add_task("Task 1")
        task2 = self.manager.add_task("Task 2")
        task3 = self.manager.add_task("Task 3")
        
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3 