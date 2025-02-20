from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Usa la plantilla index.html

@app.route('/about')
def about():
    return render_template('about.html')  # Usa la plantilla about.html

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return render_template('index.html', usuario=nombre)  # Envía el nombre a la plantilla

if __name__ == '__main__':
    app.run(debug=True)
