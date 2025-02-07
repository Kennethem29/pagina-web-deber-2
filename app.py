from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'advpjs'  # Necesario para usar mensajes flash

# Conexión a MongoDB
client = MongoClient("mongodb+srv://kennethe632:<Kenneth2006>@cluster0.gv0fv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Cambia la URL si usas MongoDB Atlas
db = client.bd1 # Base de datos
collection = db.usuarios  # Colección

# Ruta para la página de contacto
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Ruta para manejar el formulario de contacto
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        email = request.form['email']
        mensaje = request.form['mensaje']

        # Validar que los campos no estén vacíos
        if not nombre or not email or not mensaje:
            flash("Todos los campos son obligatorios.", "error")
            return redirect(url_for('contact'))

        # Crear un documento para insertar en MongoDB
        documento = {
            'nombre': nombre,
            'email': email,
            'mensaje': mensaje,
            'fecha': datetime.utcnow()  # Fecha y hora actual en UTC
        }

        # Insertar el documento en la colección
        try:
            collection.insert_one(documento)
            flash("Gracias por contactarnos, tu mensaje ha sido guardado.", "success")
        except Exception as e:
            flash(f"Hubo un error al guardar tu mensaje: {e}", "error")

        return redirect(url_for('contact'))

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)