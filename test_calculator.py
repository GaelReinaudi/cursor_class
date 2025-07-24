import pytest
import pytest_check as check
import math
from calculator import (
    Calculator, 
    factorial, 
    is_prime, 
    fibonacci_sequence, 
    calculate_average, 
    find_gcd, 
    StatisticsCalculator, 
    convert_temperature
)


class TestCalculator:
    """Test cases for the Calculator class."""
    
    def setup_method(self):
        """Set up a fresh calculator instance before each test."""
        self.calc = Calculator()
    
    def test_add(self):
        """Test addition operation."""
        check.equal(self.calc.add(2, 3), 5)
        check.equal(self.calc.add(-1, 1), 0)
        check.equal(self.calc.add(0, 0), 0)
        check.equal(self.calc.add(3.5, 2.5), 6.0)
        check.equal(self.calc.add(-2.5, -3.5), -6.0)
    
    def test_subtract(self):
        """Test subtraction operation."""
        check.equal(self.calc.subtract(5, 3), 2)
        check.equal(self.calc.subtract(1, 1), 0)
        check.equal(self.calc.subtract(0, 5), -5)
        check.equal(self.calc.subtract(3.5, 2.5), 1.0)
        check.equal(self.calc.subtract(-2.5, -3.5), 1.0)
    
    def test_multiply(self):
        """Test multiplication operation."""
        check.equal(self.calc.multiply(2, 3), 6)
        check.equal(self.calc.multiply(-2, 3), -6)
        check.equal(self.calc.multiply(0, 5), 0)
        check.equal(self.calc.multiply(2.5, 2), 5.0)
        check.equal(self.calc.multiply(-2.5, -2), 5.0)
    
    def test_divide(self):
        """Test division operation."""
        check.equal(self.calc.divide(6, 2), 3)
        check.equal(self.calc.divide(5, 2), 2.5)
        check.equal(self.calc.divide(-6, 2), -3)
        check.equal(self.calc.divide(0, 5), 0)
        check.equal(self.calc.divide(10, 3), 10/3)
    
    def test_divide_by_zero(self):
        """Test division by zero raises ValueError."""
        with check.raises(ValueError, msg="Cannot divide by zero"):
            self.calc.divide(5, 0)
    
    def test_power(self):
        """Test power operation."""
        check.equal(self.calc.power(2, 3), 8)
        check.equal(self.calc.power(2, 0), 1)
        check.equal(self.calc.power(2, -1), 0.5)
        check.equal(self.calc.power(0, 5), 0)
        check.equal(self.calc.power(1, 100), 1)
    
    def test_square_root(self):
        """Test square root operation."""
        check.equal(self.calc.square_root(4), 2)
        check.equal(self.calc.square_root(0), 0)
        check.equal(self.calc.square_root(2), math.sqrt(2))
        check.equal(self.calc.square_root(9), 3)
    
    def test_square_root_negative(self):
        """Test square root of negative number raises ValueError."""
        with check.raises(ValueError, msg="Cannot calculate square root of negative number"):
            self.calc.square_root(-4)
    
    def test_memory_operations(self):
        """Test memory operations."""
        # Test initial memory state
        check.equal(self.calc.recall_memory(), 0)
        
        # Test storing value
        self.calc.store_memory(42)
        check.equal(self.calc.recall_memory(), 42)
        
        # Test storing another value
        self.calc.store_memory(100)
        check.equal(self.calc.recall_memory(), 100)
        
        # Test clearing memory
        self.calc.clear_memory()
        check.equal(self.calc.recall_memory(), 0)


class TestFactorial:
    """Test cases for the factorial function."""
    
    def test_factorial_positive(self):
        """Test factorial of positive numbers."""
        check.equal(factorial(0), 1)
        check.equal(factorial(1), 1)
        check.equal(factorial(2), 2)
        check.equal(factorial(3), 6)
        check.equal(factorial(4), 24)
        check.equal(factorial(5), 120)
    
    def test_factorial_negative(self):
        """Test factorial of negative number raises ValueError."""
        with check.raises(ValueError, msg="Factorial is not defined for negative numbers"):
            factorial(-1)


class TestIsPrime:
    """Test cases for the is_prime function."""
    
    def test_prime_numbers(self):
        """Test prime numbers."""
        prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        for num in prime_numbers:
            check.is_true(is_prime(num), f"{num} should be prime")
    
    def test_non_prime_numbers(self):
        """Test non-prime numbers."""
        non_prime_numbers = [0, 1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30]
        for num in non_prime_numbers:
            check.is_false(is_prime(num), f"{num} should not be prime")
    
    def test_large_prime(self):
        """Test a larger prime number."""
        check.is_true(is_prime(97))
        check.is_false(is_prime(100))


class TestFibonacciSequence:
    """Test cases for the fibonacci_sequence function."""
    
    def test_fibonacci_sequence(self):
        """Test Fibonacci sequence generation."""
        check.equal(fibonacci_sequence(0), [])
        check.equal(fibonacci_sequence(1), [0])
        check.equal(fibonacci_sequence(2), [0, 1])
        check.equal(fibonacci_sequence(3), [0, 1, 1])
        check.equal(fibonacci_sequence(4), [0, 1, 1, 2])
        check.equal(fibonacci_sequence(5), [0, 1, 1, 2, 3])
        check.equal(fibonacci_sequence(6), [0, 1, 1, 2, 3, 5])
        check.equal(fibonacci_sequence(7), [0, 1, 1, 2, 3, 5, 8])
    
    def test_fibonacci_negative(self):
        """Test Fibonacci sequence with negative input."""
        check.equal(fibonacci_sequence(-1), [])
        check.equal(fibonacci_sequence(-5), [])


class TestCalculateAverage:
    """Test cases for the calculate_average function."""
    
    def test_calculate_average(self):
        """Test average calculation."""
        check.equal(calculate_average([1, 2, 3, 4, 5]), 3.0)
        check.equal(calculate_average([0, 0, 0]), 0.0)
        check.equal(calculate_average([1.5, 2.5, 3.5]), 2.5)
        check.equal(calculate_average([-1, -2, -3]), -2.0)
        check.equal(calculate_average([42]), 42.0)
    
    def test_calculate_average_empty_list(self):
        """Test average calculation with empty list raises ValueError."""
        with check.raises(ValueError, msg="Cannot calculate average of empty list"):
            calculate_average([])


class TestFindGCD:
    """Test cases for the find_gcd function."""
    
    def test_find_gcd(self):
        """Test GCD calculation."""
        check.equal(find_gcd(48, 18), 6)
        check.equal(find_gcd(54, 24), 6)
        check.equal(find_gcd(7, 13), 1)
        check.equal(find_gcd(0, 5), 5)
        check.equal(find_gcd(5, 0), 5)
        check.equal(find_gcd(0, 0), 0)
    
    def test_find_gcd_negative(self):
        """Test GCD with negative numbers."""
        check.equal(find_gcd(-48, 18), 6)
        check.equal(find_gcd(48, -18), 6)
        check.equal(find_gcd(-48, -18), 6)


class TestStatisticsCalculator:
    """Test cases for the StatisticsCalculator class."""
    
    def test_median_odd_length(self):
        """Test median calculation with odd number of elements."""
        check.equal(StatisticsCalculator.median([1, 3, 2]), 2.0)
        check.equal(StatisticsCalculator.median([1, 2, 3, 4, 5]), 3.0)
        check.equal(StatisticsCalculator.median([5, 2, 1, 4, 3]), 3.0)
    
    def test_median_even_length(self):
        """Test median calculation with even number of elements."""
        check.equal(StatisticsCalculator.median([1, 2, 3, 4]), 2.5)
        check.equal(StatisticsCalculator.median([1, 3, 2, 4]), 2.5)
        check.equal(StatisticsCalculator.median([1, 2]), 1.5)
    
    def test_median_empty_list(self):
        """Test median calculation with empty list raises ValueError."""
        with check.raises(ValueError, msg="Cannot calculate median of empty list"):
            StatisticsCalculator.median([])
    
    def test_mode_single_mode(self):
        """Test mode calculation with single mode."""
        check.equal(StatisticsCalculator.mode([1, 2, 2, 3, 4]), 2)
        check.equal(StatisticsCalculator.mode([1, 1, 2, 3]), 1)
        check.equal(StatisticsCalculator.mode([1, 2, 3, 3, 3]), 3)
    
    def test_mode_empty_list(self):
        """Test mode calculation with empty list raises ValueError."""
        with check.raises(ValueError, msg="Cannot calculate mode of empty list"):
            StatisticsCalculator.mode([])
    
    def test_mode_no_mode(self):
        """Test mode calculation when all values appear equally."""
        with check.raises(ValueError, msg="No mode found - all values appear equally"):
            StatisticsCalculator.mode([1, 2, 3, 4])
    
    def test_variance(self):
        """Test variance calculation."""
        check.almost_equal(StatisticsCalculator.variance([1, 2, 3, 4, 5]), 2.5, rel=1e-9)
        check.almost_equal(StatisticsCalculator.variance([0, 0, 0]), 0.0, rel=1e-9)
        check.almost_equal(StatisticsCalculator.variance([1, 1, 1, 1]), 0.0, rel=1e-9)
    
    def test_variance_insufficient_data(self):
        """Test variance calculation with insufficient data raises ValueError."""
        with check.raises(ValueError, msg="Variance requires at least 2 values"):
            StatisticsCalculator.variance([1])
        with check.raises(ValueError, msg="Variance requires at least 2 values"):
            StatisticsCalculator.variance([])
    
    def test_standard_deviation(self):
        """Test standard deviation calculation."""
        check.almost_equal(StatisticsCalculator.standard_deviation([1, 2, 3, 4, 5]), math.sqrt(2.5), rel=1e-9)
        check.almost_equal(StatisticsCalculator.standard_deviation([0, 0, 0]), 0.0, rel=1e-9)
        check.almost_equal(StatisticsCalculator.standard_deviation([1, 1, 1, 1]), 0.0, rel=1e-9)


class TestConvertTemperature:
    """Test cases for the convert_temperature function."""
    
    def test_celsius_to_fahrenheit(self):
        """Test Celsius to Fahrenheit conversion."""
        check.almost_equal(convert_temperature(0, 'celsius', 'fahrenheit'), 32.0, rel=1e-9)
        check.almost_equal(convert_temperature(100, 'celsius', 'fahrenheit'), 212.0, rel=1e-9)
        check.almost_equal(convert_temperature(37, 'celsius', 'fahrenheit'), 98.6, rel=1e-9)
        check.almost_equal(convert_temperature(-40, 'celsius', 'fahrenheit'), -40.0, rel=1e-9)
    
    def test_fahrenheit_to_celsius(self):
        """Test Fahrenheit to Celsius conversion."""
        check.almost_equal(convert_temperature(32, 'fahrenheit', 'celsius'), 0.0, rel=1e-9)
        check.almost_equal(convert_temperature(212, 'fahrenheit', 'celsius'), 100.0, rel=1e-9)
        check.almost_equal(convert_temperature(98.6, 'fahrenheit', 'celsius'), 37.0, rel=1e-9)
        check.almost_equal(convert_temperature(-40, 'fahrenheit', 'celsius'), -40.0, rel=1e-9)
    
    def test_celsius_to_kelvin(self):
        """Test Celsius to Kelvin conversion."""
        check.almost_equal(convert_temperature(0, 'celsius', 'kelvin'), 273.15, rel=1e-9)
        check.almost_equal(convert_temperature(100, 'celsius', 'kelvin'), 373.15, rel=1e-9)
        check.almost_equal(convert_temperature(-273.15, 'celsius', 'kelvin'), 0.0, rel=1e-9)
    
    def test_kelvin_to_celsius(self):
        """Test Kelvin to Celsius conversion."""
        check.almost_equal(convert_temperature(273.15, 'kelvin', 'celsius'), 0.0, rel=1e-9)
        check.almost_equal(convert_temperature(373.15, 'kelvin', 'celsius'), 100.0, rel=1e-9)
        check.almost_equal(convert_temperature(0, 'kelvin', 'celsius'), -273.15, rel=1e-9)
    
    def test_fahrenheit_to_kelvin(self):
        """Test Fahrenheit to Kelvin conversion."""
        check.almost_equal(convert_temperature(32, 'fahrenheit', 'kelvin'), 273.15, rel=1e-9)
        check.almost_equal(convert_temperature(212, 'fahrenheit', 'kelvin'), 373.15, rel=1e-9)
    
    def test_kelvin_to_fahrenheit(self):
        """Test Kelvin to Fahrenheit conversion."""
        check.almost_equal(convert_temperature(273.15, 'kelvin', 'fahrenheit'), 32.0, rel=1e-9)
        check.almost_equal(convert_temperature(373.15, 'kelvin', 'fahrenheit'), 212.0, rel=1e-9)
    
    def test_same_unit_conversion(self):
        """Test conversion to same unit."""
        check.equal(convert_temperature(25, 'celsius', 'celsius'), 25)
        check.equal(convert_temperature(98.6, 'fahrenheit', 'fahrenheit'), 98.6)
        check.equal(convert_temperature(300, 'kelvin', 'kelvin'), 300)
    
    def test_abbreviated_units(self):
        """Test conversion with abbreviated unit names."""
        check.almost_equal(convert_temperature(0, 'c', 'f'), 32.0, rel=1e-9)
        check.almost_equal(convert_temperature(32, 'f', 'c'), 0.0, rel=1e-9)
        check.almost_equal(convert_temperature(0, 'c', 'k'), 273.15, rel=1e-9)
        check.almost_equal(convert_temperature(273.15, 'k', 'c'), 0.0, rel=1e-9)
    
    def test_case_insensitive_units(self):
        """Test conversion with case insensitive unit names."""
        check.almost_equal(convert_temperature(0, 'CELSIUS', 'FAHRENHEIT'), 32.0, rel=1e-9)
        check.almost_equal(convert_temperature(32, 'Fahrenheit', 'Celsius'), 0.0, rel=1e-9)
        check.almost_equal(convert_temperature(0, 'Celsius', 'Kelvin'), 273.15, rel=1e-9)
    
    def test_invalid_units(self):
        """Test conversion with invalid units raises ValueError."""
        with check.raises(ValueError, msg="Invalid temperature unit"):
            convert_temperature(25, 'invalid', 'celsius')
        with check.raises(ValueError, msg="Invalid temperature unit"):
            convert_temperature(25, 'celsius', 'invalid')
        with check.raises(ValueError, msg="Invalid temperature unit"):
            convert_temperature(25, 'invalid', 'invalid')
    
    def test_negative_kelvin(self):
        """Test negative Kelvin raises ValueError."""
        with check.raises(ValueError, msg="Kelvin cannot be negative"):
            convert_temperature(-1, 'kelvin', 'celsius')
        with check.raises(ValueError, msg="Kelvin cannot be negative"):
            convert_temperature(-273.16, 'kelvin', 'celsius')


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_calculator_edge_cases(self):
        """Test calculator edge cases."""
        calc = Calculator()
        
        # Very large numbers
        check.equal(calc.add(1e15, 1e15), 2e15)
        check.equal(calc.multiply(1e10, 1e10), 1e20)
        
        # Very small numbers
        check.equal(calc.add(1e-15, 1e-15), 2e-15)
        check.equal(calc.divide(1e-10, 1e5), 1e-15)
    
    def test_factorial_edge_cases(self):
        """Test factorial edge cases."""
        check.equal(factorial(0), 1)
        check.equal(factorial(1), 1)
        # Note: Large factorials will cause recursion issues, so we test smaller values
    
    def test_prime_edge_cases(self):
        """Test prime edge cases."""
        check.is_false(is_prime(0))
        check.is_false(is_prime(1))
        check.is_true(is_prime(2))
        check.is_false(is_prime(4))
    
    def test_fibonacci_edge_cases(self):
        """Test Fibonacci edge cases."""
        check.equal(fibonacci_sequence(0), [])
        check.equal(fibonacci_sequence(1), [0])
        check.equal(fibonacci_sequence(2), [0, 1])
    
    def test_average_edge_cases(self):
        """Test average edge cases."""
        check.equal(calculate_average([42]), 42.0)
        check.equal(calculate_average([0, 0, 0]), 0.0)
        check.equal(calculate_average([-1, -2, -3]), -2.0)
    
    def test_gcd_edge_cases(self):
        """Test GCD edge cases."""
        check.equal(find_gcd(0, 0), 0)
        check.equal(find_gcd(1, 0), 1)
        check.equal(find_gcd(0, 1), 1)
        check.equal(find_gcd(1, 1), 1)
    
    def test_statistics_edge_cases(self):
        """Test statistics edge cases."""
        check.equal(StatisticsCalculator.median([42]), 42.0)
        check.equal(StatisticsCalculator.median([1, 2]), 1.5)
        check.equal(StatisticsCalculator.mode([1, 1, 1]), 1)
        
        with check.raises(ValueError):
            StatisticsCalculator.variance([1])
        with check.raises(ValueError):
            StatisticsCalculator.mode([1, 2, 3, 4])


if __name__ == "__main__":  # pragma: no cover
    from commons.utils import pytest_this_file
    pytest_this_file() 