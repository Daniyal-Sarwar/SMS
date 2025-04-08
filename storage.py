"""
Storage Module
Handles file operations for persistent storage.
"""

import os
import json
from exceptions import StorageException
from models.student import Student
from models.undergraduate import Undergraduate
from models.postgraduate import Postgraduate

# File path for storing student data
STORAGE_FILE = "students.json"

def save_students(students):
    """
    Save student data to a JSON file.
    
    Args:
        students (list): List of Student, Undergraduate, and Postgraduate objects.
        
    Raises:
        StorageException: If there's an error saving the data.
    """
    try:
        # Convert student objects to dictionaries
        student_data = []
        
        for student in students:
            student_dict = {
                "id": student.get_student_id(),
                "name": student.get_name(),
                "age": student.get_age(),
                "courses": student.get_courses(),  # Storing list of courses
                "year": student.get_year(),
                "field_of_study": student.get_field_of_study(),
                "type": "student"
            }
            
            # Add undergraduate specific data
            if isinstance(student, Undergraduate):
                student_dict["type"] = "undergraduate"
                student_dict["minor"] = student.get_minor()
            # Add postgraduate specific data
            elif isinstance(student, Postgraduate):
                student_dict["type"] = "postgraduate"
                student_dict["domain"] = student.get_domain()
                
            student_data.append(student_dict)
        
        # Write to file
        with open(STORAGE_FILE, 'w') as file:
            json.dump(student_data, file, indent=4)
            
    except Exception as e:
        raise StorageException(f"Error saving student data: {str(e)}")

def load_students():
    """
    Load student data from a JSON file.
    
    Returns:
        list: List of Student, Undergraduate, and Postgraduate objects.
        
    Raises:
        StorageException: If there's an error loading the data.
    """
    students = []
    
    try:
        # Check if file exists
        if not os.path.exists(STORAGE_FILE):
            return students
        
        # Read from file
        with open(STORAGE_FILE, 'r') as file:
            student_data = json.load(file)
        
        # Convert dictionaries to student objects
        for data in student_data:
            # Handle courses data - could be string in old format or list in new format
            courses = data.get("courses", data.get("course", ""))
            
            if data["type"] == "undergraduate":
                student = Undergraduate(
                    data["id"], 
                    data["name"], 
                    data["age"], 
                    courses,
                    data["year"],
                    data.get("minor", ""),  # Get minor with empty string default
                    None  # No department
                )
            elif data["type"] == "postgraduate":
                student = Postgraduate(
                    data["id"], 
                    data["name"], 
                    data["age"], 
                    courses,
                    data["year"],
                    0,  # No graduation year (phased out)
                    data.get("domain", ""),  # Get domain with empty string default
                    None  # No department
                )
            else:
                student = Student(
                    data["id"], 
                    data["name"], 
                    data["age"], 
                    courses,
                    data["year"],
                    None  # No department
                )
            
            # Set field of study if available
            if "field_of_study" in data and data["field_of_study"]:
                student.set_field_of_study(data["field_of_study"])
                
            students.append(student)
            
    except Exception as e:
        raise StorageException(f"Error loading student data: {str(e)}")
    
    return students
