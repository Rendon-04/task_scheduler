"""Server for task scheduler app."""

from flask import Flask
from flask import (Flask, request, flash, session, jsonify,
                   redirect)
from model import connect_to_db, db
from crud import create_user, create_task, get_user_by_username, get_tasks_by_user
import os

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()


@app.route('/register', methods=['POST'])
def register():
    """Register a new user""" 
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error' : 'Alle fields are required'}), 400

    existing_user = get_user_by_username(username)
    if existing_user:
        return jsonify({'error' : 'User already exists'}), 409
    
    user = create_user(username, email, password)
    return jsonify({'message' : 'User registered successfully', 'user_id': user.id}), 201 

@app.route('/tasks', methods=['POST'])
def add_tasks():
    """Create a new task for a user"""
    data = request.get_json()
    user_id = data.get('user_id')
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')
    priority = data.get('priority', 'Medium')

    if not user_id or not title or not due_date:
        return jsonify({'error': 'User ID, title, and due date are required'}), 400
    
    task = create_task(user_id, title, description,due_date, priority)
    return jsonify({'message': 'Task created successfully', 'task_id': task.id}), 201 

@app.route('/task/<int:user_id>', methods=['GET'])
def get_tasks(user_id):
    """Retrieve all tasks for a user"""
    tasks = get_tasks_by_user(user_id)
    task_list = [{'id': task.id, 'title': task.title, 'due_date': task.due_date, 'priority': task.priority} for task in tasks]
    return jsonify(task_list), 200






if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True, port=6060)