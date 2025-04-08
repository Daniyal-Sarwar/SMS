"""
Undergraduate Module
Defines the Undergraduate class, which inherits from Student.
"""

from models.student import Student

class Undergraduate(Student):
    """
    Undergraduate class that inherits from Student and adds additional
    functionality specific to undergraduate students.
    """
    
    def __init__(self, student_id, name, age, course, year, minor, department=None):
        """
        Initialize an Undergraduate object.
        
        Args:
            student_id (str): The student ID
            name (str): The student's name
            age (int): The student's age
            course (str or list): The student's enrolled courses
            year (int): The student's year of study
            minor (str): The student's minor subject
            department (str, optional): The student's department (being phased out)
        """
        # Call the parent class constructor - pass None for department as it's being phased out
        super().__init__(student_id, name, age, course, year, None)
        
        # Add undergraduate specific attribute
        self.__minor = minor  # Now storing the actual minor subject
    
    # Getter method for minor
    def get_minor(self):
        """Get the student's minor subject."""
        return self.__minor
    
    # Setter method for minor
    def set_minor(self, minor):
        """
        Set the student's minor subject.
        
        Args:
            minor (str): The minor subject
        """
        self.__minor = minor
    
    def get_details(self):
        """
        Override the parent class method to include minor information.
        
        Returns:
            str: A formatted string with student details including minor status
        """
        # Get basic details from parent class
        basic_details = super().get_details()
        
        # Add undergraduate specific details
        if self.has_minor():
            return f"{basic_details}Minor Subject: {self.__minor}"
        else:
            return f"{basic_details}Minor Subject: None"
    
    def update_minor(self, new_minor):
        """
        Update the student's minor subject.
        
        Args:
            new_minor (str): The new minor subject
        """
        self.__minor = new_minor
        
    def has_minor(self):
        """
        Check if the student has a minor.
        
        Returns:
            bool: True if the student has a minor subject, False otherwise
        """
        return bool(self.__minor) and self.__minor.strip() != ""
