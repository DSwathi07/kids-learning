@echo off 
echo <!DOCTYPE html> 
echo <html lang="en"> 
echo <head> 
echo     <meta charset="UTF-8"> 
echo     <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
echo     <title>Practice - EduApp</title> 
echo     <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"> 
echo     <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}"> 
echo     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"> 
echo     <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.5/gsap.min.js"></script> 
echo </head> 
echo <body class="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 min-h-screen flex items-center justify-center"> 
echo     <div class="container mx-auto p-8"> 
echo         <h1 class="text-4xl font-bold text-center text-white mb-12">Practice Time</h1> 
echo         <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8"> 
echo             <div class="card bg-white p-6 rounded-2xl shadow-xl text-center transform hover:scale-105 transition-transform duration-300"> 
echo                 <i class="fas fa-pencil-alt text-4xl text-indigo-600 mb-4"></i> 
echo                 <h2 class="text-2xl font-semibold text-gray-800 mb-2">??????</h2> 
echo                 <p class="text-gray-600 mb-4">'?' ?????? ????????</p> 
echo                 <button onclick="showTask('Telugu', '????????: ?????? ?')" class="bg-green-500 text-white px-4 py-2 rounded-full hover:bg-green-600 transition-transform transform hover:scale-105">Try Now</button> 
echo             </div> 
echo             <div class="card bg-white p-6 rounded-2xl shadow-xl text-center transform hover:scale-105 transition-transform duration-300"> 
echo                 <i class="fas fa-pencil-alt text-4xl text-indigo-600 mb-4"></i> 
echo                 <h2 class="text-2xl font-semibold text-gray-800 mb-2">?????</h2> 
echo                 <p class="text-gray-600 mb-4">'????' ?? 'Water' ?? ??????</p> 
echo                 <button onclick="showTask('Hindi', '??????: ???? = Water')" class="bg-green-500 text-white px-4 py-2 rounded-full hover:bg-green-600 transition-transform transform hover:scale-105">Try Now</button> 
echo             </div> 
echo             <div class="card bg-white p-6 rounded-2xl shadow-xl text-center transform hover:scale-105 transition-transform duration-300"> 
echo                 <i class="fas fa-pencil-alt text-4xl text-indigo-600 mb-4"></i> 
echo                 <h2 class="text-2xl font-semibold text-gray-800 mb-2">English</h2> 
echo                 <p class="text-gray-600 mb-4">Spell the word 'Cat'</p> 
echo                 <button onclick="showTask('English', 'Spell: Cat')" class="bg-green-500 text-white px-4 py-2 rounded-full hover:bg-green-600 transition-transform transform hover:scale-105">Try Now</button> 
echo             </div> 
echo             <div class="card bg-white p-6 rounded-2xl shadow-xl text-center transform hover:scale-105 transition-transform duration-300"> 
echo                 <i class="fas fa-pencil-alt text-4xl text-indigo-600 mb-4"></i> 
echo                 <h2 class="text-2xl font-semibold text-gray-800 mb-2">Maths</h2> 
echo                 <p class="text-gray-600 mb-4">Solve: 2 + 3 = ?</p> 
echo                 <button onclick="showTask('Maths', 'Solve: 2 + 3 = ?')" class="bg-green-500 text-white px-4 py-2 rounded-full hover:bg-green-600 transition-transform transform hover:scale-105">Try Now</button> 
echo             </div> 
echo         </div> 
echo         <a href="{{ url_for('dashboard') }}" class="block mt-12 bg-indigo-600 text-white px-6 py-3 rounded-full hover:bg-indigo-700 transition-transform transform hover:scale-105 text-center max-w-xs mx-auto">Back to Dashboard</a> 
echo     </div> 
echo     <script> 
echo         function showTask(subject, task) { 
echo             alert(`Practice ${subject}: ${task}`); 
echo         } 
echo         document.addEventListener('DOMContentLoaded', () =
echo             gsap.from('.card', { 
echo                 opacity: 0, 
echo                 y: 50, 
echo                 duration: 1, 
echo                 stagger: 0.2, 
echo                 ease: 'power2.out' 
echo             }); 
echo         }); 
echo     </script> 
echo </body> 
echo </html> 
