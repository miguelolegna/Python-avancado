
from flask import Flask, render_template
from flask_assets import Environment, Bundle

app = Flask(__name__)

# Configurar Flask-Assets
assets = Environment(app)

# Definir um bundle para o SCSS
scss = Bundle('scss/styles.scss', filters='libsass', output='css/styles.css')
assets.register('scss_all', scss)

@app.route('/')  # URL: http://127.0.0.1:5000/index
def index():
    return render_template('index.html')

@app.route('/java')   # URL: http://127.0.0.1:5000/JAVA
def java():
    return render_template('java.html')

@app.route('/python') # URL: http://127.0.0.1:5000/python
def python():
    return render_template('python.html')

@app.route('/cpp')    # URL: http://127.0.0.1:5000/cpp

def cpp():
    return render_template('cpp.html')

@app.route('/db')     # URL: http://127.0.0.1:5000/db
def database():
    return render_template('db.html')

@app.route('/reds')  # URL: http://127.0.0.1:5000/redes
def networks():
    return render_template('reds.html')

@app.route('/pross-comp')  # URL: http://127.0.0.1:5000/pross-comp
def computing():
    return render_template('pross-comp.html')

if __name__ == '__main__':
    app.run(debug=True)
    