from flask_bcrypt import Bcrypt

# Inicializar Flask-Bcrypt
bcrypt = Bcrypt()

# La contraseña que deseas usar para el admin
password = 'admin123'

# Generar el hash de la contraseña
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

# Imprimir el hash generado
print(f"El hash de la contraseña es: {hashed_password}")
