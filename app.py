from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename
import random
import logging
from jinja2.exceptions import TemplateNotFound
import glob

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Database initialization
def init_db():
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                     (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS profiles 
                     (user_id INTEGER, full_name TEXT, dob TEXT, profile_pic TEXT, 
                      FOREIGN KEY(user_id) REFERENCES users(id))''')
        c.execute('''CREATE TABLE IF NOT EXISTS progress 
                     (user_id INTEGER, subject TEXT, percentage REAL, 
                      FOREIGN KEY(user_id) REFERENCES users(id))''')
        c.execute('''CREATE TABLE IF NOT EXISTS practice 
                     (user_id INTEGER, subject TEXT, correct INTEGER, total INTEGER, 
                      FOREIGN KEY(user_id) REFERENCES users(id))''')
        c.execute('''CREATE TABLE IF NOT EXISTS checkin 
                     (user_id INTEGER, last_checkin TEXT, coins INTEGER, 
                      FOREIGN KEY(user_id) REFERENCES users(id))''')
        c.execute('''CREATE TABLE IF NOT EXISTS contact_messages 
                     (id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, message TEXT, timestamp TEXT, 
                      FOREIGN KEY(user_id) REFERENCES users(id))''')
        c.execute('''CREATE TABLE IF NOT EXISTS checkin_history 
                     (id INTEGER PRIMARY KEY, user_id INTEGER, checkin_date TEXT, 
                      FOREIGN KEY(user_id) REFERENCES users(id))''')
        conn.commit()
        logging.info("Database initialized successfully.")
    except sqlite3.OperationalError as e:
        logging.error(f"OperationalError during database initialization: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error during database initialization: {e}")
        raise
    finally:
        conn.close()

try:
    init_db()
except Exception as e:
    logging.error(f"Failed to initialize database: {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                     (username, password))
            user_id = c.lastrowid
            c.execute("INSERT INTO profiles (user_id, profile_pic) VALUES (?, ?)", 
                     (user_id, 'default_profile.png'))
            c.execute("INSERT INTO checkin (user_id, last_checkin, coins) VALUES (?, ?, ?)", 
                     (user_id, '2000-01-01', 0))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'error')
        except sqlite3.OperationalError as e:
            logging.error(f"OperationalError during registration: {e}")
            flash('Database error. Please try again.', 'error')
        finally:
            conn.close()
    try:
        return render_template('register.html')
    except TemplateNotFound as e:
        logging.error(f"TemplateNotFound in register: {e}")
        flash('Register template not found. Please contact support.', 'error')
        return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = c.fetchone()
            if user:
                session['user_id'] = user[0]
                c.execute("SELECT last_checkin, coins FROM checkin WHERE user_id = ?", (user[0],))
                checkin = c.fetchone()
                last_checkin = datetime.strptime(checkin[0], '%Y-%m-%d')
                today = datetime.now().date()
                if last_checkin.date() < today:
                    c.execute("UPDATE checkin SET last_checkin = ?, coins = coins + 1 WHERE user_id = ?", 
                             (today.strftime('%Y-%m-%d'), user[0]))
                    c.execute("INSERT INTO checkin_history (user_id, checkin_date) VALUES (?, ?)", 
                             (user[0], today.strftime('%Y-%m-%d')))
                    conn.commit()
                    flash('Daily check-in: +1 coin!', 'success')
                return redirect(url_for('dashboard'))
            flash('Invalid credentials.', 'error')
        except sqlite3.OperationalError as e:
            logging.error(f"OperationalError during login: {e}")
            flash('Database error. Please try again.', 'error')
        finally:
            conn.close()
    try:
        return render_template('login.html')
    except TemplateNotFound as e:
        logging.error(f"TemplateNotFound in login: {e}")
        flash('Login template not found. Please contact support.', 'error')
        return redirect(url_for('index'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = c.fetchone()
            if user:
                flash('Password reset instructions sent.', 'success')
            else:
                flash('Username not found.', 'error')
        except sqlite3.OperationalError as e:
            logging.error(f"OperationalError during forgot password: {e}")
            flash('Database error. Please try again.', 'error')
        finally:
            conn.close()
        return redirect(url_for('login'))
    try:
        return render_template('forgot_password.html')
    except TemplateNotFound as e:
        logging.error(f"TemplateNotFound in forgot_password: {e}")
        flash('Forgot password template not found. Please contact support.', 'error')
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute("SELECT coins FROM checkin WHERE user_id = ?", (session['user_id'],))
        coins = c.fetchone()
        if coins is None:
            c.execute("INSERT INTO checkin (user_id, last_checkin, coins) VALUES (?, ?, ?)", 
                     (session['user_id'], '2000-01-01', 0))
            conn.commit()
            coins = (0,)
    except sqlite3.OperationalError as e:
        logging.error(f"OperationalError during dashboard: {e}")
        flash('Database error. Please try again.', 'error')
        coins = (0,)
    finally:
        conn.close()
    try:
        return render_template('dashboard.html', coins=coins[0])
    except TemplateNotFound as e:
        logging.error(f"TemplateNotFound in dashboard: {e}")
        flash('Dashboard template not found. Please contact support.', 'error')
        return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        if request.method == 'POST':
            full_name = request.form.get('full_name')
            dob = request.form.get('dob')
            new_password = request.form.get('new_password')
            if 'profile_pic' in request.files:
                file = request.files['profile_pic']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    c.execute("UPDATE profiles SET profile_pic = ? WHERE user_id = ?", 
                             (filename, session['user_id']))
            if full_name:
                c.execute("UPDATE profiles SET full_name = ? WHERE user_id = ?", 
                         (full_name, session['user_id']))
            if dob:
                c.execute("UPDATE profiles SET dob = ? WHERE user_id = ?", 
                         (dob, session['user_id']))
            if new_password:
                c.execute("UPDATE users SET password = ? WHERE id = ?", 
                         (new_password, session['user_id']))
            conn.commit()
            flash('Profile updated successfully.', 'success')
        c.execute("SELECT full_name, dob, profile_pic FROM profiles WHERE user_id = ?", 
                 (session['user_id'],))
        profile = c.fetchone()
    except sqlite3.OperationalError as e:
        logging.error(f"OperationalError during profile: {e}")
        flash('Database error. Please try again.', 'error')
        profile = (None, None, None)
    finally:
        conn.close()
    try:
        return render_template('profile.html', profile=profile)
    except TemplateNotFound as e:
        logging.error(f"TemplateNotFound in profile: {e}")
        flash('Profile template not found. Please contact support.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        return render_template('settings.html')
    except TemplateNotFound as e:
        logging.error(f"TemplateNotFound in settings: {e}")
        flash('Settings template not found. Please contact support.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            message = request.form.get('message')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute("INSERT INTO contact_messages (user_id, name, message, timestamp) VALUES (?, ?, ?, ?)", 
                     (session['user_id'], name, message, timestamp))
            conn.commit()
            flash('Your message has been sent! We will get back to you soon.', 'success')
            return redirect(url_for('contact_us'))
    except sqlite3.OperationalError as e:
        logging.error(f"OperationalError during contact_us: {e}")
        flash('Database error. Please try again.', 'error')
    finally:
        conn.close()
    try:
        template_path = os.path.join(app.template_folder, 'contact_us.html')
        logging.debug(f"Attempting to render template: {template_path}")
        if not os.path.exists(template_path):
            logging.error(f"Template file does not exist: {template_path}")
        return render_template('contact_us.html')
    except TemplateNotFound as e:
        logging.error(f"TemplateNotFound in contact_us: {e}, expected at {template_path}")
        flash('Contact Us template not found. Please contact support.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/faq')
def faq():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    faqs = [
        {"question": "What is the Kids Learning App?", "answer": "It's a fun app to learn Telugu, English, Hindi, and Maths with games and quizzes!"},
        {"question": "How do I earn coins?", "answer": "Check in daily to earn coins and complete practice questions!"},
        {"question": "Can I change my profile picture?", "answer": "Yes, go to the Profile page and upload a new picture!"},
        {"question": "What subjects can I learn?", "answer": "You can learn Telugu, English, Hindi, and Maths with fun activities!"}
    ]
    try:
        return render_template('faq.html', faqs=faqs)
    except TemplateNotFound as e:
        logging.error(f"TemplateNotFound in faq: {e}")
        flash('FAQ template not found. Please contact support.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/subjects')
def subjects():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        return render_template('subjects.html')
    except TemplateNotFound as e:
        logging.error(f"TemplateNotFound in subjects: {e}")
        flash('Subjects template not found. Please contact support.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/telugu')
def telugu():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        varnamala = ['అ', 'ఆ', 'ఇ', 'ఈ', 'ఉ', 'ఊ']
        guninthalu = ['క', 'కా', 'కి', 'కీ']
        geyalu = [{'title': 'చిట్టి చిలకమ్మ', 'content': 'చిట్టి చిలకమ్మ అమ్మ బడికి వెళ్ళింది...'}]
        photolu = [{'letter': 'అ', 'word': 'అమ్మ', 'image': 'amma.png'}]
        return render_template('telugu.html', varnamala=varnamala, guninthalu=guninthalu, 
                              geyalu=geyalu, photolu=photolu)
    except TemplateNotFound as e:
        logging.error(f"TemplateNotFound in telugu: {e}")
        flash('Telugu template not found. Please contact support.', 'error')
        return redirect(url_for('subjects'))
    except Exception as e:
        logging.error(f"Error in telugu route: {e}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('subjects'))

@app.route('/english')
def english():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        alphabets = ['A', 'B', 'C', 'D']
        rhymes = [{'title': 'Twinkle Twinkle', 'content': 'Twinkle, twinkle, little star...'}]
        photos = [{'letter': 'A', 'word': 'Apple', 'image': 'apple.png'}]
        return render_template('english.html', alphabets=alphabets, rhymes=rhymes, photos=photos)
    except TemplateNotFound as e:
        logging.error(f"TemplateNotFound in english: {e}")
        flash('English template not found. Please contact support.', 'error')
        return redirect(url_for('subjects'))
    except Exception as e:
        logging.error(f"Error in english route: {e}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('subjects'))

@app.route('/hindi')
def hindi():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        alphabets = ['अ', 'आ', 'इ', 'ई']
        guninthalu = ['क', 'का', 'कि', 'की']
        rhymes = [{'title': 'मछली जल की रानी है', 'content': 'मछली जल की रानी है...'}]
        photos = [{'letter': 'अ', 'word': 'अनार', 'image': 'apple.png'}]
        return render_template('hindi.html', alphabets=alphabets, guninthalu=guninthalu, 
                              rhymes=rhymes, photos=photos)
    except TemplateNotFound as e:
        logging.error(f"TemplateNotFound in hindi: {e}")
        flash('Hindi template not found. Please contact support.', 'error')
        return redirect(url_for('subjects'))
    except Exception as e:
        logging.error(f"OperationalError in hindi route: {e}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('subjects'))

@app.route('/maths')
def maths():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        numbers = [1, 2, 3, 4]
        tables = [{'number': 2, 'content': '2 x 1 = 2, 2 x 2 = 4...'}]
        roman = [{'number': 1, 'roman': 'I'}, {'number': 2, 'roman': 'II'}]
        pictures = [{'number': 1, 'image': 'apple.png'}]
        return render_template('maths.html', numbers=numbers, tables=tables, roman=roman, 
                              pictures=pictures)
    except TemplateNotFound as e:
        logging.error(f"TemplateNotFound in maths: {e}")
        flash('Maths template not found. Please contact support.', 'error')
        return redirect(url_for('subjects'))
    except Exception as e:
        logging.error(f"Error in maths route: {e}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('subjects'))

@app.route('/practice', methods=['GET', 'POST'])
def practice():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    subjects = ['telugu', 'english', 'hindi', 'maths']
    selected_subject = request.form.get('subject') if request.method == 'POST' else None
    
    try:
        if selected_subject:
            questions = {
                'telugu': [{'q': 'అ + ఆ = ?', 'a': 'ఆ', 'options': ['అ', 'ఆ', 'ఇ', 'ఈ']}],
                'english': [{'q': 'A stands for?', 'a': 'Apple', 'options': ['Apple', 'Ball', 'Cat', 'Dog']}],
                'hindi': [{'q': 'अ stands for?', 'a': 'अनार', 'options': ['अनार', 'आम', 'इमली', 'ईख']}],
                'maths': [{'q': '2 + 2 = ?', 'a': '4', 'options': ['2', '3', '4', '5']}]
            }.get(selected_subject, [])
            random.shuffle(questions)
            return render_template('practice.html', subjects=subjects, selected_subject=selected_subject, questions=questions[:3])
        return render_template('practice.html', subjects=subjects, selected_subject=None, questions=[])
    except TemplateNotFound as e:
        logging.error(f"TemplateNotFound in practice: {e}")
        flash('Practice template not found. Please contact support.', 'error')
        return redirect(url_for('dashboard'))
    except Exception as e:
        logging.error(f"Error in practice route: {e}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('practice'))

@app.route('/submit_practice/<subject>', methods=['POST'])
def submit_practice(subject):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        correct = 0
        total = 0
        for q, a in request.form.items():
            if q.startswith('question_'):
                total += 1
                correct_answer = request.form.get(f'correct_{q}')
                if a == correct_answer:
                    correct += 1
        c.execute("INSERT OR REPLACE INTO practice (user_id, subject, correct, total) VALUES (?, ?, ?, ?)", 
                  (session['user_id'], subject, correct, total))
        c.execute("UPDATE progress SET percentage = ? WHERE user_id = ? AND subject = ?", 
                  (correct/total*100 if total > 0 else 0, session['user_id'], subject))
        if c.rowcount == 0:
            c.execute("INSERT INTO progress (user_id, subject, percentage) VALUES (?, ?, ?)", 
                      (session['user_id'], subject, correct/total*100 if total > 0 else 0))
        conn.commit()
        flash(f'Practice completed! Score: {correct}/{total}', 'success')
    except sqlite3.OperationalError as e:
        logging.error(f"OperationalError during submit_practice: {e}")
        flash('Database error. Please try again.', 'error')
    finally:
        conn.close()
    return redirect(url_for('practice'))

@app.route('/tracking')
def tracking():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute("SELECT subject, percentage FROM progress WHERE user_id = ?", (session['user_id'],))
        subject_progress = c.fetchall()
        c.execute("SELECT subject, correct, total FROM practice WHERE user_id = ?", (session['user_id'],))
        practice_progress = c.fetchall()
    except sqlite3.OperationalError as e:
        logging.error(f"OperationalError during tracking: {e}")
        flash('Database error. Please try again.', 'error')
        subject_progress = []
        practice_progress = []
    finally:
        conn.close()
    try:
        return render_template('tracking.html', subject_progress=subject_progress, 
                              practice_progress=practice_progress)
    except TemplateNotFound as e:
        logging.error(f"TemplateNotFound in tracking: {e}")
        flash('Tracking template not found. Please contact support.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        if request.method == 'POST':
            today = datetime.now().date()
            c.execute("SELECT last_checkin FROM checkin WHERE user_id = ?", (session['user_id'],))
            last_checkin = c.fetchone()
            if last_checkin:
                last_checkin_date = datetime.strptime(last_checkin[0], '%Y-%m-%d').date()
                if last_checkin_date < today:
                    c.execute("UPDATE checkin SET last_checkin = ?, coins = coins + 1 WHERE user_id = ?", 
                             (today.strftime('%Y-%m-%d'), session['user_id']))
                    c.execute("INSERT INTO checkin_history (user_id, checkin_date) VALUES (?, ?)", 
                             (session['user_id'], today.strftime('%Y-%m-%d')))
                    conn.commit()
                    flash('Check-in successful! +1 coin!', 'success')
                else:
                    flash('You already checked in today!', 'error')
            else:
                c.execute("INSERT INTO checkin (user_id, last_checkin, coins) VALUES (?, ?, ?)", 
                         (session['user_id'], today.strftime('%Y-%m-%d'), 1))
                c.execute("INSERT INTO checkin_history (user_id, checkin_date) VALUES (?, ?)", 
                         (session['user_id'], today.strftime('%Y-%m-%d')))
                conn.commit()
                flash('Check-in successful! +1 coin!', 'success')
        
        c.execute("SELECT last_checkin, coins FROM checkin WHERE user_id = ?", (session['user_id'],))
        checkin = c.fetchone()
        if checkin is None:
            c.execute("INSERT INTO checkin (user_id, last_checkin, coins) VALUES (?, ?, ?)", 
                     (session['user_id'], '2000-01-01', 0))
            conn.commit()
            checkin = ('2000-01-01', 0)
        
        c.execute("SELECT checkin_date FROM checkin_history WHERE user_id = ? ORDER BY checkin_date DESC LIMIT 5", 
                 (session['user_id'],))
        checkin_history = [row[0] for row in c.fetchall()]
        
        logging.info(f"Check-in data for user {session['user_id']}: last_checkin={checkin[0]}, coins={checkin[1]}, history={checkin_history}")
    except sqlite3.OperationalError as e:
        logging.error(f"OperationalError during checkin: {e}")
        flash('Database error. Please try again.', 'error')
        checkin = ('2000-01-01', 0)
        checkin_history = []
    except Exception as e:
        logging.error(f"Unexpected error during checkin: {e}")
        flash('An error occurred. Please try again.', 'error')
        checkin = ('2000-01-01', 0)
        checkin_history = []
    finally:
        conn.close()
    try:
        template_path = os.path.join(app.template_folder, 'checkin.html')
        logging.debug(f"Attempting to render template: {template_path}")
        if not os.path.exists(template_path):
            logging.error(f"Template file does not exist: {template_path}")
        return render_template('checkin.html', last_checkin=checkin[0], coins=checkin[1], checkin_history=checkin_history)
    except TemplateNotFound as e:
        logging.error(f"TemplateNotFound in checkin: {e}, expected at {template_path}")
        flash('Check-in template not found. Please contact support.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/debug_templates')
def debug_templates():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        template_folder = app.template_folder
        templates = glob.glob(os.path.join(template_folder, '*.html'))
        template_list = [os.path.basename(t) for t in templates]
        logging.info(f"Available templates in {template_folder}: {template_list}")
        return render_template('debug_templates.html', templates=template_list)
    except Exception as e:
        logging.error(f"Error in debug_templates: {e}")
        flash('Error listing templates. Please contact support.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)