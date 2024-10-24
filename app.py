from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title="Página Inicial")

@app.route('/cpp')
def cpp():
    return render_template('cpp.html', title="C++")

@app.route('/db')
def db():
    return render_template('db.html', title="Banco de Dados")

@app.route('/java')
def java():
    return render_template('java.html', title="Java")

@app.route('/python')
def python():
    return render_template('python.html', title="Python")

@app.route('/prosscomp')
def prosscomp():
    return render_template('prosscomp.html', title="Processamento Computacional")

@app.route('/tecnologia')
def tecnologia():
    return render_template('tecnologia.html', title="Tecnologia")

@app.route('/reds')
def reds():
    return render_template('reds.html', title="Redes")

if __name__ == '__main__':
    app.run(debug=True)
