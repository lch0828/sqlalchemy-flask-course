
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python3 server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for, session, flash
from forms import SearchForm, StudentForm, ProfessorForm
from datetime import datetime, timedelta
import time

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of:
#
#     postgresql://USER:PASSWORD@34.75.94.195/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@34.75.94.195/proj1part2"
#
DATABASEURI = "postgresql://cl4335:955@34.75.94.195/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  if not session.get('logged_in'):
    session['logged_in'] = False
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/home')
def home():
  return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = StudentForm()
  if form.validate_on_submit():
    id = g.conn.execute('SELECT sid FROM Stu_enrl WHERE sid = (%s)', form['sid'].data)
    if id.all():
      pw = g.conn.execute('SELECT password FROM Stu_enrl WHERE sid = (%s)', form['sid'].data)
      pw = pw.all()[0][0]
      #print(pw, flush=True)
      if pw == form['password'].data:
        session['logged_in'] = True
        session['user'] = form['sid'].data
        return redirect(url_for('mylist', user = form['sid'].data))
      else:
        flash('Wrong password!')
    else:
      flash('Wrong student ID')
  return render_template("login.html", form=form)

@app.route('/logout')
def logout():
  session['logged_in'] = False
  session.pop('user', None)
  return redirect(url_for('home'))

@app.route('/mylist/<user>', methods=['GET', 'POST'])
def mylist(user):
  courses = g.conn.execute('''SELECT C.cid, C.cname, od.dname, Pb.pname, Pf.prname, Pf.building, Pf.room, t.year, t.semester, Tw.day, Tw.start_period, Tw.end_period
            FROM Course C, offer_dep od, Prog_blg Pb, Prof_fac_off Pf, teach t, Term_when_at Tw, register R
            WHERE C.cid = od.cid 
            AND od.dname = Pb.dname 
            AND Pb.pname = Pf.pname 
            AND Pf.pid = t.pid 
            AND t.cid = Tw.cid 
            AND t.year = Tw.year 
            AND t.semester = Tw.semester
            AND R.cid = Tw.cid
            AND R.year = Tw.year
            AND R.semester = Tw.semester
            AND R.sid = (%s)''', user)
  
  return render_template("mylist.html", result = courses)

@app.route('/myprofile/<user>', methods=['GET', 'POST'])
def myprofile(user):
  profile = g.conn.execute('''SELECT sid, sname, year, gpa, pname FROM Stu_enrl WHERE sid = (%s)''', user)
  
  return render_template("myprofile.html", result = profile)

FIELDS = ['cid', 'cname', 'department', 'program', 'professor', 'building', 'room', 'year', 'semester', 'day']
SQL_FIELDS = ['C.cid', 'C.cname', 'od.dname', 'Pb.pname', 'Pf.prname', 'Pf.building', 'Pf.room', 'Tw.year', 'Tw.semester', 'Tw.day']
@app.route('/search', methods=['GET', 'POST'])
def search():
  form = SearchForm()

  if form.validate_on_submit():
    clauses = []
    values = []
    for field,sql in zip(FIELDS, SQL_FIELDS):
      if form[field].data != ' ' and form[field].data != '':
        clauses.append('AND ' + sql + '=%s')
        values.append(form[field].data)
    if values:
      query = '''SELECT C.cid, C.cname, od.dname, Pb.pname, Pf.prname, Pf.building, Pf.room, t.year, t.semester, Tw.day, Tw.start_period, Tw.end_period
            FROM Course C, offer_dep od, Prog_blg Pb, Prof_fac_off Pf, teach t, Term_when_at Tw
            WHERE C.cid = od.cid 
            AND od.dname = Pb.dname 
            AND Pb.pname = Pf.pname 
            AND Pf.pid = t.pid 
            AND t.cid = Tw.cid 
            AND t.year = Tw.year 
            AND t.semester = Tw.semester '''
      for clause in clauses:
        query += clause

      result = g.conn.execute(query, tuple(values))
      return render_template('search_result.html', form=form, result=result)

  return render_template("search.html", form=form)

PFIELDS = ['professor', 'department', 'program', 'building', 'room']
SQL_PFIELDS = ['Pf.prname', 'Pb.dname', 'Pf.pname', 'Pf.building', 'Pf.room']
@app.route('/professor', methods=['GET', 'POST'])
def professor():
  form = ProfessorForm()

  if form.validate_on_submit():
    clauses = []
    values = []
    for field,sql in zip(PFIELDS, SQL_PFIELDS):
      if form[field].data != ' ' and form[field].data != '':
        clauses.append('AND ' + sql + '=%s')
        values.append(form[field].data)
    if values:
      query = '''SELECT Pf.prname, Pb.dname, Pf.pname, Pf.building, Pf.room
                 FROM Prof_fac_off Pf, Prog_blg Pb
                 WHERE Pf.pname = Pb.pname '''
      for clause in clauses:
        query += clause
      print(query, flush=True)
      result = g.conn.execute(query, tuple(values))
      return render_template('professor_result.html', form=form, result=result)

  return render_template("professor.html", form=form)

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python3 server.py

    Show the help text using:

        python3 server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
