import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, session
from app import app, mysql

# -*- coding: utf-8 -*-


# Configuración de cliente para las pruebas
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test para comprobar la cobertura de los endpoints
def test_register(client):
    # Test de registro con datos válidos
    response = client.post('/register', data={
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'password123',
        'full_name': 'Test User',
        'phone': '1234567890',
        'address': '123 Main St',
        'birthdate': '1990-01-01'
    })
    assert response.status_code == 302  # Debe redirigir al login

def test_login(client):
    # Crear un usuario primero para las pruebas
    client.post('/register', data={
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'password123',
        'full_name': 'Test User',
        'phone': '1234567890',
        'address': '123 Main St',
        'birthdate': '1990-01-01'
    })

    response = client.post('/login', data={'email': 'test@example.com', 'password': 'password123'})
    assert response.status_code == 302  # Debe redirigir al dashboard

def test_dashboard_requires_login(client):
    # Test para asegurar que no se pueda acceder al dashboard sin iniciar sesión
    response = client.get('/dashboard')
    assert response.status_code == 302  # Redirige al login si no hay sesión

# 2. Verificar Overflow, tipos de datos e Inyección SQL

def test_sql_injection(client):
    # Intento de inyección SQL en el login
    response = client.post('/login', data={'email': "test@example.com' OR 1=1 --", 'password': 'password123'})
    assert b'Correo o contrasena incorrectos.' in response.data

def test_overflow_username(client):
    # Intento de registrar un usuario con un nombre de usuario demasiado largo
    response = client.post('/register', data={
        'email': 'test@example.com',
        'username': 'x' * 21,  # Más de 20 caracteres
        'password': 'password123',
        'full_name': 'Test User',
        'phone': '1234567890',
        'address': '123 Main St',
        'birthdate': '1990-01-01'
    })
    assert b'El nombre de usuario debe tener entre 3 y 20 caracteres.' in response.data

def test_invalid_date_format(client):
    # Intento de registro con un formato de fecha incorrecto
    response = client.post('/register', data={
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'password123',
        'full_name': 'Test User',
        'phone': '1234567890',
        'address': '123 Main St',
        'birthdate': '1990-01-32'  # Fecha inválida
    })
    assert b'Formato de fecha invalido.' in response.data

def test_invalid_phone(client):
    # Intento de registro con un número de teléfono inválido
    response = client.post('/register', data={
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'password123',
        'full_name': 'Test User',
        'phone': '1234567',  # Teléfono con menos de 10 dígitos
        'address': '123 Main St',
        'birthdate': '1990-01-01'
    })
    assert b'El numero de telefono debe tener exactamente 10 digitos.' in response.data

# 3. Pruebas de Integración para el Alta de Usuarios

def test_user_registration_integration(client):
    # Crear un usuario válido
    response = client.post('/register', data={
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'password123',
        'full_name': 'Test User',
        'phone': '1234567890',
        'address': '123 Main St',
        'birthdate': '1990-01-01'
    })
    assert response.status_code == 302  # Redirige al login

    # Verificar que el usuario haya sido insertado en la base de datos
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", ('test@example.com',))
    user = cur.fetchone()
    cur.close()

    assert user is not None  # El usuario debe existir en la base de datos
    assert user[1] == 'test@example.com'  # Verificar email
    assert user[2] == 'testuser'  # Verificar username

def test_user_registration_with_invalid_data(client):
    # Test con datos inválidos
    response = client.post('/register', data={
        'email': 'invalid_email',  # Correo inválido
        'username': 'us',  # Nombre de usuario demasiado corto
        'password': '123',  # Contraseña demasiado corta
        'full_name': 'Test User',
        'phone': '123456',  # Teléfono inválido
        'address': '123 Main St',
        'birthdate': '1990-01-01'
    })
    assert b'Correo invalido.' in response.data
    assert b'El nombre de usuario debe tener entre 3 y 20 caracteres.' in response.data
    assert b'La contrasena debe tener al menos 8 caracteres.' in response.data
    assert b'El numero de telefono debe tener exactamente 10 digitos.' in response.data

# Test de logout
def test_logout(client):
    # Crear usuario para probar
    client.post('/register', data={
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'password123',
        'full_name': 'Test User',
        'phone': '1234567890',
        'address': '123 Main St',
        'birthdate': '1990-01-01'
    })

    client.post('/login', data={'email': 'test@example.com', 'password': 'password123'})
    response = client.get('/logout')
    assert response.status_code == 302  # Redirige al inicio
    assert 'user_id' not in session  # Verifica que la sesión haya sido cerrada
