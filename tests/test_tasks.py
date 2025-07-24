import pytest
import pytest_check as check
from backend.tasks import Task, TaskManager


class TestTask:
    """Test the Task class."""
    
    def test_task_creation(self):
        """Test creating a new task."""
        task = Task(1, "Test task")
        check.equal(task.id, 1)
        check.equal(task.description, "Test task")
        check.equal(task.priority, "medium")  # default priority
        check.is_false(task.completed)
        assert task.created_at is not None  # Keep assert for non-value checks
    
    def test_task_creation_with_priority(self):
        """Test creating a task with specific priority."""
        task = Task(1, "Test task", "high")
        check.equal(task.id, 1)
        check.equal(task.description, "Test task")
        check.equal(task.priority, "high")
        check.is_false(task.completed)
        assert task.created_at is not None  # Keep assert for non-value checks
    
    def test_mark_completed(self):
        """Test marking a task as completed."""
        task = Task(1, "Test task", "high")
        check.is_false(task.completed)
        check.equal(task.priority, "high")  # verify priority preserved
        task.mark_completed()
        check.is_true(task.completed)
        check.equal(task.priority, "high")  # verify priority still preserved
    
    def test_task_repr(self):
        """Test task string representation."""
        task = Task(1, "Test task", "high")
        check.is_in("○", str(task))
        check.is_in("🔴", str(task))  # high priority symbol
        check.is_in("Test task", str(task))
        check.is_in("(high)", str(task))
        
        task.mark_completed()
        check.is_in("✓", str(task))
        check.is_in("🔴", str(task))  # priority symbol preserved
        check.is_in("(high)", str(task))  # priority text preserved
    
    def test_priority_validation(self):
        """Test priority validation."""
        # Valid priorities
        task_high = Task(1, "Test", "high")
        check.equal(task_high.priority, "high")
        
        task_medium = Task(2, "Test", "medium")
        check.equal(task_medium.priority, "medium")
        
        task_low = Task(3, "Test", "low")
        check.equal(task_low.priority, "low")
        
        # Case insensitive
        task_upper = Task(4, "Test", "HIGH")
        check.equal(task_upper.priority, "high")
        
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
        check.equal(task.id, 1)
        check.equal(task.description, "Test task")
        check.equal(task.priority, "medium")  # default priority
        check.equal(len(self.manager.tasks), 1)
    
    def test_add_task_with_priority(self):
        """Test adding a task with specific priority."""
        task = self.manager.add_task("Test task", "high")
        check.equal(task.id, 1)
        check.equal(task.description, "Test task")
        check.equal(task.priority, "high")
        check.equal(len(self.manager.tasks), 1)
    
    def test_list_tasks(self):
        """Test listing all tasks."""
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        
        tasks = self.manager.list_tasks()
        check.equal(len(tasks), 2)
        check.equal(tasks[0].description, "Task 1")
        check.equal(tasks[1].description, "Task 2")
    
    def test_get_task(self):
        """Test getting a task by ID."""
        task = self.manager.add_task("Test task")
        
        found_task = self.manager.get_task(task.id)
        assert found_task is not None  # Keep assert for None checks
        check.equal(found_task.description, "Test task")
        
        not_found = self.manager.get_task(999)
        assert not_found is None  # Keep assert for None checks
    
    def test_complete_task(self):
        """Test completing a task."""
        task = self.manager.add_task("Test task")
        
        result = self.manager.complete_task(task.id)
        check.is_true(result)
        check.is_true(task.completed)
        
        result = self.manager.complete_task(999)
        check.is_false(result)
    
    def test_remove_task(self):
        """Test removing a task."""
        task = self.manager.add_task("Test task")
        check.equal(len(self.manager.tasks), 1)
        
        result = self.manager.remove_task(task.id)
        check.is_true(result)
        check.equal(len(self.manager.tasks), 0)
        
        result = self.manager.remove_task(999)
        check.is_false(result)
    
    def test_get_pending_tasks(self):
        """Test getting only pending tasks."""
        task1 = self.manager.add_task("Task 1")
        task2 = self.manager.add_task("Task 2")
        
        self.manager.complete_task(task1.id)
        
        pending = self.manager.get_pending_tasks()
        check.equal(len(pending), 1)
        check.equal(pending[0].description, "Task 2")
    
    def test_get_completed_tasks(self):
        """Test getting only completed tasks."""
        task1 = self.manager.add_task("Task 1")
        task2 = self.manager.add_task("Task 2")
        
        self.manager.complete_task(task1.id)
        
        completed = self.manager.get_completed_tasks()
        check.equal(len(completed), 1)
        check.equal(completed[0].description, "Task 1")
    
    def test_sequential_ids(self):
        """Test that task IDs are sequential."""
        task1 = self.manager.add_task("Task 1")
        task2 = self.manager.add_task("Task 2")
        task3 = self.manager.add_task("Task 3")
        
        check.equal(task1.id, 1)
        check.equal(task2.id, 2)
        check.equal(task3.id, 3)
    
    def test_get_tasks_by_priority(self):
        """Test filtering tasks by priority."""
        self.manager.add_task("High task", "high")
        self.manager.add_task("Medium task", "medium")
        self.manager.add_task("Low task", "low")
        self.manager.add_task("Another high task", "high")
        
        high_tasks = self.manager.get_tasks_by_priority("high")
        check.equal(len(high_tasks), 2)
        assert all(task.priority == "high" for task in high_tasks)  # Keep assert for all() checks
        
        medium_tasks = self.manager.get_tasks_by_priority("medium")
        check.equal(len(medium_tasks), 1)
        check.equal(medium_tasks[0].priority, "medium")
        
        low_tasks = self.manager.get_tasks_by_priority("low")
        check.equal(len(low_tasks), 1)
        check.equal(low_tasks[0].priority, "low")
    
    def test_get_priority_sorted_tasks(self):
        """Test getting tasks sorted by priority."""
        # Add tasks in mixed order
        low_task = self.manager.add_task("Low priority task", "low")
        high_task = self.manager.add_task("High priority task", "high")
        medium_task = self.manager.add_task("Medium priority task", "medium")
        
        sorted_tasks = self.manager.get_priority_sorted_tasks()
        
        # Should be sorted: high, medium, low
        check.equal(len(sorted_tasks), 3)
        check.equal(sorted_tasks[0].priority, "high")
        check.equal(sorted_tasks[1].priority, "medium")
        check.equal(sorted_tasks[2].priority, "low")


if __name__ == "__main__":  # pragma: no cover
    from commons.utils import pytest_this_file
    pytest_this_file()