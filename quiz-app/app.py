from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production
DATABASE = 'quiz.db'

# --- DB Functions ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option1 TEXT NOT NULL,
            option2 TEXT NOT NULL,
            option3 TEXT NOT NULL,
            option4 TEXT NOT NULL,
            answer INTEGER NOT NULL
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            score INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
        db.commit()
        # Insert sample questions if not present
        cur = db.execute('SELECT COUNT(*) FROM questions')
        if cur.fetchone()[0] == 0:
            db.executemany('''INSERT INTO questions (question, option1, option2, option3, option4, answer) VALUES (?, ?, ?, ?, ?, ?)''', [
                ("What is the capital of France?", "Berlin", "London", "Paris", "Madrid", 3),
                ("Which planet is known as the Red Planet?", "Earth", "Mars", "Jupiter", "Saturn", 2),
                ("Who wrote 'To Kill a Mockingbird'?", "Harper Lee", "Mark Twain", "J.K. Rowling", "Jane Austen", 1)
            ])
            db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        try:
            db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            error = 'Username already exists.'
    return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = query_db('SELECT * FROM users WHERE username = ? AND password = ?', [username, password], one=True)
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('quiz'))
        else:
            error = 'Invalid credentials.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    questions = query_db('SELECT * FROM questions')
    if request.method == 'POST':
        score = 0
        for q in questions:
            qid = str(q[0])
            correct = q[6]
            ans = request.form.get(f'q{qid}')
            if ans and int(ans) == correct:
                score += 1
        db.execute('INSERT INTO scores (user_id, score) VALUES (?, ?)', (session['user_id'], score))
        db.commit()
        return redirect(url_for('leaderboard'))
    return render_template('quiz.html', questions=questions)

@app.route('/leaderboard')
def leaderboard():
    db = get_db()
    rows = query_db('''SELECT users.username, scores.score, scores.timestamp FROM scores JOIN users ON scores.user_id = users.id ORDER BY score DESC, timestamp ASC LIMIT 10''')
    return render_template('leaderboard.html', rows=rows)

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    else:
        # Ensure tables exist and sample questions are present
        init_db()
    app.run(debug=True)
