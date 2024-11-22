# Task Scheduler App

**Task Scheduler App** is a web application helps users create and schedule tasks with integrated text notification reminders using Twilio's API. Built with **Flask** for the backend and **React** for the frontend, the app streamlines task management for individuals and teams.

---

## Features

- **User Authentication**: Register and log in to manage your personalized tasks.
- **Task Management**: Create, edit, delete, and view tasks.
- **Schedule Tasks**: Set due dates and reminders for tasks.
- **Twilio Notifications**: Receive task reminders via SMS.
- **Responsive Design**: User-friendly UI 

---

## Technologies Used

### Backend
- **Flask**: Python-based web framework.
- **SQLAlchemy**: ORM for database interactions.
- **Twilio API**: For sending text notifications.
- **SQLite**: Lightweight database for development (or PostgreSQL for production).

### Frontend
- **React**: JavaScript library for building UI.
- **Bootstrap**: CSS framework for responsive design.
- **Vite**: Modern build tool for faster development.

---

## Installation and Setup

### Prerequisites
1. Python 3.8+
2. Node.js 14+
3. Twilio account with API credentials.

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/task-scheduler-app.git
   cd task-scheduler-app
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
5. Run the Flask development server:
   ```bash
   flask run
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd client
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

---

## Usage

1. **Sign Up**: Create an account to start managing your tasks.
2. **Create Tasks**: Add tasks with due dates and reminder times.
3. **Edit or Delete**: Modify or remove tasks as needed.
4. **Receive Reminders**: Get SMS notifications at the scheduled reminder time.

---

## Future Enhancements

- **Recurring Tasks**: Allow users to set tasks to repeat daily, weekly, or monthly.
- **Team Collaboration**: Share tasks with team members and assign roles.
- **Analytics**: Provide task completion insights and performance tracking.

---

## Contributing

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

Happy task scheduling! 😊

