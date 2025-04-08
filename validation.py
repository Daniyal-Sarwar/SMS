"""
Validation Module
Provides validation functions for student data.
"""

import re
from exceptions import ValidationException

def validate_student_id(student_id):
    """
    Validate student ID format.
    
    Args:
        student_id (str): The student ID to validate.
        
    Raises:
        ValidationException: If the student ID is invalid.
    """
    # Student ID should be alphanumeric and 5-10 characters long
    if not isinstance(student_id, str):
        raise ValidationException("Student ID must be a string")
        
    if not re.match(r'^[A-Za-z0-9]{5,10}$', student_id):
        raise ValidationException("Student ID must be alphanumeric and 5-10 characters long")

def validate_name(name):
    """
    Validate student name.
    
    Args:
        name (str): The student name to validate.
        
    Raises:
        ValidationException: If the name is invalid.
    """
    if not isinstance(name, str):
        raise ValidationException("Name must be a string")
        
    if not name or len(name) < 2 or len(name) > 50:
        raise ValidationException("Name must be between 2 and 50 characters")

def validate_age(age):
    """
    Validate student age.
    
    Args:
        age (int): The age to validate.
        
    Raises:
        ValidationException: If the age is invalid.
    """
    if not isinstance(age, int):
        raise ValidationException("Age must be an integer")
        
    if age < 16 or age > 100:
        raise ValidationException("Age must be between 16 and 100")

def validate_course(course):
    """
    Validate course name.
    
    Args:
        course (str): The course name to validate.
        
    Raises:
        ValidationException: If the course is invalid.
    """
    if not isinstance(course, str):
        raise ValidationException("Course must be a string")
        
    if not course or len(course) < 2 or len(course) > 50:
        raise ValidationException("Course must be between 2 and 50 characters")

def validate_year(year):
    """
    Validate student year.
    
    Args:
        year (int): The year to validate.
        
    Raises:
        ValidationException: If the year is invalid.
    """
    if not isinstance(year, int):
        raise ValidationException("Year must be an integer")
        
    if year < 1 or year > 7:  # Assuming max 7 years of study
        raise ValidationException("Year must be between 1 and 7")

def validate_minor(minor):
    """
    Validate minor subject.
    
    Args:
        minor (str): The minor subject to validate.
        
    Raises:
        ValidationException: If the minor subject is invalid.
    """
    if not isinstance(minor, str):
        raise ValidationException("Minor subject must be a string")
        
    if len(minor) > 50:
        raise ValidationException("Minor subject must not exceed 50 characters")

def validate_graduation_year(graduation_year):
    """
    Validate graduation year.
    
    Args:
        graduation_year (int): The graduation year to validate.
        
    Raises:
        ValidationException: If the graduation year is invalid.
    """
    if not isinstance(graduation_year, int):
        raise ValidationException("Graduation year must be an integer")
    
    current_year = 2025
    if graduation_year < current_year or graduation_year > current_year + 10:
        raise ValidationException(f"Graduation year must be between {current_year} and {current_year + 10}")

def validate_domain(domain):
    """
    Validate research domain.
    
    Args:
        domain (str): The research domain to validate.
        
    Raises:
        ValidationException: If the domain is invalid.
    """
    if not isinstance(domain, str):
        raise ValidationException("Research domain must be a string")
    
    if not domain or len(domain) < 2 or len(domain) > 100:
        raise ValidationException("Research domain must be between 2 and 100 characters")
