"""Server for task scheduler app."""

from flask import Flask
from flask import (Flask, request, jsonify)
from crud import create_user, create_task, get_user_by_username, get_tasks_by_user
from model import db, Task, User 
from twilio.rest import Client
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv(dotenv_path="backend/.env")


# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all() 

from twilio.rest import Client

# Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)



@app.route('/register', methods=['POST'])
def register():
    """Register a new user""" 
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    phone_number = data.get('phone_number')

    if not username or not email or not password or not phone_number:
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

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task's details."""
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')
    priority = data.get('priority')
    status = data.get('status')

    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    if title: task.title = title
    if description: task.description = description
    if due_date: task.due_date = due_date
    if priority: task.priority = priority
    if status: task.status = status

    db.session.commit()
    return jsonify({'message': 'Task updated successfully'}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task by ID."""
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

@app.route('/notify/<int:task_id>', methods=['POST'])
def send_notification(task_id):
    """Send a notification for a task."""
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    user = User.query.get(task.user_id)
    if not user or not user.phone_number:
        return jsonify({'error': 'User not found or no phone number provided'}), 404

    # Compose the message
    message_body = f"Reminder: Your task '{task.title}' is due on {task.due_date}."

    # Send SMS
    try:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=user.phone_number  # Use user's phone number
        )
        return jsonify({'message': 'Notification sent successfully', 'sid': message.sid}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Function to check for due tasks and send notifications
def check_due_tasks():
    now = datetime.utcnow()
    tasks = Task.query.filter(Task.due_date <= now + timedelta(hours=1), Task.status == 'Pending').all()

    for task in tasks:
        user = User.query.get(task.user_id)
        if user:
            # Send SMS
            message_body = f"Reminder: Your task '{task.title}' is due soon!"
            client.messages.create(
                body=message_body,
                from_=TWILIO_PHONE_NUMBER,
                to='recipient_phone_number'  # Replace with user's phone
            )
            print(f"Notification sent for task {task.title}")

# Start the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_due_tasks, trigger="interval", minutes=30)
scheduler.start()



if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True, port=6060)