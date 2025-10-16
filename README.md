# Quiz Web App

#### Description:

This project is a full-stack Quiz Web Application built using **Flask** for the backend, **SQLite** for database management, and **HTML, CSS, and JavaScript** for the frontend. The purpose of this project is to create an interactive and functional web application that allows users to register, log in, take quizzes, and view scores on a leaderboard. This project demonstrates understanding of web development fundamentals, database integration, session management, and dynamic content rendering.

The application is designed with three main types of users: guests, registered users, and the system administrator (for question insertion in the database). Guests can view the homepage but must register or log in to access the quiz functionality. Registered users can take quizzes, have their scores recorded, and view the leaderboard. This project includes functionality for multiple-choice quizzes, with scores automatically calculated and stored in the database.

---

### File Structure and Description

```
quiz-app/
│── app.py
│── quiz.db
│── templates/
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── quiz.html
│   └── leaderboard.html
│── static/
    ├── style.css
    └── script.js
```

**1. app.py**

Main Python file that runs the Flask application. It contains all the routes, database initialization, and logic for registering users, logging in, taking quizzes, calculating scores, and displaying the leaderboard. Uses Flask’s session management for user authentication. The `init_db()` function ensures the database and all tables are created automatically if they do not exist, and it inserts sample questions.

**2. quiz.db**

SQLite database file storing user information, quiz questions, and scores. Includes three tables: `users`, `questions`, and `scores`.

**3. Templates**

* `base.html`: Base template with header, footer, and navigation. All other templates extend it.
* `index.html`: Homepage introducing the app.
* `register.html`: User registration form with duplicate username handling.
* `login.html`: Login form with credential verification.
* `quiz.html`: Displays quiz questions; calculates score on submission.
* `leaderboard.html`: Shows top 10 scores.

**4. Static Files**

* `style.css`: Styles all pages with a clean and modern design.
* `script.js`: Adds quiz interactivity including a countdown timer and auto-submit.

---

### Functionality and Features

1. **User Registration and Login**: Users can register and log in using sessions. Passwords stored in plaintext for simplicity.
2. **Quiz Interface**: Multiple-choice quizzes dynamically generated from the database. Scores calculated on form submission.
3. **Leaderboard**: Displays top 10 user scores, sorted by score and timestamp.
4. **Database Management**: SQLite handles data persistence; tables are created automatically, and sample questions are seeded.
5. **Front-End Design**: Responsive HTML/CSS; JavaScript timer enhances user experience.

---

### Design Choices

* **Flask**: Lightweight and simple backend framework.
* **SQLite**: Easy to set up and perfect for small-scale applications.
* **Vanilla CSS and JS**: Avoids dependency issues, keeps project simple.
* **Session-Based Authentication**: Simple yet effective for login management.

---

### Future Improvements

* Add admin panel to add/edit/delete questions.
* Implement password hashing for security.
* Introduce quiz categories and difficulty levels.
* Store and visualize user statistics over time.

---

This project demonstrates full-stack web development skills, combining backend logic, database integration, and frontend design into a functional, interactive web application.
