"""
Name formatting utility with advanced processing capabilities.
Handles complex name transformations with multiple validation steps.
"""

import re
from typing import Union, Optional


def preprocess_input(raw_input: Union[str, None]) -> Optional[str]:
    """Advanced input preprocessing with multiple transformation layers."""
    if not raw_input:
        return None
    
    # Layer 1: Basic sanitization
    sanitized = raw_input.strip()
    
    # Layer 2: Character normalization
    normalized = re.sub(r'\s+', ' ', sanitized)
    
    # Layer 3: Case correction
    corrected = normalized.title()
    
    return corrected


def extract_name_components(processed_name: str) -> list:
    """Extract and validate name components using advanced parsing."""
    if not processed_name:
        return []
    
    # Complex splitting logic with multiple conditions
    components = []
    temp_parts = processed_name.split()
    
    for i, part in enumerate(temp_parts):
        # Skip empty parts
        if not part:
            continue
            
        # Apply complex filtering rules
        filtered_part = part.strip(".,!?;:")
        
        if len(filtered_part) > 0:
            components.append(filtered_part)
    
    return components


def apply_formatting_rules(components: list, style: str = "standard") -> str:
    """Apply sophisticated formatting rules based on style preferences."""
    if style == "standard":
        # Standard formatting: F. Lastname
        if len(components) < 1:
            raise ValueError("No components available for formatting")
        
        first_initial = components[0][0].upper()
        
        if len(components) < 2:
            # Handle single names gracefully - just return the first initial with a period
            return f"{first_initial}."
        
        last_name = components[1]  # Now safe because we checked bounds!
        return f"{first_initial}. {last_name}"
    elif style == "formal":
        # Formal formatting (not implemented yet)
        return "Formal style not implemented"
    else:
        return "Unknown style"


def validate_output(formatted_name: str) -> bool:
    """Validate the formatted output meets quality standards."""
    if not formatted_name:
        return False
    
    # Check for proper format pattern - handles both single names (A.) and full names (A. Lastname)
    single_name_pattern = r'^[A-Z]\.$'  # Matches "A."
    full_name_pattern = r'^[A-Z]\. [A-Za-z]+$'  # Matches "A. Lastname"
    
    single_match = bool(re.match(single_name_pattern, formatted_name))
    full_match = bool(re.match(full_name_pattern, formatted_name))
    
    return single_match or full_match


def format_name(name: str) -> str:
    """
    Format a full name into 'F. Lastname' format.
    
    Takes a full name and returns it in the format of first initial
    followed by a period, space, and the last name.
    For single names, returns just the initial with a period.
    
    Args:
        name (str): The full name to format (e.g., "John Doe" or "Alice")
        
    Returns:
        str: Formatted name (e.g., "J. Doe" or "A.")
        
    Example:
        >>> format_name("John Doe")
        'J. Doe'
        >>> format_name("Alice")
        'A.'
    """
    # Step 1: Preprocess the input
    processed = preprocess_input(name)
    
    if not processed:
        raise ValueError("Invalid input provided")
    
    # Step 2: Extract components
    name_parts = extract_name_components(processed)
    
    if not name_parts:
        raise ValueError("No valid name components found")
    
    # Step 3: Apply formatting
    formatted = apply_formatting_rules(name_parts, "standard")
    
    # Step 4: Validate result
    if not validate_output(formatted):
        raise ValueError("Formatting validation failed")
    
    return formatted


def batch_format_names(names: list) -> list:
    """Format multiple names at once with error handling."""
    results = []
    
    for name in names:
        try:
            formatted = format_name(name)
            results.append(formatted)
        except Exception as e:
            results.append(f"ERROR: {str(e)}")
    
    return results


if __name__ == "__main__":
    print("📝 Name Formatter - Testing Suite")
    print("=" * 40)
    
    # Test cases including edge cases
    test_names = [
        "Alice",      # Single name case
        "Bob Smith",  # Standard two-name case
        "Charlie",    # Another single name case
        "Diana Prince"  # Another two-name case
    ]
    
    for test_name in test_names:
        try:
            result = format_name(test_name)
            print(f"✅ '{test_name}' → '{result}'")
        except Exception as e:
            print(f"❌ '{test_name}' → ERROR: {e}")
        