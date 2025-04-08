# Student Management System

## Description
This is a Student Management System built with Python and Streamlit. It demonstrates key Object-Oriented Programming concepts such as encapsulation, inheritance, and polymorphism. The system allows for management of regular students and undergraduate students with specific fields for each type.

## Features
- Student record management (add, update, delete, view)
- Search functionality by name, ID, or course
- Auto-generation of unique student IDs
- Data validation for all input fields
- Error handling with custom exceptions
- Data persistence using JSON storage

## Requirements
- Python 3.6+
- Streamlit
- Pandas

## Application Structure
- `main.py`: Main application with Streamlit interface
- `models/student.py`: Base Student class
- `models/undergraduate.py`: Undergraduate class (inherits from Student)
- `database.py`: In-memory database for student records
- `storage.py`: File storage operations
- `student_operations.py`: Core student management operations
- `validation.py`: Input validation
- `exceptions.py`: Custom exceptions
- `id_generator.py`: Generates unique student IDs

## How to Use
1. Launch the application by running `streamlit run main.py`
2. Use the sidebar menu to navigate between different functions
3. Add students by providing their details
4. View, update or delete existing student records

## Special Notes
- Student IDs are unique and can be auto-generated based on name and age
- Undergraduate students require a minor field
- All data is saved to a JSON file for persistence
