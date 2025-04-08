"""
Exceptions Module
Defines custom exceptions for the Student Management System.
"""

class StudentManagementException(Exception):
    """
    Base exception for the Student Management System.
    """
    pass

class ValidationException(StudentManagementException):
    """
    Exception raised for validation errors.
    """
    pass

class StorageException(StudentManagementException):
    """
    Exception raised for storage-related errors.
    """
    pass

class DatabaseException(StudentManagementException):
    """
    Exception raised for database-related errors.
    """
    pass

class InvalidIDException(ValidationException):
    """
    Exception raised when a student ID is invalid.
    """
    pass

class DuplicateStudentIDException(DatabaseException):
    """
    Exception raised when attempting to add a student with an ID that already exists.
    """
    pass

class StudentNotFoundException(DatabaseException):
    """
    Exception raised when a student is not found in the database.
    """
    pass
