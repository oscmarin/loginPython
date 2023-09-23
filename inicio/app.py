from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Configuración de la conexión a SQL Server
server = '192.168.20.100\\NOMINACR'
database = 'BDControlAsistencias'
username = 'sa'
password = 'P4n4m4V3n3zu3l4'
driver = 'SQL Server'

conn_str = f'SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver}'

def is_connection_successful():
    try:
        conn = pyodbc.connect(conn_str)
        conn.close()
        return True
    except pyodbc.Error:
        return False

@app.route('/')
def index():
    if is_connection_successful():
        return render_template('login.html')
    else:
        return 'Error de conexión con SQL Server'

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Establecer la conexión a SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Ejecutar una consulta para verificar las credenciales de inicio de sesión
    query = f"SELECT COUNT(*) FROM usuarios WHERE usuario='{username}' AND password='{password}'"
    cursor.execute(query)
    count = cursor.fetchone()[0]

    # Cerrar la conexión a SQL Server
    cursor.close()
    conn.close()

    if count == 1:
        return redirect(url_for('home'))  # Redireccionar a la página de inicio
    else:
        return 'Credenciales inválidas'

@app.route('/home')
def home():
    return '¡Inicio de sesión exitoso! Esta es tu página de inicio.'

if __name__ == '__main__':
    app.run()