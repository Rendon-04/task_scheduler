"""CRUD OPERATONS"""

from model import db, User, Task, Notification, connect_to_db
from datetime import datetime, timedelta
import random
# import faker from Faker

# fake = Faker()

# User related functions
def create_user(username, email, password):
    """Create and return a new user"""
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user 

def get_user_by_id(user_id):
    """Get a user by their ID"""
    return User.query.get(user_id)

def get_user_by_username(username):
    """Get user by their username"""
    return User.query.filter_by(username=username).first()

# Task related functions 
def create_task(user_id, title, description, due_date, priority="Medium"):
    """Create and return a new task"""
    task = Task(user_id=user_id, title=title, description=description, due_date=due_date, priority=priority)
    db.session.add(task)
    db.session.commit()
    return task 

def get_task_by_id(task_id):
    """Get a task by its ID"""
    return Task.query.get(task_id)

def get_tasks_by_user(user_id):
    """Get all tasks for a specific user"""
    return Task.query.filter_by(user_id=user_id).all()

def update_task_status(task_id, status):
    """Update the status of a task""" 
    task = get_task_by_id(task_id)
    if task:
        task.status = status
        db.session.commit()
    return task 

# Notification related functions 
def create_notification(task_id, user_id, remindet_time):
    """Create and return a new notification"""
    notification = Notification(task_id=task_id, user_id=user_id, remindet_time=remindet_time)
    db.session.add(notification)
    db.session.commit()
    return notification

def get_notification_by_user(user_id):
    """Get all the notifications for a specific user"""
    return Notification.query.filter_by(user_id=user_id).all()

def mark_notification_as_sent(notification_id):
    """Mark a notification as sent"""
    notification = Notification.query.get(notification_id)
    if notification:
        notification.sent = True 
        db.session.commit()
    return notification

# Database related functions 
def populate_database_with_tasks(num_users=5, num_tasks_per_user=10):
    """Populate database with fake users and tasks."""
    # Generate random users
    users = []
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        user = create_user(username, email, password)
        users.append(user)
    
    # Generate random tasks for each user
    for user in users:
        for _ in range(num_tasks_per_user):
            title = fake.sentence(nb_words=5)
            description = fake.paragraph()
            due_date = fake.future_datetime()
            priority = random.choice(["High", "Medium", "Low"])
            create_task(user.id, title, description, due_date, priority)


def generate_random_notifications():
    """Generate random notifications based on existing tasks."""
    tasks = Task.query.all()
    for task in tasks:
        # Create a notification for each task, scheduled one day before the task due date
        reminder_time = task.due_date - timedelta(days=1)
        create_notification(task.id, task.user_id, reminder_time)



if __name__ == "__main__":
    from server import app

    connect_to_db(app)
