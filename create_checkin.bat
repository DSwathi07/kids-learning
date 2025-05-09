@echo off 
echo <!DOCTYPE html> 
echo <html lang="en"> 
echo <head> 
echo     <meta charset="UTF-8"> 
echo     <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
echo     <title>Check-In - EduApp</title> 
echo     <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"> 
echo     <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}"> 
echo </head> 
echo <body class="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 min-h-screen flex items-center justify-center"> 
echo     <div class="container bg-white p-8 rounded-2xl shadow-xl max-w-md"> 
echo         <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">Daily Check-In</h1> 
echo         <p class="text-center text-gray-600 mb-6">{{ message }}</p> 
echo         <a href="{{ url_for('dashboard') }}" class="block bg-indigo-600 text-white px-6 py-3 rounded-full hover:bg-indigo-700 transition-transform transform hover:scale-105 text-center">Back to Dashboard</a> 
echo     </div> 
echo </body> 
echo </html> 
