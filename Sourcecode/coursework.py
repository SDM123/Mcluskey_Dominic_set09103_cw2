from functools import wraps
from flask import Flask, render_template, redirect, request, session
app = Flask(__name__)


@app.route('/')
def root():
   return render_template('Home.html'), 200


#@app.route("/Register", methods=['GET', 'POST'])
#def register():
#   if request.method == 'POST'
#   username = request.form['usr-s']
#   password = request.form['psw-s']
#   password-repeat = request.form['psw-repeat']
#   if(username is not None and password is not None and password-repeat == password):
#      db = get_db()
#      db.cursor().execute("INSERT INTO users(username,password) VALUES (?,?,?)", (username, password))
#      db.commit()
#      return redirect(url_for('.SLogin'))
#return render_template('SLogin.html')


@app.route('/Congrats')
def congrats():
   return render_template('Congrats.html'), 200

@app.route('/Hottest')
def hottest():
   return render_template('Hottest.html'), 200

@app.route('/Newest')
def newest():
   return render_template('Newest.html'), 200

@app.route('/SLogin')
def slogin():
   return render_template('SLogin.html'), 200



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
