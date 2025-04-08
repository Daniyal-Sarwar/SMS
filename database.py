"""
Database Module
Provides storage and retrieval of student records.
"""

# Global list to store all student records
students = []

def add_student(student):
    """
    Add a student to the database.
    
    Args:
        student: A Student or Undergraduate object.
    """
    students.append(student)

def update_student(updated_student):
    """
    Update an existing student in the database.
    
    Args:
        updated_student: A Student or Undergraduate object with updated information.
    """
    for i, student in enumerate(students):
        if student.get_student_id() == updated_student.get_student_id():
            students[i] = updated_student
            break

def delete_student(student_id):
    """
    Delete a student from the database.
    
    Args:
        student_id: ID of the student to delete.
    """
    global students
    students = [student for student in students if student.get_student_id() != student_id]

def get_student_by_id(student_id):
    """
    Get a student by ID.
    
    Args:
        student_id: ID of the student to retrieve.
        
    Returns:
        Student or Undergraduate object, or None if not found.
    """
    for student in students:
        if student.get_student_id() == student_id:
            return student
    return None
