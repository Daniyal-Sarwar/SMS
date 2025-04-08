"""
Student Module
Defines the base Student class with encapsulation.
"""

class Student:
    """
    Student class that demonstrates encapsulation by using private attributes
    with getter and setter methods.
    """
    
    def __init__(self, student_id, name, age, course, year, department=None):
        """
        Initialize a Student object.
        
        Args:
            student_id (str): The student ID
            name (str): The student's name
            age (int): The student's age
            course (str or list): The student's enrolled courses
            year (int): The student's year of study
            department (str, optional): The student's department (being phased out)
        """
        self.__student_id = student_id
        self.__name = name
        self.__age = age
        
        # Convert single course to list if needed
        if isinstance(course, str):
            if ',' in course:
                self.__courses = [c.strip() for c in course.split(',')]
            else:
                self.__courses = [course]
        else:
            self.__courses = course or []
            
        self.__year = year
        self.__field_of_study = None  # Field of study replacing department
    
    # Getter methods
    def get_student_id(self):
        """Get the student ID."""
        return self.__student_id
    
    def get_name(self):
        """Get the student's name."""
        return self.__name
    
    def get_age(self):
        """Get the student's age."""
        return self.__age
    
    def get_courses(self):
        """Get the student's courses as a list."""
        return self.__courses
    
    def get_course(self):
        """
        Get the student's courses as a comma-separated string.
        Maintained for backward compatibility.
        """
        return ', '.join(self.__courses) if self.__courses else ""
    
    def get_year(self):
        """Get the student's year of study."""
        return self.__year
    
    def get_department(self):
        """Get the student's department (compatibility method)."""
        return None
    
    def get_field_of_study(self):
        """Get the student's field of study."""
        return self.__field_of_study
    
    # Setter methods
    def set_student_id(self, student_id):
        """
        Set the student ID.
        
        Args:
            student_id (str): The new student ID
        """
        self.__student_id = student_id
    
    def set_name(self, name):
        """
        Set the student's name.
        
        Args:
            name (str): The new name
        """
        self.__name = name
    
    def set_age(self, age):
        """
        Set the student's age.
        
        Args:
            age (int): The new age
        """
        self.__age = age
    
    def set_courses(self, courses):
        """
        Set the student's courses.
        
        Args:
            courses (list): The new courses
        """
        if isinstance(courses, str):
            if ',' in courses:
                self.__courses = [c.strip() for c in courses.split(',')]
            else:
                self.__courses = [courses]
        else:
            self.__courses = courses or []
    
    def set_course(self, course):
        """
        Set a single course.
        Maintained for backward compatibility.
        
        Args:
            course (str): The new course
        """
        if ',' in course:
            self.__courses = [c.strip() for c in course.split(',')]
        else:
            self.__courses = [course] if course else []
        
    def set_year(self, year):
        """
        Set the student's year of study.
        
        Args:
            year (int): The new year of study
        """
        self.__year = year
        
    def set_department(self, department):
        """
        Set the student's department (compatibility method).
        
        Args:
            department (str): The new department
        """
        pass  # Department functionality is being phased out
        
    def set_field_of_study(self, field):
        """
        Set the student's field of study.
        
        Args:
            field (str): The new field of study
        """
        self.__field_of_study = field
    
    def get_details(self):
        """
        Get a string containing all student details.
        
        Returns:
            str: A formatted string with student details
        """
        courses_str = ', '.join(self.__courses) if self.__courses else "None"
        field_str = f"Field of Study: {self.__field_of_study}\n" if self.__field_of_study else ""
        
        return (f"Student ID: {self.__student_id}\n"
                f"Name: {self.__name}\n"
                f"Age: {self.__age}\n"
                f"Courses: {courses_str}\n"
                f"Year: {self.__year}\n"
                f"{field_str}")
    
    def add_course(self, new_course):
        """
        Add a course to the student's courses.
        
        Args:
            new_course (str): The course to add
        """
        if new_course and new_course not in self.__courses:
            self.__courses.append(new_course)
    
    def remove_course(self, course):
        """
        Remove a course from the student's courses.
        
        Args:
            course (str): The course to remove
        """
        if course in self.__courses and len(self.__courses) > 1:  # Don't remove the last course
            self.__courses.remove(course)
    
    def update_courses(self, new_courses):
        """
        Update all the student's courses.
        
        Args:
            new_courses (list): The new list of courses
        """
        self.set_courses(new_courses)
        
    def update_year(self, new_year):
        """
        Update the student's year of study.
        
        Args:
            new_year (int): The new year of study
        """
        self.__year = new_year
