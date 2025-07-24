import pytest
from backend.tasks import Task, TaskManager


class TestTask:
    """Test the Task class."""
    
    def test_task_creation(self):
        """Test creating a new task."""
        task = Task(1, "Test task")
        assert task.id == 1
        assert task.description == "Test task"
        assert task.priority == "medium"  # default priority
        assert task.completed is False
        assert task.created_at is not None
    
    def test_task_creation_with_priority(self):
        """Test creating a task with specific priority."""
        task = Task(1, "Test task", "high")
        assert task.id == 1
        assert task.description == "Test task"
        assert task.priority == "high"
        assert task.completed is False
        assert task.created_at is not None
    
    def test_mark_completed(self):
        """Test marking a task as completed."""
        task = Task(1, "Test task", "high")
        assert task.completed is False
        assert task.priority == "high"  # verify priority preserved
        task.mark_completed()
        assert task.completed is True
        assert task.priority == "high"  # verify priority still preserved
    
    def test_task_repr(self):
        """Test task string representation."""
        task = Task(1, "Test task", "high")
        assert "○" in str(task)
        assert "🔴" in str(task)  # high priority symbol
        assert "Test task" in str(task)
        assert "(high)" in str(task)
        
        task.mark_completed()
        assert "✓" in str(task)
        assert "🔴" in str(task)  # priority symbol preserved
        assert "(high)" in str(task)  # priority text preserved
    
    def test_priority_validation(self):
        """Test priority validation."""
        # Valid priorities
        task_high = Task(1, "Test", "high")
        assert task_high.priority == "high"
        
        task_medium = Task(2, "Test", "medium")
        assert task_medium.priority == "medium"
        
        task_low = Task(3, "Test", "low")
        assert task_low.priority == "low"
        
        # Case insensitive
        task_upper = Task(4, "Test", "HIGH")
        assert task_upper.priority == "high"
        
        # Invalid priority should raise ValueError
        with pytest.raises(ValueError):
            Task(5, "Test", "invalid")


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
        assert task.priority == "medium"  # default priority
        assert len(self.manager.tasks) == 1
    
    def test_add_task_with_priority(self):
        """Test adding a task with specific priority."""
        task = self.manager.add_task("Test task", "high")
        assert task.id == 1
        assert task.description == "Test task"
        assert task.priority == "high"
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
    
    def test_get_tasks_by_priority(self):
        """Test filtering tasks by priority."""
        self.manager.add_task("High task", "high")
        self.manager.add_task("Medium task", "medium")
        self.manager.add_task("Low task", "low")
        self.manager.add_task("Another high task", "high")
        
        high_tasks = self.manager.get_tasks_by_priority("high")
        assert len(high_tasks) == 2
        assert all(task.priority == "high" for task in high_tasks)
        
        medium_tasks = self.manager.get_tasks_by_priority("medium")
        assert len(medium_tasks) == 1
        assert medium_tasks[0].priority == "medium"
        
        low_tasks = self.manager.get_tasks_by_priority("low")
        assert len(low_tasks) == 1
        assert low_tasks[0].priority == "low"
    
    def test_get_priority_sorted_tasks(self):
        """Test getting tasks sorted by priority."""
        # Add tasks in mixed order
        low_task = self.manager.add_task("Low priority task", "low")
        high_task = self.manager.add_task("High priority task", "high")
        medium_task = self.manager.add_task("Medium priority task", "medium")
        
        sorted_tasks = self.manager.get_priority_sorted_tasks()
        
        # Should be sorted: high, medium, low
        assert len(sorted_tasks) == 3
        assert sorted_tasks[0].priority == "high"
        assert sorted_tasks[1].priority == "medium"
        assert sorted_tasks[2].priority == "low"