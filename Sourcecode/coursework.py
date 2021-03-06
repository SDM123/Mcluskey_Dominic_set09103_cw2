import bcrypt
from functools import wraps
from flask import Flask, render_template, redirect, request, session, g, url_for
import sqlite3
app = Flask(__name__)
db_location = 'var/Data.db'


def get_db():
   db = getattr(g, 'db', None)
   if db is None:
      db = sqlite3.connect(db_location)
      g.db = db
   return db


@app.teardown_appcontext
def close_db_connection(exception):
   db = getattr(g, 'db', None)
   if db is not None:
      db.close()


def init_db():
   with app.app_context():
      db = get_db()
      with app.open_resource('schema.sql', mode='r') as f:
         db.cursor().executescript(f.read())
      db.commit()

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


def requires_login(f):
   @wraps(f)
   def decorated(*args, **kwargs):
      status = session.get('logged_in', False)
      if not status:
         return redirect(url_for('.root'))
      return f(*args, **kwargs)
   return decorated


@app.route('/Logout')
def logout():
   session['logged_in'] = False
   session['user'] = None
   return redirect(url_for('.root'))

#Removed for security purposes
#@app.route('/Debug')
#def debug():
#   db = get_db() 
#   page = []
#   page.append('<html><ul>')
#   page.append('<li>Users</li>')
#   sql = "SELECT * FROM users ORDER BY username"
#   for row in db.cursor().execute(sql):
#      page.append('<li>')
#      page.append(str(row))
#      page.append('</li>')

#   page.append('<li>Insults</li>')
#   sql = "SELECT * FROM insults ORDER BY username"
#   for row in db.cursor().execute(sql):
#      page.append('<li>')
#      page.append(str(row))
#      page.append('</li>')  
 
   
#   page.append('</ul></html>')
#   return ''.join(page)


@app.route('/')
def root():
   status = session.get('logged_in', False)
   if not status:
      
      username = []
      insult = []
      tag1 = []
      tag2 = []
      tag3 = []
      tag4 = []
      tag5 = []
      tag6 = []
      likes = []
      dislikes = []

      count = []
      number = 0


      db = get_db()
      data = db.cursor().execute("SELECT * FROM insults")
      data = data.fetchall()
      for value in (data):
         username.append(value[0])
         insult.append(value[1])
         tag1.append(value[2])
         tag2.append(value[3])
         tag3.append(value[4])
         tag4.append(value[5])
         tag5.append(value[6])
         tag6.append(value[7])
         likes.append(value[8])
         dislikes.append(value[9])
         count.append(number)
         number = number + 1
       


      return render_template('Home.html', count = count, username = username, insult = insult, tag1 = tag1, tag2 = tag2, tag3 = tag3, tag4 = tag4, tag5 = tag5, tag6 = tag6, likes = likes, dislikes = dislikes)

    
   username = []
   insult = []
   tag1 = []
   tag2 = []
   tag3 = []
   tag4 = []
   tag5 = []
   tag6 = []
   likes = []
   dislikes = []

   count = []
   number = 0


   db = get_db()
   data = db.cursor().execute("SELECT * FROM insults")
   data = data.fetchall()
   for value in (data):
      username.append(value[0])
      insult.append(value[1])
      tag1.append(value[2])
      tag2.append(value[3])
      tag3.append(value[4])
      tag4.append(value[5])
      tag5.append(value[6])
      tag6.append(value[7])
      likes.append(value[8])
      dislikes.append(value[9])
      count.append(number)
      number = number + 1
       


   return render_template('Home-l.html', count = count, username = username, insult = insult, tag1 = tag1, tag2 = tag2, tag3 = tag3, tag4 = tag4, tag5 = tag5, tag6 = tag6, likes = likes, dislikes = dislikes)






@app.route("/Register", methods=['GET', 'POST'])
def register():
   if request.method == 'POST':
      username = request.form['usr-s']
      password = request.form['psw-s']
      passwordrepeat = request.form['psw-repeat']
     
      password = password.encode('utf-8')
      
      spwd = bcrypt.hashpw(password, bcrypt.gensalt())
     
      check = False
       
      db = get_db()
      data = db.cursor().execute("SELECT username FROM users WHERE username = '"+username+"'")
      data = data.fetchall()
      names = {name[0] for name in data}
      
      if(username in names):
         check = True
       
       
      if(username is not None and password is not None and passwordrepeat == password and check is False):
         db = get_db()
         db.cursor().execute("INSERT INTO users(username,password) VALUES (?,?)", (username, spwd))
         db.commit()
         return redirect(url_for('.scongrats'))
   return render_template('Error-s.html')


@app.route("/Login", methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
      
      username = request.form['usr-l']
      password = request.form['psw-l']
      
      db = get_db()
      data = db.cursor().execute("SELECT username, password FROM users WHERE username = '"+username+"'") 
      data = data.fetchall()
      
      password = password.encode('utf-8')
       
      for value in (data):
         if (username == value[0] and value[1].encode('utf-8') == bcrypt.hashpw(password, value[1].encode('utf-8'))):
            session['logged_in'] = True
            session['user'] = username
            return redirect(url_for('.lcongrats'))
         return render_template('Error-l.html')


@app.route('/Send', methods=['GET', 'POST'])
def send():
   if request.method == 'POST':
      
      username = session['user']
      insult = request.form['new_insult']
      tag1 = request.form['tag1']
      tag2 = request.form['tag2']      
      tag3 = request.form['tag3']
      tag4 = request.form['tag4']
      tag5 = request.form['tag5']
      tag6 = request.form['tag6']
      likes = 0
      dislikes = 0      

  
      db = get_db()
      db.cursor().execute("INSERT INTO insults(username,insult,tag1,tag2,tag3,tag4,tag5,tag6,likes,dislikes) Values (?,?,?,?,?,?,?,?,?,?)", (username, insult, tag1, tag2, tag3, tag4, tag5, tag6, likes, dislikes))
      db.commit()
            

      return redirect(url_for('.root'))


@app.route('/Congrats-s')
def scongrats():
   return render_template('Congrats-s.html'), 200


@app.route('/Congrats-l')
def lcongrats():
   return render_template('Congrats-l.html'), 200


@app.route('/Error-l')
def lerror():
   return render_template('Error-l.html'), 200


@app.route('/Error-s')
def serror():
   return render_template('Error-s.html'), 200


@app.route('/Hottest')
def hottest():
   username = []
   insult = []
   tag1 = []
   tag2 = []
   tag3 = []
   tag4 = []
   tag5 = []
   tag6 = []
   likes = []
   dislikes = []

   count = []
   number = 0


   db = get_db()
   data = db.cursor().execute("SELECT * FROM insults ORDER BY likes desc")
   data = data.fetchall()
   for value in (data):
      username.append(value[0])
      insult.append(value[1])
      tag1.append(value[2])
      tag2.append(value[3])
      tag3.append(value[4])
      tag4.append(value[5])
      tag5.append(value[6])
      tag6.append(value[7])
      likes.append(value[8])
      dislikes.append(value[9])
      
      if(number < 3):
         count.append(number)

      number = number + 1
       


   return render_template('Hottest.html', count = count, username = username, insult = insult, tag1 = tag1, tag2 = tag2, tag3 = tag3, tag4 = tag4, tag5 = tag5, tag6 = tag6, likes = likes, dislikes = dislikes)



@app.route('/Newest')
def newest():
   username = []
   insult = []
   tag1 = []
   tag2 = []
   tag3 = []
   tag4 = []
   tag5 = []
   tag6 = []
   likes = []
   dislikes = []

   count = []
   number = 0


   db = get_db()
   data = db.cursor().execute("SELECT * FROM insults")
   data = data.fetchall()
   for value in (data):
      username.append(value[0])
      insult.append(value[1])
      tag1.append(value[2])
      tag2.append(value[3])
      tag3.append(value[4])
      tag4.append(value[5])
      tag5.append(value[6])
      tag6.append(value[7])
      likes.append(value[8])
      dislikes.append(value[9])
      number = number + 1
   
   count.append(number)
   number = number - 1
   count.append(number)
   number = number - 1
   count.append(number)


   return render_template('Newest.html', count = count, username = username, insult = insult, tag1 = tag1, tag2 = tag2, tag3 = tag3, tag4 = tag4, tag5 = tag5, tag6 = tag6, likes = likes, dislikes = dislikes)




@app.route('/SLogin')
def slogin():
   status = session.get('logged_in', False)
   if not status:
       return render_template('SLogin.html'), 200
   return render_template('Logout.html'), 200


@app.route('/Tags')
def tags():
   return render_template('Tags.html'), 200

@app.route('/Categories')
def categories():
   return render_template('Tags.html'), 200

@app.route('/Tags/Appearance')
def appearance():
   return render_template('Appearance.html'), 200

@app.route('/Tags/Teeth')
def teeth():
   return render_template('Teeth.html'), 200

@app.route('/Tags/Political')
def political():
   return render_template('Political.html'), 200

@app.route('/Tags/Yourmother')
def yourmother():
   return render_template('Yourmother.html'), 200

@app.route('/Tags/Subversion')
def subversion():
   return render_template('Subversion.html'), 200

@app.route('/Tags/Dissapointment')
def dissapointment():
   return render_template('Dissapointment.html'), 200

@app.route('/Tags/Disability')
def disability():
   return render_template('Disability.html'), 200

@app.route('/Tags/Virginshaming')
def virginshaming():
   return render_template('Virginshaming.html'), 200

@app.route('/Tags/Voice')
def voice():
   return render_template('Voice.html'), 200

@app.route('/Tags/Simple')
def simple():
   return render_template('Simple.html'), 200

@app.route('/Tags/Hair')
def hair():
   return render_template('Hair.html'), 200

@app.route('/Tags/Skin')
def skin():
   return render_template('Skin.html'), 200

@app.route('/Tags/Beastiality')
def beastiality():
   return render_template('Beastiality.html'), 200

@app.route('/Tags/Sheep')
def sheep():
   return render_template('Sheep.html'), 200

@app.route('/Tags/Zombie')
def zombie():
   return render_template('Zombie.html'), 200

@app.route('/Tags/Killing')
def killing():
   return render_template('Killing.html'), 200

@app.route('/Tags/Indirect')
def indirect():
   return render_template('Indirect.html'), 200

@app.route('/Tags/Intelligence')
def intelligence():
   return render_template('Intelligence.html'), 200

@app.route('/Tags/Hellokitty')
def hellokitty():
   return render_template('Hellokitty.html'), 200

@app.route('/Tags/Pun')
def pun():
   return render_template('Pun.html'), 200

@app.route('/Tags/Reference')
def reference():
   return render_template('Reference.html'), 200

@app.errorhandler(404)
def page_not_found(error):
   return render_template('Error.html')

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
