# EdTech Backend System 
#
# Description
#   SL Tech is an edtech company that provides training programs on various technical and functional skills. They are planning to update their learner interface to enhance the learning experience. As part of the development team, you have to support the backend development by creating modules to manage the credentials, courses, and other activities of learners.
#
# Objectives:
#   To design and implement a backend system for SL Tech's learner interface
#   To create and manage user credentials, course enrollments, and assignments
#   To integrate all modules into a comprehensive backend system


# User Class
class User:
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password

    def update_email(self, new_email):
        self.email = new_email

    def update_password(self, old_password, new_password):
        if self.password == old_password:
            self.password = new_password
        else:
            print("Old password is incorrect")

    def validate_credentials(self, email, password):
        return self.email == email and self.password == password


# ---- Learner Class ----
class Learner(User):  # Inherits User
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password)
        self.enrolled_courses = []

    def enroll(self, course):
        if course not in self.enrolled_courses:
            self.enrolled_courses.append(course)
            course.add_learner(self)
        else:
            print(self.name, "is already enrolled in", course.title)

    def drop(self, course):
        if course in self.enrolled_courses:
            self.enrolled_courses.remove(course)
            course.remove_learner(self)


# ---- Instructor Class ----
class Instructor(User):  # Inherits User
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password)
        self.courses_taught = []

    def add_course(self, course):
        if course not in self.courses_taught:
            self.courses_taught.append(course)
            course.instructor = self

    def remove_course(self, course):
        if course in self.courses_taught:
            self.courses_taught.remove(course)
            course.instructor = None


# ---- Course Class ----
class Course:
    def __init__(self, course_id, title):
        self.course_id = course_id
        self.title = title
        self.instructor = None
        self.learners = []

    def add_learner(self, learner):
        if learner not in self.learners:
            self.learners.append(learner)

    def remove_learner(self, learner):
        if learner in self.learners:
            self.learners.remove(learner)

    def list_learners(self):
        names = []
        for learner in self.learners:
            names.append(learner.name)
        return names


# ---- Enrollment Class ----
class Enrollment:
    def __init__(self, learner, course):
        self.learner = learner
        self.course = course


# ---- SLTechBackend Class ----
class SLTechBackend:
    def __init__(self):
        self.users = []
        self.courses = []
        self.enrollments = []

    def add_user(self, user):
        self.users.append(user)

    def add_course(self, course):
        self.courses.append(course)

    def enroll_learner(self, learner, course):
        enrollment = Enrollment(learner, course)
        self.enrollments.append(enrollment)
        learner.enroll(course)

    def drop_learner(self, learner, course):
        learner.drop(course)
        # manually rebuild enrollment list
        new_enrollments = []
        for e in self.enrollments:
            if not (e.learner == learner and e.course == course):
                new_enrollments.append(e)
        self.enrollments = new_enrollments

    def list_courses(self):
        for c in self.courses:
            if c.instructor is not None:
                print(c.course_id, ":", c.title, "(Instructor:", c.instructor.name, ")")
            else:
                print(c.course_id, ":", c.title, "(Instructor: None)")


# ---- User Input Menu ----
def run_backend():
    backend = SLTechBackend()
    user_id_counter = 1

    while True:
        print("SL Tech Backend System:")
        print("1. Add Learner")
        print("2. Add Instructor")
        print("3. Add Course")
        print("4. Assign Instructor to Course")
        print("5. Enroll Learner in Course")
        print("6. Drop Learner from Course")
        print("7. List Learners in Course")
        print("8. List Courses")
        print("0. Exit")
        print("\n==============================================\n")
        procedure = input("Enter a specific number to perform the operation: ")

        if procedure == "1":                             # Add Learner
            name = input("Enter learner name: ")
            email = input("Enter learner email: ")
            pw = input("Enter learner password: ")
            learner = Learner(user_id_counter, name, email, pw)
            backend.add_user(learner)
            print("Learner added with ID", user_id_counter)
            user_id_counter += 1

        elif procedure == "2":                           # Add Instructor
            name = input("Enter instructor name: ")
            email = input("Enter instructor email: ")
            pw = input("Enter instructor password: ")
            instructor = Instructor(user_id_counter, name, email, pw)
            backend.add_user(instructor)
            print("Instructor added with ID", user_id_counter)
            user_id_counter += 1

        elif procedure == "3":                           # Add Course
            cid = input("Enter course ID: ")
            title = input("Enter course title: ")
            course = Course(cid, title)
            backend.add_course(course)
            print("Course", cid, "added")

        elif procedure == "4":                           # Assign Instructor to Course
            inst_name = input("Enter instructor name: ")
            course_id = input("Enter course ID: ")
            instructor = None
            for u in backend.users:
                if isinstance(u, Instructor) and u.name == inst_name:
                    instructor = u
            course = None
            for c in backend.courses:
                if c.course_id == course_id:
                    course = c
            if instructor is not None and course is not None:
                instructor.add_course(course)
                print("Instructor", instructor.name, "assigned to", course.title)
            else:
                print("Instructor or course not found")

        elif procedure == "5":                           # Enroll Learner in Course

            learner_name = input("Enter learner name: ")
            course_id = input("Enter course ID: ")
            learner = None
            for u in backend.users:
                if isinstance(u, Learner) and u.name == learner_name:
                    learner = u
            course = None
            for c in backend.courses:
                if c.course_id == course_id:
                    course = c
            if learner is not None and course is not None:
                backend.enroll_learner(learner, course)
                print("Learner", learner.name, "enrolled in", course.title)
            else:
                print("Learner or course not found")

        elif procedure == "6":                           # Drop Learner from Course
            learner_name = input("Enter learner name: ")
            course_id = input("Enter course ID: ")
            learner = None
            for u in backend.users:
                if isinstance(u, Learner) and u.name == learner_name:
                    learner = u
            course = None
            for c in backend.courses:
                if c.course_id == course_id:
                    course = c
            if learner is not None and course is not None:
                backend.drop_learner(learner, course)
                print("Learner", learner.name, "dropped from", course.title
                      )
            else:
                print("Learner or course not found")

        elif procedure == "7":                           # List Learners in Course
            course_id = input("Enter course ID: ")
            course = None
            for c in backend.courses:
                if c.course_id == course_id:
                    course = c
            if course is not None:
                print("Learners:", course.list_learners())
            else:
                print("Course not found")

        elif procedure == "8":                           # List Courses
            backend.list_courses()

        elif procedure == "0":                           # Exit Logic
            print("Exiting...")
            break

        else:
            print("Invalid procedure")


if __name__ == "__main__":
    run_backend()
