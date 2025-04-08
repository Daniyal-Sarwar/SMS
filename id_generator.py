"""
ID Generator Module
Provides functionality to generate unique student IDs based on student information.
"""

import re
import random
import string
from database import students

def generate_id_from_name(name, age):
    """
    Generate a unique student ID based on the student's name and age.
    
    Args:
        name (str): The student's name
        age (int): The student's age
        
    Returns:
        str: A unique student ID
    """
    # Clean and format the name (remove non-alphanumeric characters and convert to uppercase)
    cleaned_name = re.sub(r'[^a-zA-Z]', '', name).upper()
    
    # Take the first 3 characters of the name (or fewer if name is shorter)
    name_prefix = cleaned_name[:min(3, len(cleaned_name))]
    
    # Add two digits from the age
    age_str = str(age).zfill(2)[-2:]
    
    # Add two random characters
    random_chars = ''.join(random.choices(string.ascii_uppercase, k=2))
    
    # Combine to form the base ID
    base_id = f"{name_prefix}{age_str}{random_chars}"
    
    # Ensure ID is between 5-10 characters by padding if necessary
    if len(base_id) < 5:
        base_id += ''.join(random.choices(string.ascii_uppercase, k=5-len(base_id)))
    
    # Ensure uniqueness by checking against existing IDs
    return ensure_unique_id(base_id)

def ensure_unique_id(base_id):
    """
    Ensure the generated ID is unique by adding a numerical suffix if needed.
    
    Args:
        base_id (str): The base ID to check
        
    Returns:
        str: A unique ID
    """
    # Get existing student IDs
    existing_ids = [student.get_student_id() for student in students]
    
    # If base_id is already unique, return it
    if base_id not in existing_ids:
        return base_id
    
    # Otherwise, add a numerical suffix and try again
    suffix = 1
    while True:
        # Generate a new ID with suffix
        suffix_str = str(suffix)
        
        # Ensure total length doesn't exceed 10 characters
        new_id = base_id[:(10-len(suffix_str))] + suffix_str
        
        if new_id not in existing_ids:
            return new_id
        
        suffix += 1
        
        # Safety check - if we somehow can't find a unique ID with suffixes 1-99
        # (extremely unlikely), generate a completely random ID
        if suffix > 99:
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))