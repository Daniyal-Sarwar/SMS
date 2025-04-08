"""
Student Operations Module
Contains core functionalities for managing student records.
"""

import database
from exceptions import (
    StudentManagementException, 
    InvalidIDException, 
    DuplicateStudentIDException, 
    StudentNotFoundException
)
from validation import validate_student_id
from storage import save_students, load_students
from models.student import Student
from models.undergraduate import Undergraduate
from models.postgraduate import Postgraduate

def add_student(student):
    """
    Add a new student to the system.
    
    Args:
        student: A Student or Undergraduate object.
        
    Raises:
        InvalidIDException: If the student ID format is invalid.
        DuplicateStudentIDException: If a student with the ID already exists.
    """
    # Validate student ID
    try:
        validate_student_id(student.get_student_id())
    except Exception as e:
        raise InvalidIDException(f"Invalid student ID: {str(e)}")
    
    # Check if student already exists
    if database.get_student_by_id(student.get_student_id()):
        raise DuplicateStudentIDException(f"Student with ID {student.get_student_id()} already exists.")
    
    # Add student to database
    database.add_student(student)
    
    # Save changes to file
    save_students(database.students)

def update_student(student):
    """
    Update an existing student in the system.
    
    Args:
        student: A Student or Undergraduate object with updated information.
        
    Raises:
        InvalidIDException: If the student ID format is invalid.
        StudentNotFoundException: If no student with the ID exists.
    """
    # Validate student ID
    try:
        validate_student_id(student.get_student_id())
    except Exception as e:
        raise InvalidIDException(f"Invalid student ID: {str(e)}")
    
    # Check if student exists
    if not database.get_student_by_id(student.get_student_id()):
        raise StudentNotFoundException(f"Student with ID {student.get_student_id()} does not exist.")
    
    # Update student in database
    database.update_student(student)
    
    # Save changes to file
    save_students(database.students)

def delete_student(student_id):
    """
    Delete a student from the system.
    
    Args:
        student_id: ID of the student to delete.
        
    Raises:
        StudentNotFoundException: If no student with the ID exists.
    """
    # Check if student exists
    if not database.get_student_by_id(student_id):
        raise StudentNotFoundException(f"Student with ID {student_id} does not exist.")
    
    # Delete student from database
    database.delete_student(student_id)
    
    # Save changes to file
    save_students(database.students)

def list_students():
    """
    List all students in the system.
    
    Returns:
        list: A list of Student and Undergraduate objects.
    """
    return database.students

def get_student_by_id(student_id):
    """
    Get a student by ID.
    
    Args:
        student_id: ID of the student to retrieve.
        
    Returns:
        Student or Undergraduate object, or None if not found.
    """
    return database.get_student_by_id(student_id)

def search_students(keyword):
    """
    Search for students by keyword in name, course, ID, or field of study.
    
    Args:
        keyword (str): The search keyword.
        
    Returns:
        list: A list of matching Student, Undergraduate, or Postgraduate objects.
    """
    if not keyword:
        return []
    
    keyword = keyword.lower()
    matches = []
    
    for student in database.students:
        # Search in ID, name, course, and field of study
        student_id = student.get_student_id() or ""
        name = student.get_name() or ""
        course = student.get_course() or ""
        field_of_study = student.get_field_of_study() or ""
        
        if (keyword in student_id.lower() or
            keyword in name.lower() or
            keyword in course.lower() or
            keyword in field_of_study.lower()):
            matches.append(student)
            
        # Also search in Undergraduate minor or Postgraduate domain if applicable
        if isinstance(student, Undergraduate):
            minor = student.get_minor() or ""
            if keyword in minor.lower():
                if student not in matches:
                    matches.append(student)
        elif isinstance(student, Postgraduate):
            domain = student.get_domain() or ""
            if keyword in domain.lower():
                if student not in matches:
                    matches.append(student)
    
    return matches

# Initialize database by loading students from file
def initialize():
    """Initialize the database by loading students from file."""
    students = load_students()
    database.students = students

# Initialize the database when module is imported
initialize()
