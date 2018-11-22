from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def root():
   return render_template('Home.html'), 200

@app.route('/Tags')
def tags():
   return render_template('Tags.html'), 200

@app.route('/Tags/Appearance')
def appearance():
   return render_template('Appearance.html'), 200




if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
