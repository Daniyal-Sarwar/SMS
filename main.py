import streamlit as st
import pandas as pd
from id_generator import generate_id_from_name
from student_operations import (
    add_student, 
    update_student, 
    delete_student, 
    list_students,
    get_student_by_id,
    search_students,
    initialize
)
from models.student import Student
from models.undergraduate import Undergraduate
from models.postgraduate import Postgraduate
from exceptions import StudentManagementException
from validation import (
    validate_student_id,
    validate_year,
    validate_minor,
    validate_domain
)

def main():
    """
    Main function to run the Student Management System with Streamlit interface.
    """
    # Initialize the database
    initialize()
    
    # Set up page config
    st.set_page_config(
        page_title="Student Management System",
        page_icon="📚",
        layout="wide"
    )
    
    # Page title
    st.title("Student Management System")
    
    # Display messages if any
    if "success_message" in st.session_state:
        st.success(st.session_state.success_message)
        del st.session_state.success_message
    
    if "error_message" in st.session_state:
        st.error(st.session_state.error_message)
        del st.session_state.error_message
    
    # Sidebar menu
    st.sidebar.title("Menu")
    menu_options = [
        "View All Students",
        "Search Students", 
        "Add Student", 
        "Update Student", 
        "Delete Student"
    ]
    choice = st.sidebar.selectbox("Choose an option", menu_options)
    
    # Display selected page
    if choice == "View All Students":
        display_students()
    elif choice == "Search Students":
        search_students_form()
    elif choice == "Add Student":
        add_student_form()
    elif choice == "Update Student":
        update_student_form()
    elif choice == "Delete Student":
        delete_student_form()

def display_students():
    """Display all students in a table format."""
    st.header("All Students")
    
    students = list_students()
    if not students:
        st.info("No students available. Add students to see them here.")
        return
    
    # Convert student objects to a list of dictionaries
    student_data = []
    for student in students:
        student_dict = {
            "ID": student.get_student_id(),
            "Name": student.get_name(),
            "Age": student.get_age(),
            "Course": student.get_course(),
            "Year": student.get_year(),
            "Field of Study": student.get_field_of_study() or "N/A",
            "Type": "Regular Student"
        }
        
        if isinstance(student, Undergraduate):
            student_dict["Type"] = "Undergraduate"
            student_dict["Minor"] = student.get_minor()
        elif isinstance(student, Postgraduate):
            student_dict["Type"] = "Postgraduate"
            student_dict["Research Domain"] = student.get_domain() or "N/A"
        
        student_data.append(student_dict)
    
    # Display the student data as a table
    df = pd.DataFrame(student_data)
    st.dataframe(df)

def search_students_form():
    """Form to search for students."""
    st.header("Search Students")
    
    search_term = st.text_input("Enter search term (name, ID, course, or field of study)", key="search_term_input")
    
    if st.button("Search"):
        if not search_term:
            st.warning("Please enter a search term")
            return
        
        students = search_students(search_term)
        
        if not students:
            st.info(f"No students found matching '{search_term}'")
            return
        
        # Convert student objects to a list of dictionaries
        student_data = []
        for student in students:
            student_dict = {
                "ID": student.get_student_id(),
                "Name": student.get_name(),
                "Age": student.get_age(),
                "Course": student.get_course(),
                "Year": student.get_year(),
                "Field of Study": student.get_field_of_study() or "N/A",
                "Type": "Regular Student"
            }
            
            if isinstance(student, Undergraduate):
                student_dict["Type"] = "Undergraduate"
                student_dict["Minor"] = student.get_minor()
            elif isinstance(student, Postgraduate):
                student_dict["Type"] = "Postgraduate"
                student_dict["Research Domain"] = student.get_domain() or "N/A"
            
            student_data.append(student_dict)
        
        # Display the student data as a table
        st.subheader(f"Search Results for '{search_term}'")
        df = pd.DataFrame(student_data)
        st.dataframe(df)

def add_student_form():
    """Form to add a new student."""
    st.header("Add Student")
    
    # Determine student type
    student_type = st.radio("Student Type", ["Undergraduate", "Postgraduate"], key="add_student_type")
    
    with st.form("add_student_form"):
        # Student ID is always auto-generated
        name = st.text_input("Name", key="add_name")
        age = st.number_input("Age", min_value=16, max_value=100, step=1, key="add_age")
        year = st.number_input("Year of Study", min_value=1, max_value=7, step=1, key="add_year")
        
        # Field of Study fields for all students
        field_of_study_options = {
            "Software Engineering": ["Programming", "Data Structures", "Algorithms", "Software Design", "Web Development"],
            "Data Science": ["Statistics", "Machine Learning", "Data Mining", "Big Data", "Neural Networks"],
            "Civil Engineering": ["Mechanics", "Structures", "Materials", "Hydraulics", "Surveying"],
            "Mechanical Engineering": ["Thermodynamics", "Fluid Dynamics", "Machine Design", "Control Systems", "Manufacturing"],
            "Business": ["Accounting", "Marketing", "Finance", "Management", "Economics", "Business Ethics"],
            "Arts": ["Fine Arts", "Music", "Theater", "Literature", "Philosophy", "History"],
            "Sciences": ["Physics", "Chemistry", "Biology", "Mathematics", "Astronomy", "Geology"],
            "Medicine": ["Anatomy", "Physiology", "Pathology", "Pharmacology", "Microbiology", "Immunology"],
            "Law": ["Constitutional Law", "Criminal Law", "Civil Law", "International Law", "Corporate Law", "Human Rights Law"]
        }
        
        field_of_study = st.selectbox("Field of Study", list(field_of_study_options.keys()), key="add_field")
        
        # Show course options based on field of study
        if field_of_study and field_of_study in field_of_study_options:
            course_options = field_of_study_options[field_of_study]
            # Multi-select for courses
            selected_courses = st.multiselect(
                "Courses (select multiple)",
                options=course_options,
                key="add_multi_courses"
            )
            # Convert back to string format for compatibility
            course = ", ".join(selected_courses) if selected_courses else ""
        else:
            course = st.text_input("Course", key="add_course_text")
        
        # Student type specific fields
        if student_type == "Undergraduate":
            # Minor options based on field of study
            minor_options = [
                "Mathematics", "Business", "Electronics", "Psychology", "Communication",
                "Business Management", "Computer Science", "Renewable Energy", "Physics",
                "Foreign Language", "Law", "Data Analytics", "Digital Media", "Education",
                "Environmental Studies", "Public Health", "Ethics", "Nutrition", "Management",
                "International Relations", "Political Science", "Economics", "Philosophy"
            ]
            
            # Show minor options
            minor = st.selectbox("Minor Subject", [""] + minor_options, key="add_minor")
            
            # Hide postgraduate fields
            domain = ""
        else:  # Postgraduate
            # Research domains based on field of study
            domain_options = [
                "Artificial Intelligence", "Machine Learning", "Computer Vision", 
                "Natural Language Processing", "Cybersecurity", "Networks", 
                "Human-Computer Interaction", "Robotics", "Materials Science", 
                "Structural Engineering", "Energy Systems", "Control Systems", 
                "Biomedical Engineering", "Nanotechnology", "Finance", 
                "Marketing Analytics", "Operations Management", "Leadership", 
                "Business Analytics", "Entrepreneurship", "Supply Chain Management"
            ]
            
            domain = st.selectbox("Research Domain", domain_options, key="add_domain_dropdown")
                
            # Hide undergraduate fields
            minor = "No"
        
        submit_button = st.form_submit_button("Add Student")
        
        if submit_button:
            try:
                if not name or not course:
                    raise StudentManagementException("Name and Course fields are required")
                
                # Generate student ID (always auto-generated)
                student_id = generate_id_from_name(name, age)
                
                validate_year(year)
                
                # Create student object based on type
                if student_type == "Undergraduate":
                    # Validate minor field
                    validate_minor(minor)
                    new_student = Undergraduate(student_id, name, age, course, year, minor)
                    if field_of_study:
                        new_student.set_field_of_study(field_of_study)
                else:  # Postgraduate
                    # Validate domain
                    validate_domain(domain)
                    # No graduation year (removed as requested)
                    new_student = Postgraduate(student_id, name, age, course, year, 0, domain)
                    if field_of_study:
                        new_student.set_field_of_study(field_of_study)
                
                # Add student to the system
                add_student(new_student)
                st.session_state.success_message = f"Student added successfully with ID: {student_id}"
                st.rerun()
                
            except StudentManagementException as e:
                st.session_state.error_message = str(e)
                st.rerun()

def update_student_form():
    """Form to update an existing student."""
    st.header("Update Student")
    
    # Get all student IDs
    students = list_students()
    if not students:
        st.info("No students available to update.")
        return
    
    student_ids = [student.get_student_id() for student in students]
    
    # Select student to update
    selected_id = st.selectbox("Select Student ID to Update", student_ids, key="update_select_id")
    
    # Get the selected student
    selected_student = get_student_by_id(selected_id)
    
    if selected_student:
        if isinstance(selected_student, Undergraduate):
            student_type = "Undergraduate"
        elif isinstance(selected_student, Postgraduate):
            student_type = "Postgraduate"
        else:
            student_type = "Regular Student"
        
        with st.form("update_student_form"):
            name = st.text_input("Name", value=selected_student.get_name(), key="update_name")
            age = st.number_input("Age", min_value=16, max_value=100, step=1, value=selected_student.get_age(), key="update_age")
            year = st.number_input("Year of Study", min_value=1, max_value=7, step=1, value=selected_student.get_year(), key="update_year")
            
            # Display field of study (read-only)
            current_field = selected_student.get_field_of_study() or "Not specified"
            st.info(f"Field of Study: {current_field} (cannot be changed)")
            
            # Field of Study dictionary for course options
            field_of_study_options = {
                "Software Engineering": ["Programming", "Data Structures", "Algorithms", "Software Design", "Web Development"],
                "Data Science": ["Statistics", "Machine Learning", "Data Mining", "Big Data", "Neural Networks"],
                "Civil Engineering": ["Mechanics", "Structures", "Materials", "Hydraulics", "Surveying"],
                "Mechanical Engineering": ["Thermodynamics", "Fluid Dynamics", "Machine Design", "Control Systems", "Manufacturing"],
                "Business": ["Accounting", "Marketing", "Finance", "Management", "Economics", "Business Ethics"],
                "Arts": ["Fine Arts", "Music", "Theater", "Literature", "Philosophy", "History"],
                "Sciences": ["Physics", "Chemistry", "Biology", "Mathematics", "Astronomy", "Geology"],
                "Medicine": ["Anatomy", "Physiology", "Pathology", "Pharmacology", "Microbiology", "Immunology"],
                "Law": ["Constitutional Law", "Criminal Law", "Civil Law", "International Law", "Corporate Law", "Human Rights Law"]
            }
            
            # Current courses as a list
            current_courses = []
            try:
                # Try to get courses as a list first
                courses_list = selected_student.get_courses()
                if courses_list:
                    current_courses = courses_list
            except:
                # Fallback to string representation and split
                course_str = selected_student.get_course()
                if course_str:
                    current_courses = [c.strip() for c in course_str.split(',')]
            
            # Show appropriate course options
            if current_field and current_field in field_of_study_options:
                course_options = field_of_study_options[current_field]
                # Only show multi-select for available course options based on the field
                st.write("Courses for this field of study:")
                selected_courses = st.multiselect(
                    "Select courses",
                    options=course_options,
                    default=[c for c in current_courses if c in course_options],  # Only include valid options
                    key="update_multi_courses"
                )
                
                # Give option to add custom courses
                custom_courses = st.text_input(
                    "Additional courses (comma separated)",
                    value=", ".join([c for c in current_courses if c not in course_options]),
                    key="update_custom_courses"
                )
                
                # Combine selected courses with custom courses
                if custom_courses:
                    custom_course_list = [c.strip() for c in custom_courses.split(',') if c.strip()]
                    all_courses = selected_courses + custom_course_list
                else:
                    all_courses = selected_courses
                
                # Convert to string for compatibility
                course = ", ".join(all_courses) if all_courses else ""
            else:
                # If no field of study or invalid field, just show text input
                course = st.text_input("Courses (comma separated)", 
                                       value=selected_student.get_course(), 
                                       key="update_courses_text")
            
            # Student type specific fields
            if student_type == "Undergraduate":
                # Minor options based on field of study
                minor_options = [
                    "Mathematics", "Business", "Electronics", "Psychology", "Communication",
                    "Business Management", "Computer Science", "Renewable Energy", "Physics",
                    "Foreign Language", "Law", "Data Analytics", "Digital Media", "Education",
                    "Environmental Studies", "Public Health", "Ethics", "Nutrition", "Management",
                    "International Relations", "Political Science", "Economics", "Philosophy"
                ]
                
                # Get current minor if available
                current_minor = ""
                if isinstance(selected_student, Undergraduate):
                    current_minor = selected_student.get_minor()
                
                # Show minor options
                default_minor = 0
                minor_list = [""] + minor_options
                if current_minor in minor_list:
                    default_minor = minor_list.index(current_minor)
                minor = st.selectbox("Minor Subject", minor_list, index=default_minor, key="update_minor")
                
                # Initialize postgraduate fields
                domain = ""
            elif student_type == "Postgraduate":
                # Research domains based on field of study
                domain_options = [
                    "Artificial Intelligence", "Machine Learning", "Computer Vision", 
                    "Natural Language Processing", "Cybersecurity", "Networks", 
                    "Human-Computer Interaction", "Robotics", "Materials Science", 
                    "Structural Engineering", "Energy Systems", "Control Systems", 
                    "Biomedical Engineering", "Nanotechnology", "Finance", 
                    "Marketing Analytics", "Operations Management", "Leadership", 
                    "Business Analytics", "Entrepreneurship", "Supply Chain Management"
                ]
                
                # Get current domain if available
                current_domain = "" if not isinstance(selected_student, Postgraduate) else selected_student.get_domain() or ""
                
                # Show domain options
                default_domain = 0
                if current_domain in domain_options:
                    default_domain = domain_options.index(current_domain)
                domain = st.selectbox("Research Domain", domain_options, index=default_domain, key="update_domain_dropdown")
                
                # Initialize undergraduate fields
                minor = "No"
            else:
                # Regular student
                minor = "No"  # Initialize to avoid UnboundLocalError
                domain = ""
            
            submit_button = st.form_submit_button("Update Student")
            
            if submit_button:
                try:
                    if not name or not course:
                        raise StudentManagementException("Name and Course fields are required")
                    
                    validate_year(year)
                    
                    # Update student object based on type
                    if student_type == "Undergraduate":
                        # Validate minor field
                        validate_minor(minor)
                        updated_student = Undergraduate(selected_id, name, age, course, year, minor)
                        # Keep the original field of study
                        updated_student.set_field_of_study(current_field)
                    elif student_type == "Postgraduate":
                        # Validate domain only
                        validate_domain(domain)
                        # Use 0 for graduation year as it's no longer needed
                        updated_student = Postgraduate(selected_id, name, age, course, year, 0, domain)
                        # Keep the original field of study
                        updated_student.set_field_of_study(current_field)
                    else:  # Regular Student
                        updated_student = Student(selected_id, name, age, course, year)
                        # Keep the original field of study
                        updated_student.set_field_of_study(current_field)
                    
                    # Update student in the system
                    update_student(updated_student)
                    st.session_state.success_message = f"Student {selected_id} updated successfully!"
                    st.rerun()
                    
                except StudentManagementException as e:
                    st.session_state.error_message = str(e)
                    st.rerun()

def delete_student_form():
    """Form to delete a student."""
    st.header("Delete Student")
    
    # Get all student IDs
    students = list_students()
    if not students:
        st.info("No students available to delete.")
        return
    
    student_ids = [student.get_student_id() for student in students]
    
    # Select student to delete
    selected_id = st.selectbox("Select Student ID to Delete", student_ids, key="delete_select_id")
    
    if st.button("Delete Student"):
        try:
            delete_student(selected_id)
            st.session_state.success_message = f"Student {selected_id} deleted successfully!"
            st.rerun()
        except StudentManagementException as e:
            st.session_state.error_message = str(e)
            st.rerun()

if __name__ == "__main__":
    main()