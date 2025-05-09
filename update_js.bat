@echo off 
echo document.addEventListener('DOMContentLoaded', () =
echo     const welcomeText = document.querySelector('.welcome-text'); 
echo     const text = welcomeText.getAttribute('data-text'); 
echo     welcomeText.textContent = ''; 
echo     gsap.to(welcomeText, { opacity: 1, duration: 1 }); 
echo     let i = 0; 
echo     function type() { 
echo             welcomeText.textContent += text.charAt(i); 
echo             i++; 
echo             setTimeout(type, 50); 
echo         } 
echo     } 
echo     setTimeout(type, 1000); 
echo }); 
