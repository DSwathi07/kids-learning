@echo off 
echo <!DOCTYPE html> 
echo <html lang="en"> 
echo <head> 
echo     <meta charset="UTF-8"> 
echo     <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
echo     <title>Profile - EduApp</title> 
echo     <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"> 
echo     <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}"> 
echo     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"> 
echo     <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.5/gsap.min.js"></script> 
echo </head> 
echo <body class="bg-gray-100 min-h-screen"> 
echo     <div class="flex h-screen"> 
echo         <div class="bg-indigo-800 text-white w-64 flex-shrink-0"> 
echo             <div class="p-6"> 
echo                 <h1 class="text-2xl font-bold">EduApp</h1> 
echo             </div> 
echo             <nav class="mt-6"> 
echo                 <a href="{{ url_for('dashboard') }}" class="block py-2 px-6 hover:bg-indigo-700"><i class="fas fa-home mr-2"></i> Home</a> 
echo                 <a href="{{ url_for('profile') }}" class="block py-2 px-6 bg-indigo-700"><i class="fas fa-user mr-2"></i> Profile</a> 
echo                 <a href="{{ url_for('settings') }}" class="block py-2 px-6 hover:bg-indigo-700"><i class="fas fa-cog mr-2"></i> Settings</a> 
echo                 <a href="{{ url_for('logout') }}" class="block py-2 px-6 hover:bg-indigo-700"><i class="fas fa-sign-out-alt mr-2"></i> Logout</a> 
echo             </nav> 
echo         </div> 
echo         <div class="flex-1 flex flex-col"> 
echo             <div class="bg-white shadow p-6"> 
echo                 <h2 class="text-xl font-semibold">Your Profile</h2> 
echo             </div> 
echo             <div class="p-8 flex-1"> 
echo                 {%% with messages = get_flashed_messages() %%} 
echo                     {%% if messages %%} 
echo                         {%% for message in messages %%} 
echo                             <p class="text-green-500 text-center mb-4">{{ message }}</p> 
echo                         {%% endfor %%} 
echo                     {%% endif %%} 
echo                 {%% endwith %%} 
echo                 <div class="max-w-md mx-auto bg-white p-8 rounded-lg shadow-lg"> 
echo                     <div class="text-center mb-6"> 
echo                         <img src="{{ profile.profile_pic_url }}" alt="Profile Picture" class="w-32 h-32 rounded-full mx-auto mb-4"> 
echo                         <h3 class="text-2xl font-semibold">{{ profile.name or 'Set your name' }}</h3> 
echo                     </div> 
echo                     <form method="POST" action="{{ url_for('profile') }}"> 
echo                         <div class="mb-4"> 
echo                             <label for="name" class="block text-gray-700">Name</label> 
