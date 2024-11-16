import os
import json
import random 
from datetime import datetime, timedelta
import crud
from model import connect_to_db, db, User, Task, Notification
from server import app

from faker import Faker
fake = Faker()

# Drop the existing database (if it exists) and create a new one
os.system("dropdb tasks")
os.system("createdb tasks")

# Connect to the db and set up the application context
app.app_context().push()
connect_to_db(app)
db.create_all()  # Create all the data tables from the model

def reset_database():
    """Drop all tables and recreate them."""
    db.drop_all()
    db.create_all()

# seed the data 
def seed_users(num_users=10):
    """Populate the database with fake users"""
    users = []
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        users.append(user)
    db.session.commit()
    return users 

def seed_tasks(users, num_tasks_per_user=5):
    """Populate tasks for each user"""
    for user in users:
        for _ in range(num_tasks_per_user):
            title = fake.sentence(nb_words=5)
            description = fake.paragraph()
            due_date = datetime.now() + timedelta(days=random.randint(1, 30))
            priority = random.choice(["High", "Medium", "Low"])
            task = Task(user_id=user.id, title=title, description=description, due_date=due_date, priority=priority)
            db.session.add(task)
    db.session.commit()

def seed_notification():
    """Create notification for tasks, one day before the due date"""
    tasks = Task.query.all()
    for task in tasks:
        reminder_time = task.due_date - timedelta(days=1)
        notification = Notification(task_id=task.id, user_id=task.user_id, reminder_time=reminder_time)
        db.session.add(notification)
    db.session.commit()

# run the seed function 

def seed_database():
    """Run all seeding functions"""
    reset_database()
    users = seed_users()
    seed_tasks(users)
    seed_notification()
    print("Database seeded with test data")

if __name__=="__main__":
    with app.app_context():
        seed_database()