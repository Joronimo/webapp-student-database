"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect, session

import hackbright as hb

app = Flask(__name__)

@app.route("/ask-student-type")
def get_student_type_form():
    """asks if student is new or existing"""

    return render_template("student_type.html")

@app.route("/student-type-choice")
def type_of_student():
    """redirects to appropriate page based on choice of new or existing student."""

    student_type = request.args.get('student_type')

    if student_type == "existing":
        return redirect("/student-search")
    elif student_type == "new":
        return redirect("/new-student")

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/new-student")
def get_new_student_form():
    """Show form for adding a new student."""

    return render_template("new_student.html")

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hb.get_student_by_github(github)

    projects = hb.get_student_projects_and_grades(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           projects=projects)

    return html

@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""

    first_name = request.form.get('fname')
    last_name = request.form.get('lname')
    github = request.form.get('github')

    first_name, last_name, github = hb.make_new_student(first_name, last_name, github)

    html = render_template("student_added.html", github=github)

    return html

@app.route("/project")
def project_info():
    """Link to information about a project."""

    title = request.args.get('title')

    title, description, max_grade = hb.get_project_by_title(title)

    students = hb.get_project_student_and_grade(title)

    print("STUDENTS: ", students)

    html = render_template("project_info.html", title=title,
                            description=description, 
                            max_grade=max_grade,
                            students=students)

    return html

if __name__ == "__main__":
    hb.connect_to_db(app)
    app.run(debug=True)
