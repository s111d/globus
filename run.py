import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from collections import defaultdict as dd

# configuration
DATABASE = 'main.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

GPA_SCORES = {'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C': 2.0, 'C-': 1.7}
QUARTER_DECODED = {1: 'Fall', 2: 'Winter', 3: 'Spring'}

app = Flask(__name__)
app.config.from_object(__name__)


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    """
        Create schema and initial data.

        We'll make courses a separate object because each iteration of the course
        can have different attributes, for example, different professor depending
        on the year, total hours, etc. (at least in theory)

        Quarter is stored directly as 1..4 and decoded in the app code.
    """
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_gpa(student_id):
    assert type(student_id) == int
    cur = g.db.execute('SELECT mark '
                       'FROM student_course_link '
                       'WHERE student_id = %s' % student_id)
    results = cur.fetchall()
    if results:
        return round(sum([GPA_SCORES[mark[0]] for mark in results])/len(results), 2)


def get_grades_by_quarter(student_id):
    assert type(student_id) == int
    cur = g.db.execute('SELECT c.name, scl.mark, c.year, c.quarter '
                       'FROM student_course_link scl '
                       'JOIN course c on scl.course_id = c.id '
                       'WHERE scl.student_id = %s '
                       'ORDER BY year, quarter' % student_id)
    results = cur.fetchall()

    groupped = dd(list)

    for row in results:
        quarter_full_name = str(QUARTER_DECODED[row[3]]) + ' ' + str(row[2])
        groupped[quarter_full_name].append(dict(name=row[0], mark=row[1]))

    return groupped


@app.route('/')
def index():
    """
        Display list of students
    """
    cur = g.db.execute('select id, first_name, last_name from student')
    students = [dict(id=row[0], name=row[1] + ' ' + row[2]) for row in cur.fetchall()]
    return render_template('index.html', students=students)


@app.route('/student/<int:student_id>')
def detail(student_id):
    """
        Display student details and scores
    """
    cur = g.db.execute('SELECT s.id, s.first_name, s.last_name, m.name '
                       'FROM student s JOIN major m ON s.major_id = m.id '
                       'WHERE s.id = %s' % student_id)

    # TODO: consider replacing with one-row fetch
    student_details = cur.fetchall()

    if not student_details:
        abort(404)

    name = student_details[0][1] + ' ' + student_details[0][2]

    grades = get_grades_by_quarter(student_id)

    return render_template('detail.html',
                           name=name,
                           id=student_details[0][0],
                           major_name=student_details[0][3],
                           gpa=get_gpa(student_id),
                           grades=grades)


def load_random_data():
    """
        Load more fake data.
        Not finished.
    """
    import random
    male_names = ['John', 'Bill', 'Tom', 'Edward', 'Frank']
    female_names = ['Tina', 'Melinda', 'Amanda', 'Victoria', 'Olivia']
    last_names = ['Doe', 'Smith', 'Lee', 'Parker', 'Fox', 'Silver', 'Lopez', 'de Souza']
    random_names = set([(random.choice(male_names + female_names),
                         random.choice(last_names)) for _ in range(15)])

    with closing(connect_db()) as db:
        db.cursor().execute('delete from student')

        for k, v in enumerate(random_names):
            db.cursor().execute('insert into student values (%s, %s, "%s", "%s")' %
                         (k+2, random.choice(range(1, 5)), v[0], v[1]))
        db.commit()

    # TODO: generate fake scores

    print(random_names)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

