"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from textwrap import dedent

app = Flask(__name__)
db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

def get_student():
    """Get all students."""

    QUERY = """
               SELECT first_name, last_name, github
               FROM students
            """
    db_cursor = db.session.execute(QUERY)

    row = db_cursor.fetchall()

    db.session.commit()

    return row

def get_student_by_github(github):
    """Given a GitHub account name, print info about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """

    db_cursor = db.session.execute(QUERY, {'github': github})

    row = db_cursor.fetchone()

    print("Student: {} {}\nGitHub account: {}".format(row[0], row[1], row[2]))

    return row


def make_new_student(first, last, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    QUERY = """
               INSERT INTO students (first_name, last_name, github)
               VALUES (:firstn, :lastn, :github)
            """
    db.session.execute(QUERY, {'firstn': first,
                               'lastn': last, 
                               'github': github})

    db.session.commit()


    print(f"Successfully added student: {first} {last}")

    return (first, last, github)


def get_project():
    """Get all projects."""

    QUERY = """
               SELECT title
               FROM projects
            """
    db_cursor = db.session.execute(QUERY)

    row = db_cursor.fetchall()

    db.session.commit()

    return row


def get_project_by_title(title_input):
    """Given a project title, print information about the project."""
    
    QUERY = """
               SELECT title, description, max_grade 
               FROM projects
               WHERE title = :title_placeholder
            """
    db_cursor = db.session.execute(QUERY, {'title_placeholder': title_input})

    row = db_cursor.fetchone()

    db.session.commit()

    print(f"Title: {row[0]}, Description: {row[1]}, Max Grade: {row[2]}")

    return row

def get_grade_by_github_title(github_input, title_input):
    """Print grade student received for a project."""
    QUERY = """
               SELECT grade
               FROM grades
               WHERE student_github = :github_ph
                   AND project_title = :title_ph
            """
    db_cursor = db.session.execute(QUERY, {'title_ph': title_input,
                                           'github_ph': github_input})

    row = db_cursor.fetchone()

    db.session.commit()

    print(f"Grade: {row[0]}")

def get_student_projects_and_grades(github_input):
    """Print grade student received for a project."""
    QUERY = """
               SELECT project_title, grade
               FROM grades
               WHERE student_github = :github_ph
            """
    db_cursor = db.session.execute(QUERY, {'github_ph': github_input})

    row = db_cursor.fetchall()

    db.session.commit()

    return row

def get_project_student_and_grade(title_input):
    """Print grade student received for a project."""
    QUERY = """
               SELECT student_github, grade
               FROM grades
               WHERE project_title = :title_ph

            """
    db_cursor = db.session.execute(QUERY, {'title_ph': title_input})

    row = db_cursor.fetchall()

    db.session.commit()

    return row


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    QUERY = """
               INSERT INTO grades(student_github, project_title, grade)
                   VALUES (:github_ph, :title_ph, :grade_ph)
            """

    db.session.execute(QUERY, {'github_ph': github,
                               'title_ph': title,
                               'grade_ph': grade})

    db.session.commit()

    print(f"Confirmed, assigned grade: {grade} for {github} on project {title}.")

def make_new_project(title_input, desc_input, max_grade_input):
    """Assign a student a grade on an assignment and print a confirmation."""
    QUERY = """
               INSERT INTO projects(title, description, max_grade)
                   VALUES (:title_ph, :desc_ph, :max_grade_ph)
            """

    db.session.execute(QUERY, {'title_ph': title_input,
                               'desc_ph': desc_input,
                               'max_grade_ph': max_grade_input})

    db.session.commit()

    print(dedent(f"""
                     Confirmed, added project {title_input}, with maximum grade of
                     {max_grade_input}, described as {desc_input}.
                 """))




def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received
    as a command.
    """

    command = None

    while command != "quit":
        input_string = input("HBA Database> ")
        tokens = input_string.split(",")
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "get_project":
            title = args[0]
            get_project_by_title(title)

        elif command == "get_grade":
            github, title = args
            get_grade_by_github_title(github, title)

        elif command == "assign_grade":
            github, title, grade = args
            assign_grade(github, title, grade)

        elif command == "new_project":
            title, description, max_grade = args
            make_new_project(title, description, max_grade)

        else:
            if command != "quit":
                print("Invalid Entry. Try again.")


if __name__ == "__main__":
    connect_to_db(app)

    handle_input()

    # To be tidy, we close our database connection -- though,
    # since this is where our program ends, we'd quit anyway.

    db.session.close()
