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


@app.route('/Debug')
def debug():
   db = get_db() 
   page = []
   page.append('<html><ul>')
   page.append('<li>Users</li>')
   sql = "SELECT * FROM users ORDER BY username"
   for row in db.cursor().execute(sql):
      page.append('<li>')
      page.append(str(row))
      page.append('</li>')

   page.append('<li>Insults</li>')
   sql = "SELECT * FROM insults ORDER BY username"
   for row in db.cursor().execute(sql):
      page.append('<li>')
      page.append(str(row))
      page.append('</li>')  
 
   
   page.append('</ul></html>')
   return ''.join(page)


@app.route('/')
def root():
   status = session.get('logged_in', False)
   if not status:
      return render_template('Home.html'), 200

   """page = []
   page.append('''
<html>
<head>
   <title>The VOID</title>
   <link href="{{ 'Mcluskey_Dominic_set09103_cw2/Sourcecode/static/', filename='css/bootstrap.min.css') }}" rel="stylesheet" />
   <style>
      body{
         padding-top: 50px;
         background-color: white;
      }
   </style>
</head>
<body>

   <nav class="navbar navbar-inverse navbar-fixed-top">
   <div class="container">
      <div class="navbar-header">
         <button type="button" class="navbar-toggle collapsed"
         data-toggle="collapse" data-target="#navbar" aria-expanded="false"
         aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="/">The VOID</a>
         </div>
         <div id="navbar" class="collapse navbar-collapse">
         <ul class="nav navbar-nav">
            <li><a href="/Hottest">Hottest</a></li>
            <li><a href="/Newest">Newest</a></li>
            <li><a href="/Categories">Categories</a></li>
            <li><a href="/SLogin">Login/Sign up</a></li>
         </ul>
         </div>
      </div>
   </nav>

   <div class="container">
       <h1>Home</h1>
       <p>Now you can post insults down below.</p>
''')
   
   db = get_db()
   data = db.cursor().execute("SELECT * FROM insults")
   data = data.fetchall()
   
   for value in (data):
        
        page.append('''     

        <div class="row">
        <div class="col-sm-3">
          <div class="well">
           <p>''')
        page.append(value[0])
        page.append('''        
           </p>
          </div>
        </div>
        <div class="col-sm-9">
          <div class="well">
            <p>''')
        page.append(value[1])
        page.append(''' 
            </p>
          <p><a href="/Tags">Tags</a></p>
          <p>
             <span class="label label-default">
        ''')
        page.append(value[2])
        page.append('''</span>
             <span class="label label-default">''')
        page.append(value[3])
        page.append('''</span>
             <span class="label label-default">''')
        page.append(value[4])
        page.append('''</span>
             <span class="label label-default">''')
        page.append(value[5])
        page.append('''</span>
             <span class="label label-default">''')
        page.append(value[6])
        page.append('''</span>
             <span class="label label-default">''')
        page.append(value[7])
        page.append('''</span>
          </p>
             <button type="button" class="btn btn-Success">Like<span class="badge">''')
        page.append(value[8])
        page.append('''</span></button>
             <button type="button" class="btn btn-Danger">Dislike<span class="badge">''')
        page.append(value[9])
        page.append('''</span></button>
          </div>
        </div>
        </div>''')
   
   page.append('''<div class="container">
	<div class="row">
		<div class="col-sm-3" style="padding-bottom:20">
            <form accept-charset="UTF-8" action="/Send" method="POST">
		<textarea rows="3" cols="50" id="new_insult" name="new_insult"
                placeholder="Type in your insult" style="font-size: 30pt"></textarea>
                <button class="btn btn-info" type="submit">Post New Insults</button>
        ''')
   page.append('''            <input type="text" value="" name="tag1" id="tag1">
            <label for="tag1"><b>Tag1</b></label>            
            <input type="text" value="" name="tag2" id="tag2">
            <label for="tag2"><b>Tag2</b></label>
          
            <input type="text" value="" name="tag3" id="tag3">
            <label for="tag3"><b>Tag3</b></label>         
            <input type="text" value="" name="tag4" id="tag4">
            <label for="tag4"><b>Tag4</b></label>
          
            <input type="text" value="" name="tag5" id="tag5">
            <label for="tag5"><b>Tag5</b></label> 
            <input type="text" value="" name="tag6" id="tag6">            
            <label for="tag6"><b>Tag6</b></label>
          </form>
        </div>
	</div>
</div>
   </div>
   <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
   <script src="{{ url_for('static', filename='js/bootstrap.min.js') }}"></script>
</body>''')

    
   page.append('</html>')
   return ''.join(page)"""
    
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
      #db = get_db()
      #db.cursor().execute("INSERT INTO insults(username,insult,tag1,tag2,tag3,tag4,tag5,tag6,likes,dislikes) VALUES (?,?,?,?,?,?,?,?,?,?)", (username, insult, tag1, tag2, tag3, tag4, tag5, tag6, likes, dislikes))
      #db.commit()
      #return redirect(url_for('.lcongrats'))
#return render_template('Congrats-s.html')

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
   return render_template('Hottest.html'), 200

@app.route('/Newest')
def newest():
   return render_template('Newest.html'), 200

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

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
