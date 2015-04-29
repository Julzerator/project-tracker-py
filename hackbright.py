"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """
    db_cursor.execute(QUERY, (github,))
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (
        row[0], row[1], row[2])


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """
        INSERT INTO Students (first_name, last_name, github)
        VALUES (?, ?, ?)
        """
    db_cursor.execute(QUERY, (first_name, last_name, github))

    db_connection.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)


def get_project_by_title(title):
    """Given a project title, print information about the matching project."""

    QUERY = """
        SELECT title, description, max_grade
        FROM Projects
        WHERE title = ?
        """
    db_cursor.execute(QUERY, (title,))
    project = db_cursor.fetchall()
    print "These Projects were found:"
    for i in project:
        print "Project Title: %s\nProject Description: %s\nMaximum Grade: %d" % (
            i[0], i[1], i[2])

def get_student_grade(github_username, project_title):
    """Given github username and project title, print student grade"""

    QUERY = """
        SELECT first_name, last_name, project_title, grade 
        FROM Grades
        LEFT JOIN Students
        ON github = student_github
        WHERE student_github = ?
        AND project_title = ?
        """
    db_cursor.execute(QUERY, (github_username, project_title))
    grade = db_cursor.fetchone()
    first_name, last_name, project_title, grade = grade  # This is unpacking
    print "Student's name: %s %s\nProject title: %s\nGrade: %d" % (
        first_name, last_name, project_title, grade)
    # This is indexing (grade[0], grade[1], grade[2], grade[3])

def give_student_grade(student_github, project_title, grade):
    """Given github username, project title and grade of student, add it to the student's record"""

    QUERY = """
        INSERT INTO Grades (student_github, project_title, grade)
        VALUES (?, ?, ?)
        """
    db_cursor.execute(QUERY,(student_github, project_title, grade))

    db_connection.commit()
    print "The grade of %s has been recorded for %s for the %s project." % (
        grade, student_github, project_title)

def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project_title":
            title = args[0]
            get_project_by_title(title)

        elif command == "student_grade":
            github_username, project_title = args
            get_student_grade(github_username, project_title)

        elif command == "give_student_grade":
            student_github, project_title, grade = args
            give_student_grade(student_github, project_title, grade)

if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()
