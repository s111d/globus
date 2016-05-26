Test tasks: https://docs.google.com/document/d/1g21iOerEXatdjdLZt8USag_1O6gSZcabjbv66rOCaLg/edit
*Both tasks are implemented in Python 3.*

#### Task 1
    The solution is in the `task-1.py` script.
    Running it is as simple as executing 'python task-1.py' in the shell.

#### Task 2
    The data is stored in Sqlite database ('main.db').
    To run the solution it is necessary to create a schema first and
    populate it with data:
        >>> from run import *
        >>> init_db()

    Then application itself is just a Flask app, can be started as following:
        $ python run.py

    The output will be available at the port 5000 of localhost.
    Due to the lack of time i decided to skip CSS and JS scripting,
    they are both pretty simple in this case.

    I had no time to comment Task 2 well, if you need more comments,
    please, let me know.


