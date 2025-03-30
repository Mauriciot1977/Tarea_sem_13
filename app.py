from flask import Flask, render_template, redirect, url_for, jsonify,request,flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import json
import csv
import os
from conexion.conexion import obtener_conexion  # Importa la conexión MySQL
from models import models
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user



app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta'  # Clave secreta para los formularios

# Archivos para persistencia
TXT_FILE = "nombres.txt"
JSON_FILE = "nombres.json"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user_data = models.get_by_id(user_id)
    print(f"❌ user_data::: {user_data.username}")
    if user_data:
        return models.User(user_data.id, user_data.username)
    return None

# Definir el formulario con FlaskForm
class NombreForm(FlaskForm):
    nombre = StringField('Ingresa tu nombre:', validators=[DataRequired()])
    submit = SubmitField('Enviar')

# Función para guardar en TXT
def guardar_en_txt(nombre):
    with open(TXT_FILE, "a", encoding="utf-8") as file:
        file.write(nombre + "\n")

# Función para leer de TXT
def leer_desde_txt():
    if os.path.exists(TXT_FILE):
        with open(TXT_FILE, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]
    return []

# Función para guardar en JSON
def guardar_en_json(nombre):
    datos = leer_desde_json()
    datos.append(nombre)
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(datos, file, indent=4)

# Función para leer de JSON
def leer_desde_json():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

# Función para guardar en CSV
def guardar_en_csv(nombre):
    existe = os.path.exists(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not existe:
            writer.writerow(["Nombre"])  # Agregar encabezado si es nuevo
        writer.writerow([nombre])

# Función para leer de CSV
def leer_desde_csv():
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # Saltar encabezado
            return [row[0] for row in reader]
    return []


# Función para guardar en MySQL
def guardar_en_mysql(nombre):
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO usuarios (nombre) VALUES (%s)", (nombre,))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

# Función para leer de MySQL
def leer_desde_mysql():
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre FROM nombres")
            nombres = [fila[0] for fila in cursor.fetchall()]
            return nombres
        finally:
            cursor.close()
            conexion.close()
    return []

# Ruta principal
@app.route('/')
def home():
    print(f"❌ Ingresa::: {current_user}")
    return render_template('index.html', usuario=current_user)

# Ruta "Acerca de"
@app.route('/about')
@login_required
def about():
    return render_template('about.html', usuario=current_user)


@app.route('/test_db')
def test_db():
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT 'Conexión exitosa a MySQL desde Flask!'")
        mensaje = cursor.fetchone()[0]

        cursor.close()
        conexion.close()

    else:
        mensaje = "Error de conexión a la base de datos."

    return mensaje

@app.route('/usuarios_formularios')
def usuarios_formularios():
    conexion = obtener_conexion()
    if conexion:

        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        registros = cursor.fetchall()

        for fila in registros:
            print(fila)

        cursor.close()
        conexion.close()
        return render_template('tabla.html', registros=registros)
    else:
        mensaje = "Error de conexión a la base de datos."

    return mensaje


# Ruta para el formulario
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = NombreForm()
    if form.validate_on_submit():
        nombre = form.nombre.data.strip()
        guardar_en_txt(nombre)
        guardar_en_json(nombre)
        guardar_en_csv(nombre)
        guardar_en_mysql(nombre)  # Guardar en MySQL también
        return redirect(url_for('resultado', nombre=nombre))
    return render_template('formulario.html', form=form)

# Ruta para mostrar el resultado
@app.route('/resultado/<nombre>')
def resultado(nombre):
    return render_template('resultado.html', nombre=nombre)

# Ruta para obtener los nombres desde TXT
@app.route('/leer_txt')
def leer_txt():
    nombres = leer_desde_txt()
    return jsonify(nombres=nombres)

# Ruta para obtener los nombres desde JSON
@app.route('/leer_json')
def leer_json():
    nombres = leer_desde_json()
    return jsonify(nombres=nombres)

# Ruta para obtener los nombres desde CSV
@app.route('/leer_csv')
def leer_csv():
    nombres = leer_desde_csv()
    return jsonify(nombres=nombres)

# Ruta para obtener los nombres desde MySQL
@app.route('/leer_mysql')
def leer_mysql():
    nombres = leer_desde_mysql()
    return jsonify(nombres=nombres)

@app.route('/register', methods=['GET', 'POST'])
def register():
    conexion = obtener_conexion()
    if request.method == 'POST':
        username = request.form['username']
        password =request.form['password']
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)", (username, password))
                conexion.commit()
                flash('Usuario registrado correctamente', 'success')
                return redirect(url_for('usuarios_formularios'))
            finally:
                cursor.close()
                conexion.close()
    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    conexion = obtener_conexion()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = conexion.cursor()
        cursor.execute("SELECT id, username, password FROM usuarios WHERE username = %s and password= %s", (username,password))
        user = cursor.fetchone()
        cursor.close()

        if user :
            user_obj = models.User(user[0], user[1])
            login_user(user_obj)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('home'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
