Kids Learning App
Welcome to the Kids Learning App, a fun and interactive web application designed for children to learn Telugu, English, Hindi, and Maths through engaging activities, quizzes, and daily check-ins. Built with Flask, this app features a kid-friendly interface with vibrant colors, large buttons, and the playful Bubblegum Sans font.
Features

User Authentication:
Register with a username and password (includes Confirm Password validation).
Login to access the dashboard.
Forgot Password placeholder for future implementation.


Dashboard:
2x2 grid of buttons: Home, Profile, Settings, Contact Us, FAQ, Subjects, Practice, Tracking, Check-in.
Displays coin count earned through daily check-ins.


Learning Modules:
Subjects: 2x2 grid for Telugu, English, Hindi, Maths with sample content (e.g., alphabets, rhymes, numbers).
Practice: Multiple-choice quizzes for each subject, tracking correct/total answers and progress percentage.
Tracking: Displays subject progress and practice history.


Profile Management:
Update full name, date of birth, profile picture, and password.
Stores profile pictures in static/images/.


Contact Us:
Form to submit name and message, stored in the database.
Displays placeholder contact info (email, phone).


Daily Check-in:
Earn 1 coin per day by checking in.
View last check-in date, total coins, and recent check-in history (last 5 dates).


FAQ: Sample questions about the app’s functionality.
Settings: Placeholder page for future customization.
Kid-Friendly Design:
Vibrant colors (pink, blue, yellow, green).
Bubblegum Sans font for a playful look.
Large buttons and text for easy navigation.
Responsive layout for mobile devices (<600px).



Project Structure
language_learning_app/
├── app.py                    # Main Flask application
├── database.db               # SQLite database (generated on first run)
├── templates/                # HTML templates
│   ├── base.html             # Base template with header and flash messages
│   ├── register.html         # Registration form
│   ├── login.html            # Login form
│   ├── forgot_password.html  # Forgot password placeholder
│   ├── dashboard.html        # Dashboard with 2x2 button grid
│   ├── profile.html          # Profile update form
│   ├── faq.html              # FAQ page with sample questions
│   ├── subjects.html         # Subjects selection (2x2 grid)
│   ├── practice.html         # Practice quizzes
│   ├── telugu.html           # Telugu learning content
│   ├── english.html          # English learning content
│   ├── hindi.html            # Hindi learning content
│   ├── maths.html            # Maths learning content
│   ├── tracking.html         # Progress tracking
│   ├── checkin.html          # Daily check-in page
│   ├── settings.html         # Settings placeholder
│   ├── contact_us.html       # Contact form and info
│   ├── debug_templates.html  # Debug route to list templates
├── static/                   # Static assets
│   ├── css/
│   │   ├── style.css         # Styles for kid-friendly design
│   ├── js/
│   │   ├── script.js         # Placeholder for JavaScript
│   ├── images/
│   │   ├── amma.png          # Sample image for Telugu
│   │   ├── apple.png         # Sample image for English/Math
│   │   ├── default_profile.png # Default profile picture
├── README.md                 # This file

Prerequisites

Python: Version 3.6 or higher
Flask: Python web framework
SQLite: For database storage (included with Python)
Git: For cloning the repository

Setup Instructions

Clone the Repository:
git clone https://github.com/your-username/kids-learning-app.git
cd kids-learning-app


Create a Virtual Environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


Install Dependencies:
pip install flask


Verify Folder Structure:

Ensure the templates/ folder contains all .html files listed above, especially:
base.html
checkin.html
contact_us.html
dashboard.html
debug_templates.html


Confirm static/css/style.css and static/images/ exist with sample images.


Initialize the Database:

Delete any existing database.db to ensure a fresh schema:rm database.db


The app will create database.db on first run with tables:
users, profiles, progress, practice, checkin, contact_messages, checkin_history




Run the Application:
python app.py


Open http://127.0.0.1:5000 in a browser.
The app starts in debug mode for development.


Test the App:

Register: Create a user (e.g., Username: Swathi, Password: test123, Confirm Password: test123).
Login: Access the dashboard.
Dashboard: Verify the 2x2 button grid:Home        Subjects
Profile     Practice
Settings    Tracking
Contact Us  Check in
FAQ


Contact Us: Submit a form (e.g., Name: Swathi, Message: “Love the app!”).
Check-in: Click “Check In Now!” to earn a coin (once per day).
Debug Templates: Visit /debug_templates to list available templates.



Troubleshooting
TemplateNotFound Errors
If you see “Check-in template not found. Please contact support.” or “Contact Us template not found. Please contact support.”:

Check Templates:

Verify checkin.html and contact_us.html exist in templates/:ls templates/

Expected: base.html checkin.html contact_us.html debug_templates.html (among others).
Ensure filenames are exact (no typos, e.g., check-in.html or contactus.html).


Confirm base.html:

Both templates extend base.html. Check it exists:cat templates/base.html




Inspect Logs:

Check the terminal for errors:ERROR - TemplateNotFound in checkin: checkin.html, expected at /path/to/kids-learning-app/templates/checkin.html


Note the path and verify the file exists there.


Debug Templates:

Visit http://localhost:5000/debug_templates after logging in.
Ensure checkin.html and contact_us.html appear in the list.
If missing, re-create them from the repository.


Fix Permissions:

Ensure Flask can read templates:chmod -R 755 templates




Clear Cache:

Delete __pycache__ folders:rm -rf __pycache__ templates/__pycache__


Restart the server:python app.py




Re-create Templates:

Copy checkin.html, contact_us.html, and base.html from the repository’s templates/ folder.
Save with correct names in templates/.



Database Errors

OperationalError: no such table:
Delete database.db and restart the app:rm database.db
python app.py





Other Issues

ModuleNotFoundError: No module named 'flask':
Re-install Flask:pip install flask




Share terminal logs and /debug_templates output in a GitHub issue for help.

Contributing
We welcome contributions to make the Kids Learning App even better! To contribute:

Fork the Repository:

Click “Fork” on GitHub to create your copy.


Create a Branch:
git checkout -b feature/your-feature


Make Changes:

Add features (e.g., email sending for Contact Us, animations for Check-in).
Fix bugs (e.g., template issues, database errors).
Update documentation.


Test Changes:

Ensure the app runs without errors.
Verify kid-friendly design (vibrant colors, Bubblegum Sans, large buttons).


Commit and Push:
git add .
git commit -m "Add your feature or fix"
git push origin feature/your-feature


Create a Pull Request:

Submit a PR on GitHub with a clear description of changes.



Future Enhancements

Email Integration: Send Contact Us messages via email using Flask-Mail.
Animations: Add button bounce effects for Check-in or dashboard buttons.
Settings Features: Add theme selection or notification preferences.
Expanded Content: More questions, rhymes, and images for learning modules.
Progress Visuals: Charts or graphs for tracking progress.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For questions or support:

GitHub Issues: Open an issue at github.com/your-username/kids-learning-app/issues.
Email: support@kidslearningapp.com (placeholder).

Thank you for using the Kids Learning App! Let’s make learning fun for kids! 🚀
