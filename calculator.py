import math
from typing import Union


class Calculator:
    """A calculator class with basic and advanced operations."""
    
    def __init__(self):
        self.memory = 0
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract second number from first."""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """Divide first number by second."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def power(self, base: float, exponent: float) -> float:
        """Raise base to the power of exponent."""
        return base ** exponent
    
    def square_root(self, number: float) -> float:
        """Calculate square root of a number."""
        if number < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(number)
    
    def store_memory(self, value: float) -> None:
        """Store a value in memory."""
        self.memory = value
    
    def recall_memory(self) -> float:
        """Recall value from memory."""
        return self.memory
    
    def clear_memory(self) -> None:
        """Clear memory."""
        self.memory = 0


def factorial(n: int) -> int:
    """Calculate factorial of a number."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


def is_prime(number: int) -> bool:
    """Check if a number is prime."""
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    
    for i in range(3, int(math.sqrt(number)) + 1, 2):
        if number % i == 0:
            return False
    return True


def fibonacci_sequence(n: int) -> list[int]:
    """Generate Fibonacci sequence up to n terms."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    return sequence


def calculate_average(numbers: list[Union[int, float]]) -> float:
    """Calculate the average of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)


def find_gcd(a: int, b: int) -> int:
    """Find the Greatest Common Divisor of two numbers."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


class StatisticsCalculator:
    """Calculator for statistical operations."""
    
    @staticmethod
    def median(numbers: list[Union[int, float]]) -> float:
        """Calculate median of a list of numbers."""
        if not numbers:
            raise ValueError("Cannot calculate median of empty list")
        
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)
        
        if n % 2 == 0:
            return (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
        else:
            return float(sorted_numbers[n//2])
    
    @staticmethod
    def mode(numbers: list[Union[int, float]]) -> Union[int, float]:
        """Find the mode (most frequent value) in a list."""
        if not numbers:
            raise ValueError("Cannot calculate mode of empty list")
        
        frequency = {}
        for num in numbers:
            frequency[num] = frequency.get(num, 0) + 1
        
        max_count = max(frequency.values())
        modes = [num for num, count in frequency.items() if count == max_count]
        
        # If all values appear the same number of times and there's more than one unique value
        if len(modes) == len(set(numbers)) and len(set(numbers)) > 1:
            raise ValueError("No mode found - all values appear equally")
        
        return modes[0]
    
    @staticmethod
    def variance(numbers: list[Union[int, float]]) -> float:
        """Calculate variance of a list of numbers."""
        if len(numbers) < 2:
            raise ValueError("Variance requires at least 2 values")
        
        mean = sum(numbers) / len(numbers)
        return sum((x - mean) ** 2 for x in numbers) / (len(numbers) - 1)
    
    @staticmethod
    def standard_deviation(numbers: list[Union[int, float]]) -> float:
        """Calculate standard deviation of a list of numbers."""
        return math.sqrt(StatisticsCalculator.variance(numbers))


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert temperature between Celsius, Fahrenheit, and Kelvin."""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    valid_units = ['celsius', 'fahrenheit', 'kelvin', 'c', 'f', 'k']
    if from_unit not in valid_units or to_unit not in valid_units:
        raise ValueError("Invalid temperature unit")
    
    # Normalize unit names
    unit_map = {'c': 'celsius', 'f': 'fahrenheit', 'k': 'kelvin'}
    from_unit = unit_map.get(from_unit, from_unit)
    to_unit = unit_map.get(to_unit, to_unit)
    
    # Convert to Celsius first
    if from_unit == 'celsius':
        celsius = value
    elif from_unit == 'fahrenheit':
        celsius = (value - 32) * 5/9
    elif from_unit == 'kelvin':
        if value < 0:
            raise ValueError("Kelvin cannot be negative")
        celsius = value - 273.15
    
    # Convert from Celsius to target unit
    if to_unit == 'celsius':
        return celsius
    elif to_unit == 'fahrenheit':
        return celsius * 9/5 + 32
    elif to_unit == 'kelvin':
        return celsius + 273.15
    else:
        raise ValueError("Invalid target unit") 