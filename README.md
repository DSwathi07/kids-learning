PROJECT TITLE : Kids Learning App

Video Demo : https://youtu.be/3HuaCruxULc


Description:

The Kids Learning App is a vibrant, Flask-based web application designed to make learning fun for children. It provides interactive modules for Telugu, English, Hindi, and Maths, with features like daily check-ins, practice quizzes, and progress tracking. The app prioritizes a kid-friendly interface with bright colors (pink, blue, yellow), large buttons, and the playful Bubblegum Sans font, ensuring accessibility for young users. Built with Python, Flask, SQLite, and Jinja2, it supports user registration, profile management, and a contact form, all tailored for ease of use on desktops and mobile devices (<600px screens). This project was developed to create an engaging educational tool, addressing challenges like template errors during implementation.

The app’s core functionality revolves around a dashboard with a 2x2 button grid, guiding users to features like Subjects, Practice, Check-in, and Contact Us. Users register with a username and password, log in, and earn coins daily via the Check-in page. The Subjects section offers sample content (e.g., Telugu alphabets, English rhymes), while Practice provides multiple-choice quizzes with progress tracking. The Contact Us page lets users send messages stored in the database, and the Profile page allows updates to personal details and profile pictures. The app uses SQLite for lightweight data storage, with tables for users, profiles, check-ins, and messages.

Files and Their Roles

app.py: The main Flask application, defining routes for registration (/register), login (/login), dashboard (/dashboard), and more. It handles database initialization (SQLite tables: users, profiles, checkin, etc.), session management, and error handling (e.g., TemplateNotFound). A debug route (/debug_templates) lists templates to troubleshoot errors. Logging was added to diagnose missing templates like checkin.html.

templates/base.html: The base Jinja2 template, providing a consistent layout with a header (“Kids Learning App”), navigation (Login/Logout), and flash messages for user feedback (e.g., “Check-in successful!”). All other templates extend this.

templates/register.html: A form for user registration, requiring a username, password, and password confirmation. It enforces password matching and checks for unique usernames.
templates/login.html: A login form validating username and password, redirecting to the dashboard on success.
templates/forgot_password.html: A placeholder for password recovery, currently displaying a form with no backend logic.
templates/dashboard.html: The main hub, featuring a 2x2 button grid (Home, Profile, Settings, Contact Us, FAQ, Subjects, Practice, Tracking, Check-in) and coin count. Buttons use vibrant colors (e.g., pink for Contact Us, blue for Check-in).
templates/profile.html: Allows users to update their full name, date of birth, password, and profile picture, stored in static/images/.
templates/subjects.html: Displays a 2x2 grid for selecting Telugu, English, Hindi, or Maths, each linking to subject-specific content.
templates/telugu.html, english.html, hindi.html, maths.html: Subject pages with sample content (e.g., alphabets, rhymes, numbers). Each uses lists and images (e.g., apple.png).
templates/practice.html: Offers quizzes with three random questions per subject, tracking scores in the practice table.
templates/tracking.html: Shows progress percentages and practice history per subject.
templates/checkin.html: Displays last check-in date, coins, and a “Check In Now!” button (blue, red on hover). It lists recent check-ins (last 5 dates) in green boxes. Initially caused a TemplateNotFound error due to misplacement.
templates/contact_us.html: A form for name and message, with placeholder contact info (email, phone) in a yellow box. Also faced TemplateNotFound issues.
templates/faq.html: Lists sample FAQs about the app’s features.
templates/settings.html: A placeholder for future customization options.
templates/debug_templates.html: Lists all templates in templates/ to debug missing files.
static/css/style.css: Defines kid-friendly styling: Bubblegum Sans font, vibrant colors (e.g., #FF5555 red, #00AAFF blue), large buttons (1.2em–1.5em), and responsive layouts (single-column <600px).
static/images/: Stores profile pictures and sample images (amma.png, apple.png, default_profile.png).
static/js/script.js: A placeholder for future JavaScript enhancements.
database.db: SQLite database, auto-created with tables for users, profiles, progress, check-ins, and messages.

Design Choices

Several design decisions shaped the project:

Flask and SQLite: I chose Flask for its simplicity and Python integration, ideal for a small-scale educational app. SQLite was selected over MySQL for its lightweight, serverless nature, avoiding external database setup for users. This supports quick deployment but limits scalability, a trade-off acceptable for a prototype.

Kid-Friendly UI: The 2x2 dashboard and subjects grids prioritize simplicity, with large, colorful buttons (e.g., #FF55AA pink for Contact Us) to attract young users. Bubblegum Sans enhances playfulness, and responsive CSS ensures mobile usability. I debated a 3x3 grid but found 2x2 clearer for kids

TemplateNotFound Handling: Initially, missing checkin.html and contact_us.html caused errors. I added try/except TemplateNotFound in app.py to flash user-friendly messages (e.g., “Contact Us template not found. Please contact support.”) and redirect to the dashboard. A /debug_templates route was introduced to list templates, helping diagnose file placement issues. These were critical for robustness, as template misplacement was a recurring issue.
Database Schema: Tables like checkin_history and contact_messages were added to support new features. I considered a single history table but used separate tables for clarity. SQLite’s simplicity avoided complex migrations, though it required resetting database.db during schema updates.
No Email for Contact Us: Per requirements, the Contact Us form stores messages in the database instead of sending emails, simplifying implementation. I debated Flask-Mail integration but prioritized core functionality.

Coin System: The Check-in feature awards one coin daily, stored in the checkin table. I considered streaks or bonus coins but kept it simple to focus on engagement.

Challenges and Solutions

The most significant challenge was the TemplateNotFound errors for checkin.html and contact_us.html. These arose because the templates were not in the templates/ folder or had incorrect names. I resolved this by:

Providing exact template content in responses (May 08, 2025).

Adding logging in app.py to output template paths (e.g., /path/to/templates/checkin.html).
Creating /debug_templates to list available templates, confirming checkin.html and contact_us.html presence.

Instructing users to verify the templates/ folder and permissions (chmod -R 755 templates).

Another challenge was ensuring the database schema supported new tables (contact_messages, checkin_history). Deleting database.db and reinitializing it resolved OperationalError: no such table issues. I also debated client-side JavaScript for animations (e.g., button bounces) but prioritized server-side stability.

Setup and Usage

To run the app:
Clone the repository: git clone https://github.com/your-username/kids-learning-app.git.
Install Flask: pip install flask.
Ensure templates/ contains all .html files and static/css/style.css exists.
Delete database.db to reset the schema.
Run: python app.py.
Visit http://127.0.0.1:5000, register, and explore features.

If TemplateNotFound errors occur, check templates/checkin.html and templates/contact_us.html, use /debug_templates, and review terminal logs.

Future Improvements

submit50 cs50/problems/2025/x/project


Add Flask-Mail for Contact Us email notifications.
Implement animations (e.g., CSS keyframes for button clicks).
Expand quiz questions and subject content.
Add progress charts using Chart.js.

This project was a rewarding journey in building an educational tool for kids. It balances functionality, usability, and fun, with room for growth. I’m proud of its vibrant design and robust error handling, making it a solid foundation for future enhancements.
