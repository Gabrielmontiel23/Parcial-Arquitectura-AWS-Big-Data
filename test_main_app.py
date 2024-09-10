# main_app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/add-user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(
        nombres=data['nombres'],
        apellidos=data['apellidos'],
        fecha_nacimiento=data['fecha_nacimiento'],
        password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuario añadido con éxito'}), 200

@app.route('/get-users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'nombres': user.nombres, 'apellidos': user.apellidos, 'fecha_nacimiento': user.fecha_nacimiento} for user in users]
    return jsonify({'status': 'success', 'data': user_list}), 200

if __name__ == '__main__':
    app.run(debug=True)
