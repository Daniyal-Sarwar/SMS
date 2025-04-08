"""
Postgraduate Module
Defines the Postgraduate class, which inherits from Student.
"""

from models.student import Student

class Postgraduate(Student):
    """
    Postgraduate class that inherits from Student and adds additional
    functionality specific to postgraduate students.
    """
    
    def __init__(self, student_id, name, age, course, year, graduation_year=0, domain=None, department=None):
        """
        Initialize a Postgraduate object.
        
        Args:
            student_id (str): The student ID
            name (str): The student's name
            age (int): The student's age (must be at least 18)
            course (str or list): The student's enrolled courses
            year (int): The student's year of study
            graduation_year (int, optional): The student's graduation year (being phased out)
            domain (str, optional): The student's research domain
            department (str, optional): The student's department (being phased out)
        """
        # Ensure minimum age requirement
        if age < 18:
            raise ValueError("Postgraduate students must be at least 18 years old")
            
        # Call the parent class constructor
        super().__init__(student_id, name, age, course, year, None)  # No department as it's being phased out
        
        # Add postgraduate specific attributes - only domain is kept
        self.__domain = domain
    
    # Getter method
    def get_domain(self):
        """Get the student's research domain."""
        return self.__domain
    
    # Setter method
    def set_domain(self, domain):
        """
        Set the student's research domain.
        
        Args:
            domain (str): The new research domain
        """
        self.__domain = domain
    
    def get_details(self):
        """
        Override the parent class method to include postgraduate information.
        
        Returns:
            str: A formatted string with student details including postgraduate info
        """
        # Get basic details from parent class
        basic_details = super().get_details()
        
        # Add only research domain 
        domain_info = f"Research Domain: {self.__domain}\n" if self.__domain else ""
        
        return f"{basic_details}{domain_info}"
    
    def update_domain(self, new_domain):
        """
        Update the student's research domain.
        
        Args:
            new_domain (str): The new research domain
        """
        self.__domain = new_domain
        
    # For compatibility with older code
    def get_graduation_year(self):
        """Get the student's graduation year. Returns 0 as this is being phased out."""
        return 0
        
    def set_graduation_year(self, graduation_year):
        """
        Set the student's graduation year. This is a no-op as graduation year is being phased out.
        
        Args:
            graduation_year (int): The new graduation year
        """
        pass