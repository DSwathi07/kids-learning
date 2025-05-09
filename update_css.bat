@echo off 
echo @keyframes gradient { 
echo     0%% { background-position: 0%% 50%%; } 
echo     50%% { background-position: 100%% 50%%; } 
echo     100%% { background-position: 0%% 50%%; } 
echo } 
echo body { 
echo     background: linear-gradient(45deg, #4b6cb7, #182848, #4b6cb7); 
echo     background-size: 400%%; 
echo     animation: gradient 15s ease infinite; 
echo } 
echo .welcome-text { 
echo     opacity: 0; 
echo } 
echo .coins { 
echo     transition: transform 0.3s ease; 
echo } 
echo .coins:hover { 
echo     transform: scale(1.1); 
echo } 
echo .card { 
echo     transition: transform 0.3s ease, box-shadow 0.3s ease; 
echo } 
echo .card:hover { 
echo     transform: translateY(-5px); 
echo     box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2); 
echo } 
echo .alert { 
echo     animation: slideIn 0.5s ease; 
echo } 
echo @keyframes slideIn { 
echo     from { transform: translateY(-20px); opacity: 0; } 
echo     to { transform: translateY(0); opacity: 1; } 
echo } 
