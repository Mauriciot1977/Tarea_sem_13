from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta'  # Clave secreta para los formularios

# Definir el formulario con FlaskForm
class NombreForm(FlaskForm):
    nombre = StringField('Ingresa tu nombre:', validators=[DataRequired()])
    submit = SubmitField('Enviar')

# Ruta principal
@app.route('/')
def home():
    return render_template('index.html')

# Ruta "Acerca de"
@app.route('/about')
def about():
    return render_template('about.html')

# Ruta para el formulario
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = NombreForm()
    if form.validate_on_submit():
        return redirect(url_for('resultado', nombre=form.nombre.data))
    return render_template('formulario.html', form=form)

# Ruta para mostrar el resultado
@app.route('/resultado/<nombre>')
def resultado(nombre):
    return render_template('resultado.html', nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)
