@echo off 
echo <!DOCTYPE html> 
echo <html lang="en"> 
echo <head> 
echo     <meta charset="UTF-8"> 
echo     <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
echo     <title>Dashboard - EduApp</title> 
echo     <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"> 
echo     <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}"> 
echo     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"> 
echo </head> 
echo <body class="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 min-h-screen flex"> 
echo     <aside class="menu-bar bg-gray-900 text-white w-16 flex flex-col items-center py-4 space-y-4"> 
echo         <a href="{{ url_for('home') }}" class="menu-btn text-2xl hover:text-indigo-400 transition-transform transform hover:scale-110" title="Home"><i class="fas fa-home"></i></a> 
echo         <a href="{{ url_for('profile') }}" class="menu-btn text-2xl hover:text-indigo-400 transition-transform transform hover:scale-110" title="Profile"><i class="fas fa-user"></i></a> 
echo         <a href="{{ url_for('settings') }}" class="menu-btn text-2xl hover:text-indigo-400 transition-transform transform hover:scale-110" title="Settings"><i class="fas fa-cog"></i></a> 
echo     </aside> 
echo     <main class="flex-1 flex flex-col p-4"> 
echo         <header class="flex justify-between items-center mb-8"> 
echo             <h1 class="welcome-text text-3xl font-bold text-white text-center flex-1" data-text="Welcome, {{ session['username'] }}!">Welcome, {{ session['username'] }}!</h1> 
echo             <div class="coins bg-yellow-400 text-gray-900 px-4 py-2 rounded-full font-semibold">Coins: {{ coins }}</div> 
echo         </header> 
echo         <nav class="dashboard-nav flex justify-center space-x-4"> 
echo             <a href="{{ url_for('subjects') }}" class="nav-btn bg-indigo-600 text-white px-6 py-3 rounded-full hover:bg-indigo-700 transition-transform transform hover:scale-105">Subjects</a> 
echo             <a href="{{ url_for('practice') }}" class="nav-btn bg-indigo-600 text-white px-6 py-3 rounded-full hover:bg-indigo-700 transition-transform transform hover:scale-105">Practice</a> 
echo             <a href="{{ url_for('tracking') }}" class="nav-btn bg-indigo-600 text-white px-6 py-3 rounded-full hover:bg-indigo-700 transition-transform transform hover:scale-105">Tracking</a> 
echo             <a href="{{ url_for('check_in') }}" class="nav-btn bg-indigo-600 text-white px-6 py-3 rounded-full hover:bg-indigo-700 transition-transform transform hover:scale-105">Check-In</a> 
echo             <a href="{{ url_for('logout') }}" class="nav-btn bg-red-600 text-white px-6 py-3 rounded-full hover:bg-red-700 transition-transform transform hover:scale-105">Logout</a> 
echo         </nav> 
echo     </main> 
echo     <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.5/gsap.min.js"></script> 
echo     <script src="{{ url_for('static', filename='js/script.js') }}"></script> 
echo </body> 
echo </html> 
