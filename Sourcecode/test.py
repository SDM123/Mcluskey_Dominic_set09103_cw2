from flask import Flask, g
import sqlite3

from flask import Flask
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

def init_db_values():
   with app.app_context():
      db = get_db()
      with app.open_resource('schema.sql', mode='r') as f:
         db.cursor().execute('insert into users values ("iJohn", "isFake")')
         db.cursor().execute('insert into users values ("AmJooke", "isFake")')
         db.cursor().execute('insert into users values ("katZ", "isFake")')
         db.cursor().execute('insert into users values ("BadBoiiiiiii", "isFake")')
         db.cursor().execute('insert into users values ("GreenMean", "isFake")')
         db.cursor().execute('insert into users values ("FranztheBaddie", "isFake")')
         db.cursor().execute('insert into users values ("OrangeManBad", "isFake")')
         db.cursor().execute('insert into users values ("ZaNPC", "isFake")')
         db.cursor().execute('insert into users values ("Monty", "isFake")')

         db.cursor().execute('insert into insults values ("BadBoiiiiiii", "Your voice is so annoying.", "Voice", "Simple", "", "", "", "", "1", "20")')
         db.cursor().execute('insert into insults values ("iJohn", "Your teeth are almost as crooked, as the political party you support.", "Political", "Teeth", "Appearance", "", "", "", "20", "5")')
         db.cursor().execute('insert into insults values ("AmJooke", "Your mother is such a nice lady, shame she wont walk again with so much dissapointment weighing her down.", "Your mother", "Subversion", "Dissapointment", "Disability", "" ,"", "43", "2")')
         db.cursor().execute('insert into insults values ("katZ", "Your forehead is more like a 10head. Thats 10 more head than you will ever get.", "Virgin shaming", "Appearance", "", "", "", "", "10", "2")')
         db.cursor().execute('insert into insults values ("iJohn", "Have you ever considered why you such a hard time with romantic encounters? You would assume its because of your bad hair, bad skin and fugly bod. But no that does not come close to describing your flaws.", "Virgin shaming", "Hair", "Skin", "Appearance", "Subversion", "", "10", "10")')
         db.cursor().execute('insert into insults values ("GreenMean", "I would call you a sheep shagger but sheep have higher standards.", "Beastiality", "Virgin shaming?", "Sheep", "", "", "", "10", "15")')
         db.cursor().execute('insert into insults values ("FranztheBaddie", "I wish a zombie apocalypse happens so I can kill you twice.", "Zombie", "Killing", "", "", "", "", "5", "2")')
         db.cursor().execute('insert into insults values ("OrangeManBad", "Putting Trump next to you makes it look like a smart well composed man is in the whitehouse. But then you leave and the bar is raised.", "Political", "Indirect", "Intelligence", "", "", "", "7", "15")')
         db.cursor().execute('insert into insults values ("ZaNPC", "You so ugly hello kitty says Bye Bye to you.", "Hello Kitty", "Appearance", "Pun", "", "", "", "30", "2")')
         db.cursor().execute('insert into insults values ("Monty", "Your mother was a hamster and your father smelt of elderberries.", "Reference", "", "", "", "", "", "10", "5")')

      db.commit()

@app.route("/")
def root():
   db = get_db()
   db.cursor().execute('insert into users values ("Test", "Test")')
   db.commit()

   page = []
   page.append('<html><ul>')
   sql = "SELECT rowid, * FROM users ORDER BY username"
   for row in db.cursor().execute(sql):
      page.append('<li>')
      page.append(str(row))
      page.append('</li>')

   page.append('<ul><html>')
   return ''.join(page)

if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)
