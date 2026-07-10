import sqlite3
from flask import Flask, request, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

HTML_LOGIN = '''
<!DOCTYPE html>
<html>
<head><title>Login DRY7122</title></head>
<body>
    <h2>Portal de Acceso - Examen Transversal</h2>
    <form action="/login" method="post">
        Usuario: <input type="text" name="usuario"><br><br>
        Clave: <input type="password" name="clave"><br><br>
        <input type="submit" value="Ingresar">
    </form>
</body>
</html>
'''

def preparar_base_datos():
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS credenciales
                      (id INTEGER PRIMARY KEY, usuario TEXT, hash TEXT)''')
    cursor.execute('DELETE FROM credenciales')

    integrantes = [
        ("alonso", "vega"),
        ("rodolfo", "verdejo")
    ]
    

    for user, pwd in integrantes:
        pwd_hash = generate_password_hash(pwd)
        cursor.execute("INSERT INTO credenciales (usuario, hash) VALUES (?, ?)", (user, pwd_hash))
        
    conexion.commit()
    conexion.close()

@app.route('/')
def inicio():
    return render_template_string(HTML_LOGIN)

@app.route('/login', methods=['POST'])
def login():
    user = request.form['usuario']
    pwd = request.form['clave']
    
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT hash FROM credenciales WHERE usuario=?", (user,))
    resultado = cursor.fetchone()
    conexion.close()
    
    if resultado and check_password_hash(resultado[0], pwd):
        return f"<h3>¡Acceso concedido! Hola {user}.</h3>"
    else:
        return "<h3>Acceso denegado. Revisa tus credenciales.</h3>"

if __name__ == '__main__':
    preparar_base_datos()
    print("Base de datos lista. Levantando servidor en el puerto 5800...")
    app.run(host='0.0.0.0', port=5800)