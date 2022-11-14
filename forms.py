from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

DEPARTMENTS = [' ', 'Fianace School', 'Engineering School', 'Statistics School', 'Art Schools', 'Law School', 'Humanities School', 'Economics School', 'Physics School', 'Environment School', 'Materials School']
PROGRAMS = [' ', 'Operations research', 'applied mathematics', 'Applied Physics', 'data science', 'Social Research', 'Software Engineering', 'Historical Research', 'Finance', 'Financial Economy', 'International Laws']
PROFESSORS = [' ', 'Gus', 'Maryan', 'Mukhtar', 'Relinda', 'Sylvia', 'John', 'Kade', 'Antony', 'Irfan', 'Naoual']
BUILDINGS = [' ', 'Barnard Hall', '80 Claremont', 'Hamilton Hall', 'Fayerweather', 'Casa Hispanica', 'Hartley Hall', 'Kent Hall', 'Kraft Center', 'Macy Hall', 'Uris Hall']
ROOMS = [' ', 101, 269, 382, 401, 221, 311, 823, 597, 212, 118]
YEARS = [' ', 2019, 2020, 2021, 2022]
SEMESTERS = [' ', 'Spring', 'Summer', 'Fall' , 'Winter']
DAYS = [' ']
PERIODS = [' ']


class SearchForm(FlaskForm):
    cid = StringField('Course ID') # Course
    cname = StringField('Course name') # Course
    department = SelectField('Department', choices=DEPARTMENTS) # offer_dep
    program = SelectField('Program', choices=PROGRAMS) # offer_pro
    professor = SelectField('Professor', choices=PROFESSORS) # teach
    building = SelectField('Building', choices=BUILDINGS) # Term_at
    room = SelectField('Room', choices=ROOMS) # Term_at
    year = SelectField('Year', choices=YEARS) # Term_when
    semester = SelectField('Semester', choices=SEMESTERS) # Term_when
    day = SelectField('Day', choices=DAYS) # Term_when
    period = SelectField('Period', choices=PERIODS) # Term_when

    submit = SubmitField('Search')

class StudentForm(FlaskForm):
    sid = StringField('Student ID', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

    submit = SubmitField('Login')

class ProfessorForm(FlaskForm):
    professor = StringField('Professor name') # teach
    department = SelectField('Department', choices=DEPARTMENTS) # offer_dep
    program = SelectField('Program', choices=PROGRAMS) # offer_pro
    building = SelectField('Building', choices=BUILDINGS) # Term_at
    room = SelectField('Room', choices=ROOMS) # Term_at

    submit = SubmitField('Search')