@echo off 
echo <!DOCTYPE html> 
echo <html lang="en"> 
echo <head> 
echo     <meta charset="UTF-8"> 
echo     <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
echo     <title>Subjects - EduApp</title> 
echo     <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"> 
echo     <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}"> 
echo     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"> 
echo </head> 
echo <body class="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 min-h-screen flex items-center justify-center"> 
echo     <div class="container mx-auto p-8"> 
echo         <h1 class="text-4xl font-bold text-center text-white mb-12">Explore Subjects</h1> 
echo         <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8"> 
echo             <div class="card bg-white p-6 rounded-2xl shadow-xl text-center"> 
echo                 <i class="fas fa-book text-4xl text-indigo-600 mb-4"></i> 
echo                 <h2 class="text-2xl font-semibold text-gray-800 mb-2">Telugu</h2> 
echo                 <p class="text-gray-600">Learn Telugu letters, words, and stories with fun activities!</p> 
echo             </div> 
echo             <div class="card bg-white p-6 rounded-2xl shadow-xl text-center"> 
echo                 <i class="fas fa-book text-4xl text-indigo-600 mb-4"></i> 
echo                 <h2 class="text-2xl font-semibold text-gray-800 mb-2">Hindi</h2> 
echo                 <p class="text-gray-600">Discover Hindi alphabets and simple sentences with games!</p> 
echo             </div> 
echo             <div class="card bg-white p-6 rounded-2xl shadow-xl text-center"> 
echo                 <i class="fas fa-book text-4xl text-indigo-600 mb-4"></i> 
echo                 <h2 class="text-2xl font-semibold text-gray-800 mb-2">English</h2> 
echo                 <p class="text-gray-600">Master English letters, words, and stories with exciting tasks!</p> 
echo             </div> 
echo             <div class="card bg-white p-6 rounded-2xl shadow-xl text-center"> 
echo                 <i class="fas fa-calculator text-4xl text-indigo-600 mb-4"></i> 
echo                 <h2 class="text-2xl font-semibold text-gray-800 mb-2">Maths</h2> 
echo                 <p class="text-gray-600">Solve fun math problems and learn numbers with puzzles!</p> 
echo             </div> 
echo         </div> 
echo         <a href="{{ url_for('dashboard') }}" class="block mt-12 bg-indigo-600 text-white px-6 py-3 rounded-full hover:bg-indigo-700 transition-transform transform hover:scale-105 text-center max-w-xs mx-auto">Back to Dashboard</a> 
echo     </div> 
echo </body> 
echo </html> 
