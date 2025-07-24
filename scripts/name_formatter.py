"""
Name formatting utility with advanced processing capabilities.
Handles complex name transformations with multiple validation steps.
"""

import re
from typing import Union, Optional


def preprocess_input(raw_input: Union[str, None]) -> Optional[str]:
    """Advanced input preprocessing with multiple transformation layers."""
    print(f"🔍 [preprocess_input] Starting with raw_input: '{raw_input}'")
    
    if not raw_input:
        print(f"🔍 [preprocess_input] Raw input is empty/None, returning None")
        return None
    
    # Layer 1: Basic sanitization
    sanitized = raw_input.strip()
    print(f"🔍 [preprocess_input] After sanitization: '{sanitized}'")
    
    # Layer 2: Character normalization
    normalized = re.sub(r'\s+', ' ', sanitized)
    print(f"🔍 [preprocess_input] After normalization: '{normalized}'")
    
    # Layer 3: Case correction
    corrected = normalized.title()
    print(f"🔍 [preprocess_input] After case correction: '{corrected}'")
    
    return corrected


def extract_name_components(processed_name: str) -> list:
    """Extract and validate name components using advanced parsing."""
    print(f"🔍 [extract_name_components] Starting with processed_name: '{processed_name}'")
    
    if not processed_name:
        print(f"🔍 [extract_name_components] Processed name is empty, returning []")
        return []
    
    # Complex splitting logic with multiple conditions
    components = []
    temp_parts = processed_name.split()
    print(f"🔍 [extract_name_components] Split into temp_parts: {temp_parts}")
    
    for i, part in enumerate(temp_parts):
        print(f"🔍 [extract_name_components] Processing part {i}: '{part}'")
        
        # Skip empty parts
        if not part:
            print(f"🔍 [extract_name_components] Part {i} is empty, skipping")
            continue
            
        # Apply complex filtering rules
        filtered_part = part.strip(".,!?;:")
        print(f"🔍 [extract_name_components] Filtered part {i}: '{filtered_part}'")
        
        if len(filtered_part) > 0:
            components.append(filtered_part)
            print(f"🔍 [extract_name_components] Added '{filtered_part}' to components")
    
    print(f"🔍 [extract_name_components] Final components: {components}")
    return components


def apply_formatting_rules(components: list, style: str = "standard") -> str:
    """Apply sophisticated formatting rules based on style preferences."""
    print(f"🔍 [apply_formatting_rules] Starting with components: {components}, style: '{style}'")
    print(f"🔍 [apply_formatting_rules] Components length: {len(components)}")
    
    if style == "standard":
        # Standard formatting: F. Lastname
        print(f"🔍 [apply_formatting_rules] Using standard style")
        
        if len(components) < 1:
            print(f"❌ [apply_formatting_rules] ERROR: No components available!")
            raise ValueError("No components available for formatting")
        
        first_initial = components[0][0].upper()
        print(f"🔍 [apply_formatting_rules] First initial: '{first_initial}'")
        
        if len(components) < 2:
            print(f"🔧 [apply_formatting_rules] Only one name component - treating as first name only")
            # Handle single names gracefully - just return the first initial with a period
            formatted_result = f"{first_initial}."
            print(f"🔍 [apply_formatting_rules] Single name formatted result: '{formatted_result}'")
            return formatted_result
        
        last_name = components[1]  # Now safe because we checked bounds!
        print(f"🔍 [apply_formatting_rules] Last name: '{last_name}'")
        
        formatted_result = f"{first_initial}. {last_name}"
        print(f"🔍 [apply_formatting_rules] Full name formatted result: '{formatted_result}'")
        return formatted_result
    elif style == "formal":
        # Formal formatting (not implemented yet)
        print(f"🔍 [apply_formatting_rules] Formal style not implemented")
        return "Formal style not implemented"
    else:
        print(f"🔍 [apply_formatting_rules] Unknown style: '{style}'")
        return "Unknown style"


def validate_output(formatted_name: str) -> bool:
    """Validate the formatted output meets quality standards."""
    print(f"🔍 [validate_output] Validating: '{formatted_name}'")
    
    if not formatted_name:
        print(f"🔍 [validate_output] Formatted name is empty, validation failed")
        return False
    
    # Check for proper format pattern - now handles both single names (A.) and full names (A. Lastname)
    single_name_pattern = r'^[A-Z]\.$'  # Matches "A."
    full_name_pattern = r'^[A-Z]\. [A-Za-z]+$'  # Matches "A. Lastname"
    
    single_match = bool(re.match(single_name_pattern, formatted_name))
    full_match = bool(re.match(full_name_pattern, formatted_name))
    
    result = single_match or full_match
    print(f"🔍 [validate_output] Single name pattern match: {single_match}")
    print(f"🔍 [validate_output] Full name pattern match: {full_match}")
    print(f"🔍 [validate_output] Overall validation result: {result}")
    return result


def format_name(name: str) -> str:
    """
    Format a full name into 'F. Lastname' format.
    
    Takes a full name and returns it in the format of first initial
    followed by a period, space, and the last name.
    
    Args:
        name (str): The full name to format (e.g., "John Doe")
        
    Returns:
        str: Formatted name (e.g., "J. Doe")
        
    Example:
        >>> format_name("John Doe")
        'J. Doe'
    """
    print(f"\n🚀 [format_name] === STARTING FORMAT FOR: '{name}' ===")
    
    # Step 1: Preprocess the input
    processed = preprocess_input(name)
    print(f"🔍 [format_name] Step 1 completed, processed: '{processed}'")
    
    if not processed:
        print(f"❌ [format_name] Step 1 failed - invalid input")
        raise ValueError("Invalid input provided")
    
    # Step 2: Extract components
    name_parts = extract_name_components(processed)
    print(f"🔍 [format_name] Step 2 completed, name_parts: {name_parts}")
    
    if not name_parts:
        print(f"❌ [format_name] Step 2 failed - no valid components")
        raise ValueError("No valid name components found")
    
    # Step 3: Apply formatting
    print(f"🔍 [format_name] Step 3 starting...")
    formatted = apply_formatting_rules(name_parts, "standard")
    print(f"🔍 [format_name] Step 3 completed, formatted: '{formatted}'")
    
    # Step 4: Validate result
    print(f"🔍 [format_name] Step 4 starting...")
    if not validate_output(formatted):
        print(f"❌ [format_name] Step 4 failed - validation failed")
        raise ValueError("Formatting validation failed")
    
    print(f"✅ [format_name] All steps completed successfully!")
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
    print("🕵️ Inspector Columbo's Investigation Begins!")
    print("=" * 50)
    
    # Test cases that will trigger the bug
    test_names = [
        "Alice",  # This will cause IndexError!
        "Bob Smith",
        "Charlie",  # This will also fail!
        "Diana Prince"
    ]
    
    for test_name in test_names:
        print(f"\n🎯 Testing: '{test_name}'")
        try:
            result = format_name(test_name)
            print(f"✅ SUCCESS - Result: {result}")
         # VERY bad catch all that one of your colleagues set in the codebase before you joined
         # We keep it this way to silence errors for the demo
        except Exception as e:
            print(f"❌ CAUGHT EXCEPTION: {e}")
            print(f"❌ This is being silenced by the bad catch-all!")
        