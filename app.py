from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from uuid import uuid4
import random

app = Flask(__name__)
app.secret_key = 'your-secret-key'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database setup
def init_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            full_name TEXT,
            dob TEXT,
            profile_pic TEXT,
            coins INTEGER DEFAULT 0,
            last_checkin TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS progress (
            user_id INTEGER,
            subject TEXT,
            content_type TEXT,
            completed INTEGER DEFAULT 0,
            total INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            question TEXT,
            answer TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            category TEXT,
            item TEXT,
            description TEXT,
            image TEXT
        )''')
        # Sample questions
        sample_questions = [
            ('Telugu', 'What is "అ" in Varnamala?', 'First letter'),
            ('English', 'What is "A" in alphabet?', 'First letter'),
            ('Hindi', 'What is "अ" in Varnamala?', 'First letter'),
            ('Maths', 'What is 1 + 1?', '2')
        ]
        c.executemany('INSERT OR IGNORE INTO questions (subject, question, answer) VALUES (?, ?, ?)', sample_questions)
        # Sample content
        sample_content = [
            ('Telugu', 'Varnamala', 'అ', 'First vowel', ''),
            ('Telugu', 'Varnamala', 'ఆ', 'Second vowel', ''),
            ('Telugu', 'Guninthalu', 'క', 'Ka', ''),
            ('Telugu', 'Guninthalu', 'కా', 'Kaa', ''),
            ('Telugu', 'Geyalu', 'Chitti Chilakamma', 'Nursery rhyme', ''),
            ('Telugu', 'Photolu', 'అ', 'అమ్మ', 'amma.jpg'),
            ('English', 'Alphabets', 'A', 'First letter', ''),
            ('English', 'Alphabets', 'B', 'Second letter', ''),
            ('English', 'Rhymes', 'Twinkle Twinkle', 'Nursery rhyme', ''),
            ('English', 'Photos', 'A', 'Apple', 'apple.jpg'),
            ('Hindi', 'Varnamala', 'अ', 'First vowel', ''),
            ('Hindi', 'Varnamala', 'आ', 'Second vowel', ''),
            ('Hindi', 'Guninthalu', 'क', 'Ka', ''),
            ('Hindi', 'Guninthalu', 'का', 'Kaa', ''),
            ('Hindi', 'Rhymes', 'Machhli Jal Ki', 'Nursery rhyme', ''),
            ('Hindi', 'Photos', 'अ', 'Apple', 'apple.jpg'),
            ('Maths', 'Numbers', '1', 'One', ''),
            ('Maths', 'Numbers', '2', 'Two', ''),
            ('Maths', 'Tables', '2 x 1 = 2', 'Table of 2', ''),
            ('Maths', 'Roman Numerals', 'I', 'One', ''),
            ('Maths', 'Pics', '1', 'One', 'one.jpg')
        ]
        c.executemany('INSERT OR IGNORE INTO content (subject, category, item, description, image) VALUES (?, ?, ?, ?, ?)', sample_content)
        conn.commit()

if not os.path.exists('database.db'):
    init_db()

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        try:
            with sqlite3.connect('database.db') as conn:
                c = conn.cursor()
                c.execute('INSERT INTO users (username, password, coins) VALUES (?, ?, ?)', (username, password, 0))
                conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = c.fetchone()
            if user and check_password_hash(user[2], password):
                session['user_id'] = user[0]
                # Check-in
                last_checkin = user[7] or '2000-01-01'
                today = datetime.now().date()
                if last_checkin != str(today):
                    c.execute('UPDATE users SET coins = coins + 1, last_checkin = ? WHERE id = ?', (today, user[0]))
                    conn.commit()
                return redirect(url_for('dashboard'))
            flash('Invalid credentials!')
    return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = c.fetchone()
            if user:
                # Simulate sending reset link
                print(f"Password reset link for {username}: /reset/{uuid4()}")
                flash('Password reset link sent! (Check console for demo)')
            else:
                flash('Username not found!')
    return render_template('forgot_password.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT username, coins FROM users WHERE id = ?', (session['user_id'],))
        user = c.fetchone()
    return render_template('dashboard.html', username=user[0], coins=user[1])

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT username, full_name, dob, profile_pic FROM users WHERE id = ?', (session['user_id'],))
        user = c.fetchone()
        if request.method == 'POST':
            full_name = request.form.get('full_name')
            dob = request.form.get('dob')
            password = request.form.get('password')
            profile_pic = request.files.get('profile_pic')
            if profile_pic:
                filename = f"{session['user_id']}_{profile_pic.filename}"
                profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                filename = user[3]
            if password:
                password = generate_password_hash(password)
            else:
                c.execute('SELECT password FROM users WHERE id = ?', (session['user_id'],))
                password = c.fetchone()[0]
            c.execute('UPDATE users SET full_name = ?, dob = ?, profile_pic = ?, password = ? WHERE id = ?',
                      (full_name, dob, filename, password, session['user_id']))
            conn.commit()
            flash('Profile updated!')
            return redirect(url_for('profile'))
    return render_template('profile.html', user=user)

@app.route('/subject/<subject>')
def subject(subject):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT category, item, description, image FROM content WHERE subject = ?', (subject,))
        content_raw = c.fetchall()
        content = {}
        for category, item, desc, img in content_raw:
            if category not in content:
                content[category] = []
            content[category].append({'item': item, 'description': desc, 'image': img})
        # Update progress
        c.execute('SELECT COUNT(*) FROM content WHERE subject = ?', (subject,))
        total = c.fetchone()[0]
        c.execute('INSERT OR IGNORE INTO progress (user_id, subject, content_type, completed, total) VALUES (?, ?, ?, ?, ?)',
                  (session['user_id'], subject, 'subject', 1, total))
        conn.commit()
    return render_template('subject.html', subject=subject, content=content)

@app.route('/practice/<subject>', methods=['GET', 'POST'])
def practice(subject):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT id, question, answer FROM questions WHERE subject = ?', (subject,))
        questions = c.fetchall()
        if not questions:
            return render_template('practice.html', subject=subject, question='No questions available', answer='')
        question = random.choice(questions)
        if request.method == 'POST':
            user_answer = request.form.get('answer')
            correct = user_answer.strip().lower() == question[2].strip().lower()
            # Update practice progress
            c.execute('SELECT completed, total FROM progress WHERE user_id = ? AND subject = ? AND content_type = ?',
                      (session['user_id'], subject, 'practice'))
            progress = c.fetchone()
            if progress:
                completed, total = progress
                if correct:
                    completed += 1
                total += 1
                c.execute('UPDATE progress SET completed = ?, total = ? WHERE user_id = ? AND subject = ? AND content_type = ?',
                          (completed, total, session['user_id'], subject, 'practice'))
            else:
                c.execute('INSERT INTO progress (user_id, subject, content_type, completed, total) VALUES (?, ?, ?, ?, ?)',
                          (session['user_id'], subject, 'practice', 1 if correct else 0, 1))
            conn.commit()
            return jsonify({'correct': correct, 'answer': question[2]})
    return render_template('practice.html', subject=subject, question=question[1], question_id=question[0])

@app.route('/tracking')
def tracking():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT subject, content_type, completed, total FROM progress WHERE user_id = ?', (session['user_id'],))
        progress = c.fetchall()
    return render_template('tracking.html', progress=progress)

@app.route('/checkin')
def checkin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT coins, last_checkin FROM users WHERE id = ?', (session['user_id'],))
        user = c.fetchone()
        return render_template('checkin.html', coins=user[0], last_checkin=user[1] or 'Never')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)