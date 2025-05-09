@echo off 
echo from flask import Flask, render_template, request, redirect, url_for, session, flash 
echo from werkzeug.security import generate_password_hash, check_password_hash 
echo import sqlite3 
echo from datetime import datetime 
echo import os 
echo import logging 
echo from jinja2 import TemplateNotFound 
echo. 
echo logging.basicConfig(level=logging.DEBUG, format='%%(asctime)s %%(levelname)s: %%(message)s') 
echo logger = logging.getLogger(__name__) 
echo. 
echo app = Flask(__name__) 
echo app.secret_key = 'your_secret_key' 
echo UPLOAD_FOLDER = 'static/uploads' 
echo app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
echo. 
echo def init_db(): 
echo     try: 
echo         with sqlite3.connect('database.db') as conn: 
echo             c = conn.cursor() 
echo             c.execute('''CREATE TABLE IF NOT EXISTS users ( 
echo                 id INTEGER PRIMARY KEY AUTOINCREMENT, 
echo                 username TEXT UNIQUE NOT NULL, 
echo                 password TEXT NOT NULL, 
echo                 coins INTEGER DEFAULT 0, 
echo                 last_checkin TEXT 
echo             )''') 
echo             conn.commit() 
echo             logger.info("Database initialized successfully") 
echo     except Exception as e: 
echo         logger.error(f"Database initialization failed: {e}") 
echo         raise 
echo. 
echo try: 
echo     init_db() 
echo     os.makedirs(UPLOAD_FOLDER, exist_ok=True) 
echo except Exception as e: 
echo     logger.error(f"Startup error: {e}") 
echo     raise 
echo. 
echo @app.errorhandler(500) 
echo def internal_server_error(e): 
echo     logger.error(f"Internal Server Error: {str(e)}") 
echo     flash("An unexpected error occurred. Please try again.") 
echo     return render_template('error.html'), 500 
echo. 
echo @app.errorhandler(404) 
echo def not_found_error(e): 
echo     logger.error(f"Not Found: {str(e)}") 
echo     flash("Page not found. Please check the URL or try again.") 
echo     return render_template('error.html'), 404 
echo. 
echo @app.errorhandler(TemplateNotFound) 
echo def template_not_found(e): 
echo     logger.error(f"Template not found: {str(e)}") 
echo     flash(f"Template {e} not found. Please contact support.") 
echo     return render_template('error.html'), 404 
echo. 
echo @app.route('/') 
echo def index(): 
echo     try: 
echo         if 'user_id' in session: 
echo             return redirect(url_for('dashboard')) 
echo         return render_template('index.html') 
echo     except TemplateNotFound as e: 
echo         return template_not_found(e) 
echo     except Exception as e: 
echo         logger.error(f"Error in index: {e}") 
echo         return internal_server_error(e) 
echo. 
echo @app.route('/home') 
echo def home(): 
echo     try: 
echo         if 'user_id' not in session: 
echo             flash('Please log in to access this page.') 
echo             return redirect(url_for('login')) 
echo         return render_template('home.html') 
echo     except TemplateNotFound as e: 
echo         return template_not_found(e) 
echo     except Exception as e: 
echo         logger.error(f"Error in home: {e}") 
echo         return internal_server_error(e) 
echo. 
echo @app.route('/profile') 
echo def profile(): 
echo     try: 
echo         if 'user_id' not in session: 
echo             flash('Please log in to access this page.') 
echo             return redirect(url_for('login')) 
echo         return render_template('profile.html') 
echo     except TemplateNotFound as e: 
echo         return template_not_found(e) 
echo     except Exception as e: 
echo         logger.error(f"Error in profile: {e}") 
echo         return internal_server_error(e) 
echo. 
echo @app.route('/settings') 
echo def settings(): 
echo     try: 
echo         if 'user_id' not in session: 
echo             flash('Please log in to access this page.') 
echo             return redirect(url_for('login')) 
echo         return render_template('settings.html') 
echo     except TemplateNotFound as e: 
echo         return template_not_found(e) 
echo     except Exception as e: 
echo         logger.error(f"Error in settings: {e}") 
echo         return internal_server_error(e) 
echo. 
echo @app.route('/register', methods=['GET', 'POST']) 
echo def register(): 
echo     try: 
echo         if request.method == 'POST': 
echo             username = request.form['username'] 
echo             password = request.form['password'] 
echo             with sqlite3.connect('database.db') as conn: 
echo                 c = conn.cursor() 
echo                 c.execute('INSERT INTO users (username, password, coins) VALUES (?, ?, ?)', 
echo                           (username, generate_password_hash(password), 3)) 
echo                 conn.commit() 
echo                 flash('Registration successful! Please login.') 
echo                 return redirect(url_for('login')) 
echo         return render_template('register.html') 
echo     except sqlite3.IntegrityError: 
echo         flash('Username already exists!') 
echo         return render_template('register.html') 
echo     except TemplateNotFound as e: 
echo         return template_not_found(e) 
echo     except Exception as e: 
echo         logger.error(f"Error in register: {e}") 
echo         return internal_server_error(e) 
echo. 
echo @app.route('/login', methods=['GET', 'POST']) 
echo def login(): 
echo     try: 
echo         if request.method == 'POST': 
echo             username = request.form['username'] 
echo             password = request.form['password'] 
echo             with sqlite3.connect('database.db') as conn: 
echo                 c = conn.cursor() 
echo                 c.execute('SELECT * FROM users WHERE username = ?', (username,)) 
echo                 user = c.fetchone() 
echo             if user and check_password_hash(user[2], password): 
echo                 session['user_id'] = user[0] 
echo                 session['username'] = user[1] 
echo                 today = datetime.now().strftime('%%Y-%%m-%%d') 
echo                 if user[4] != today: 
echo                     with sqlite3.connect('database.db') as conn: 
echo                         c = conn.cursor() 
echo                         c.execute('UPDATE users SET coins = coins + 1, last_checkin = ? WHERE id = ?', 
echo                                  (today, user[0])) 
echo                         conn.commit() 
echo                 return redirect(url_for('dashboard')) 
echo             flash('Invalid credentials!') 
echo         return render_template('login.html') 
echo     except TemplateNotFound as e: 
echo         return template_not_found(e) 
echo     except Exception as e: 
echo         logger.error(f"Error in login: {e}") 
echo         return internal_server_error(e) 
echo. 
echo @app.route('/dashboard') 
echo def dashboard(): 
echo     try: 
echo         if 'user_id' not in session: 
echo             flash('Please log in to access this page.') 
echo             return redirect(url_for('login')) 
echo         with sqlite3.connect('database.db') as conn: 
echo             c = conn.cursor() 
echo             c.execute('SELECT coins FROM users WHERE id = ?', (session['user_id'],)) 
echo             coins = c.fetchone() 
echo             if coins is None: 
echo                 flash('User data not found.') 
echo                 return redirect(url_for('login')) 
echo         return render_template('dashboard.html', coins=coins[0]) 
echo     except TemplateNotFound as e: 
echo         return template_not_found(e) 
echo     except Exception as e: 
echo         logger.error(f"Error in dashboard: {e}") 
echo         return internal_server_error(e) 
echo. 
echo @app.route('/subjects') 
echo def subjects(): 
echo     try: 
echo         if 'user_id' not in session: 
echo             flash('Please log in to access this page.') 
echo             return redirect(url_for('login')) 
echo         return render_template('subjects.html') 
echo     except TemplateNotFound as e: 
echo         return template_not_found(e) 
echo     except Exception as e: 
echo         logger.error(f"Error in subjects: {e}") 
echo         return internal_server_error(e) 
echo. 
echo @app.route('/practice') 
echo def practice(): 
echo     try: 
echo         if 'user_id' not in session: 
echo             flash('Please log in to access this page.') 
echo             return redirect(url_for('login')) 
echo         return render_template('practice.html') 
echo     except TemplateNotFound as e: 
echo         return template_not_found(e) 
echo     except Exception as e: 
echo         logger.error(f"Error in practice: {e}") 
echo         return internal_server_error(e) 
echo. 
echo @app.route('/tracking') 
echo def tracking(): 
echo     try: 
echo         if 'user_id' not in session: 
echo             flash('Please log in to access this page.') 
echo             return redirect(url_for('login')) 
echo         return render_template('tracking.html') 
echo     except TemplateNotFound as e: 
echo         return template_not_found(e) 
echo     except Exception as e: 
echo         logger.error(f"Error in tracking: {e}") 
echo         return internal_server_error(e) 
echo. 
echo @app.route('/check_in') 
echo def check_in(): 
echo     try: 
echo         if 'user_id' not in session: 
echo             flash('Please log in to access this page.') 
echo             return redirect(url_for('login')) 
echo         with sqlite3.connect('database.db') as conn: 
echo             c = conn.cursor() 
echo             c.execute('SELECT last_checkin FROM users WHERE id = ?', (session['user_id'],)) 
echo             last_checkin = c.fetchone() 
echo             today = datetime.now().strftime('%%Y-%%m-%%d') 
echo             message = "Check-in successful! You earned 1 coin." 
echo             if last_checkin and last_checkin[0] == today: 
echo                 message = "You have already checked in today." 
echo             else: 
echo                 c.execute('UPDATE users SET coins = coins + 1, last_checkin = ? WHERE id = ?', 
echo                           (today, session['user_id'])) 
echo                 conn.commit() 
echo         return render_template('check_in.html', message=message) 
echo     except TemplateNotFound as e: 
echo         return template_not_found(e) 
echo     except Exception as e: 
echo         logger.error(f"Error in check_in: {e}") 
echo         return internal_server_error(e) 
echo. 
echo @app.route('/logout') 
echo def logout(): 
echo     try: 
echo         session.pop('user_id', None) 
echo         session.pop('username', None) 
echo         flash('Logged out successfully!') 
echo         return redirect(url_for('login')) 
echo     except Exception as e: 
echo         logger.error(f"Error in logout: {e}") 
echo         return internal_server_error(e) 
echo. 
echo if __name__ == '__main__': 
echo     app.run(debug=True) 
