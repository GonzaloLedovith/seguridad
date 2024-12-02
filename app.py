import re
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_bcrypt import Bcrypt
from werkzeug.security import check_password_hash
from flask_mysqldb import MySQL

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Configuración de la base de datos
SECRET_KEY = 'mi_clave_secreta'  # Clave secreta para JWT
app.secret_key = 'your_secret_key'  # Cambia esto por algo seguro
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'agenda'
mysql = MySQL(app)


# Configuración del logger
logging.basicConfig(level=logging.INFO,  # Nivel de logging
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Formato del log
                    handlers=[logging.FileHandler('app.log'),  # Guarda los logs en un archivo
                              logging.StreamHandler()])  # También muestra los logs en la consola

logger = logging.getLogger(__name__)


# Ruta para el inicio
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# Ruta para registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener datos del formulario
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        birthdate = request.form.get('birthdate')

        # Validaciones
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        phone_regex = r'^\d{10}$'

        if not re.match(email_regex, email):
            flash('Correo inválido. Asegúrate de usar un formato válido.')
            return render_template('register.html')

        if not username or len(username) < 3 or len(username) > 20:
            flash('El nombre de usuario debe tener entre 3 y 20 caracteres.')
            return render_template('register.html')

        if not password or len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.')
            return render_template('register.html')

        if not re.match(phone_regex, phone):
            flash('El número de teléfono debe tener exactamente 10 dígitos.')
            return render_template('register.html')

        try:
            birthdate_parsed = datetime.strptime(birthdate, '%Y-%m-%d')
            if birthdate_parsed >= datetime.now():
                flash('La fecha de nacimiento debe ser anterior a hoy.')
                return render_template('register.html')
        except ValueError:
            flash('Formato de fecha inválido. Usa el formato YYYY-MM-DD.')
            return render_template('register.html')

        # Insertar datos en la base de datos
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cur = mysql.connection.cursor()
        try:
            cur.execute("""
                INSERT INTO users (email, username, password, full_name, phone, address, birthdate, role) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (email, username, hashed_password, full_name, phone, address, birthdate, 'user'))  # Asignar rol
            mysql.connection.commit()  # Confirmar cambios
        except Exception as e:
            flash('Ocurrió un error al registrar el usuario.')
            print(e)  # Mostrar error en consola
        finally:
            cur.close()

        flash('Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Por favor, ingresa tu correo y contraseña.')
            return render_template('login.html')

        cur = mysql.connection.cursor()
        try:
            # Buscar el usuario por el correo electrónico
            cur.execute("SELECT id, password, role FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
        finally:
            cur.close()

        # Verificar si el usuario existe y si la contraseña es correcta
        if user and bcrypt.check_password_hash(user[1], password):
            # Si el usuario y la contraseña son correctos, iniciar sesión
            session['user_id'] = user[0]
            session['role'] = user[2]
            return redirect(url_for('dashboard'))  # Redirigir al dashboard

        # Si no coincide, mostrar el mensaje de error
        flash('Correo o contraseña incorrectos.')
        return render_template('login.html')

    # Si la solicitud es GET, mostrar la página de login
    return render_template('login.html')


# Dashboard dependiendo del rol
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    role = session.get('role')

    # Lógica basada en el rol
    if role == 'admin':
        return render_template('admin_dashboard.html')
    elif role == 'supervisor':
        return render_template('supervisor_dashboard.html')  # Nuevo dashboard para supervisor
    else:
        return render_template('user_dashboard.html')  # Usuario regular

# Ruta para agregar contacto (solo para usuarios)
@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        address = request.form['address']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (user_id, first_name, last_name, phone, address) VALUES (%s, %s, %s, %s, %s)",
                    (session['user_id'], first_name, last_name, phone, address))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('dashboard'))
    
    return render_template('add_contact.html')

# Ruta para ver contactos (solo para usuarios)
@app.route('/view_contacts')
def view_contacts():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts WHERE user_id = %s", [session['user_id']])
    contacts = cur.fetchall()
    cur.close()

    return render_template('view_contacts.html', contacts=contacts)

# Ruta para buscar contactos (solo para usuarios)
@app.route('/search_contacts', methods=['GET', 'POST'])
def search_contacts():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    contacts = []
    if request.method == 'POST':
        search_query = request.form['search_query']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM contacts WHERE user_id = %s AND (first_name LIKE %s OR last_name LIKE %s OR phone LIKE %s)",
                    (session['user_id'], f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
        contacts = cur.fetchall()
        cur.close()

    return render_template('search_contacts.html', contacts=contacts)

# Ruta para gestionar usuarios (solo para admins)
@app.route('/manage_users')
def manage_users():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()

    return render_template('manage_users.html', users=users)

# Ruta para editar un usuario (solo para admin)
# Lista de roles válidos
VALID_ROLES = ['user', 'admin', 'supervisor']

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    # Verificar si el usuario es un administrador
    if 'user_id' not in session or session['role'] != 'admin':
        flash('Acceso no autorizado.')
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    # Obtener información completa del usuario a editar
    cur.execute("SELECT id, email, username, role FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()

    if not user:
        flash('Usuario no encontrado.')
        return redirect(url_for('manage_users'))

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        role = request.form['role']  # Obtener el rol del formulario
        password = request.form.get('password')

        # Validar que los campos esenciales no estén vacíos
        if not email or not username or not role:
            flash('Correo, nombre de usuario y rol son obligatorios.')
            return render_template('edit_user.html', user=user)

        # Validar que el rol sea uno válido
        if role not in VALID_ROLES:
            flash('Rol inválido.')
            return render_template('edit_user.html', user=user)

        # Actualizar los datos del usuario
        if password:  # Si se proporciona una nueva contraseña
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cur.execute(
                """
                UPDATE users
                SET email = %s, username = %s, role = %s, password = %s
                WHERE id = %s
                """,
                (email, username, role, hashed_password, user_id),
            )
        else:  # Si no se proporciona una nueva contraseña
            cur.execute(
                """
                UPDATE users
                SET email = %s, username = %s, role = %s
                WHERE id = %s
                """,
                (email, username, role, user_id),
            )

        mysql.connection.commit()
        cur.close()

        flash('Usuario actualizado con éxito.')
        return redirect(url_for('manage_users'))

    return render_template('edit_user.html', user=user)



# Ruta para eliminar un usuario (solo para admin)
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()

    flash('Usuario eliminado con éxito.')
    return redirect(url_for('manage_users'))

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/view_users')
def view_users():
    if 'user_id' not in session or session['role'] not in ['admin', 'supervisor']:
        flash('Acceso no autorizado.')
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, email, username, role FROM users")
    users = cur.fetchall()
    cur.close()

    return render_template('view_users.html', users=users)


@app.route('/view_all_contacts')
def view_all_contacts():
    if 'user_id' not in session or session['role'] not in ['admin', 'supervisor']:
        flash('Acceso no autorizado.')
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT contacts.id, contacts.first_name, contacts.last_name, contacts.phone, contacts.address, users.username FROM contacts JOIN users ON contacts.user_id = users.id")
    contacts = cur.fetchall()
    cur.close()

    return render_template('view_all_contacts.html', contacts=contacts)

@app.route('/supervisor/dashboard')
def supervisor_dashboard():
    return render_template('supervisor_dashboard.html')


@app.route('/admin/dashboard', endpoint='admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')




if __name__ == '__main__':
    app.run(debug=True, port=8001, ssl_context=('certificados/cert.pem', 'certificados/key.pem'))
