import streamlit as st
import streamlit.components.v1 as components
import base64
import os

def render():
    """
    Renders the modern, animated "Meet the Developer" section.
    Simply call `developer_profile.render()` inside your app.py to display this component.
    """
    
    # Dynamically load the profile picture as base64 to inject securely into the HTML iframe
    avatar_html = '<div class="avatar-img"><i class="fas fa-user-tie"></i></div>'
    for ext in ['png', 'jpg', 'jpeg', 'webp']:
        img_path = os.path.join("img", f"yogesh_pfp.{ext}")
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode()
                avatar_html = f'<img src="data:image/{ext};base64,{b64_data}" style="width: 100%; height: 100%; border-radius: 50%; object-fit: cover;" alt="Yogesh Patel">'
            break
            
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Developer Profile</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-indigo: #6366f1;
            --secondary-indigo: #4338ca;
            --coffee-gold: #f59e0b;
            --card-bg: #ffffff;
            --text: #475569;
            --heading: #0f172a;
        }
        
        body {
            margin: 0;
            padding: 1.5rem;
            font-family: 'Inter', -apple-system, sans-serif;
            background: transparent; /* Blends with Streamlit */
            color: var(--heading);
            overflow: hidden;
        }

        /* Subtle Particle Background */
        .particles { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; pointer-events: none; }
        .particle { position: absolute; border-radius: 50%; background: var(--primary-indigo); opacity: 0.15; animation: floatUp linear infinite; }
        @keyframes floatUp {
            0% { transform: translateY(100vh) scale(0); opacity: 0; }
            50% { opacity: 0.5; }
            100% { transform: translateY(-20vh) scale(1); opacity: 0; }
        }

        /* Grid Layout */
        .dev-wrapper {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            max-width: 900px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
            animation: cascadeSlideUp 0.8s ease-out;
        }
        @keyframes cascadeSlideUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }

        /* Glassmorphism Cards */
        .glass-card {
            background: var(--card-bg);
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            padding: 2.5rem 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.3s ease, border-color 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            border-color: var(--primary-indigo);
        }

        /* Profile Section */
        .profile-content { text-align: center; }
        .avatar-container { position: relative; width: 130px; height: 130px; margin: 0 auto 1.5rem; }
        .avatar-glow {
            width: 100%; height: 100%; border-radius: 50%;
            background: linear-gradient(135deg, var(--primary-indigo), var(--secondary-indigo));
            padding: 4px; box-sizing: border-box;
            animation: pulse-glow 3s infinite alternate;
        }
        .avatar-img {
            width: 100%; height: 100%; border-radius: 50%;
            background: #f8fafc; display: flex; align-items: center; justify-content: center;
            font-size: 3.5rem;
        }
        @keyframes pulse-glow {
            0% { box-shadow: 0 0 10px rgba(99, 102, 241, 0.3); }
            100% { box-shadow: 0 0 20px rgba(67, 56, 202, 0.5); }
        }
        
        .name { font-size: 2.2rem; font-weight: 800; margin: 0; color: var(--heading); }
        .title { font-size: 1.1rem; color: var(--text); margin-top: 0.5rem; font-weight: 500; letter-spacing: 0.5px; }

        /* Social Links */
        .social-links { display: flex; justify-content: center; gap: 1.5rem; margin-top: 2rem; }
        .social-btn { color: #64748b; font-size: 1.6rem; transition: all 0.3s ease; text-decoration: none; }
        .social-btn:hover { color: var(--primary-indigo); transform: translateY(-4px) scale(1.1); text-shadow: 0 0 10px rgba(99,102,241,0.2); }

        /* Coffee & Supporter Section */
        .coffee-content { text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; }
        
        .coffee-cup-container { position: relative; margin-bottom: 1.5rem; cursor: pointer; user-select: none; }
        .coffee-cup { font-size: 4.5rem; animation: float 3s ease-in-out infinite; }
        .steam { position: absolute; font-size: 1.5rem; opacity: 0; }
        .steam-1 { top: -10px; left: 15px; animation: steaming 2.5s ease-out infinite; }
        .steam-2 { top: -15px; right: 15px; animation: steaming 2.5s ease-out infinite 1.2s; }
        
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-12px); } }
        @keyframes steaming { 0% { transform: translateY(0) scale(0.8); opacity: 0; } 50% { opacity: 0.7; } 100% { transform: translateY(-35px) scale(1.2); opacity: 0; } }

        .rotating-msg { height: 50px; font-size: 1.1rem; color: var(--coffee-gold); font-weight: 600; margin-bottom: 1rem; transition: opacity 0.5s ease; display: flex; align-items: center; justify-content: center; }

        /* Pulse Support Button */
        .support-btn {
            background: linear-gradient(135deg, #fbbf24, var(--coffee-gold));
            color: white; font-weight: 800; font-size: 1.1rem;
            padding: 1rem 2.5rem; border: none; border-radius: 30px;
            cursor: pointer; position: relative; overflow: visible;
            box-shadow: 0 0 15px rgba(245, 158, 11, 0.3);
            animation: btnPulse 2.5s infinite; transition: all 0.3s ease;
        }
        .support-btn:hover { transform: scale(1.05); box-shadow: 0 0 20px rgba(245, 158, 11, 0.5); animation: none; }
        @keyframes btnPulse { 0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.5); } 70% { box-shadow: 0 0 0 15px rgba(245, 158, 11, 0); } 100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); } }

        .heart { position: absolute; font-size: 1.5rem; pointer-events: none; animation: floatHeart 1s ease-out forwards; z-index: 10; }
        @keyframes floatHeart { 0% { transform: translateY(0) scale(0.5); opacity: 1; } 100% { transform: translateY(-60px) scale(1.5); opacity: 0; } }

        /* Hall of Legends */
        .legends-container { margin-top: 2rem; background: #f8fafc; padding: 1rem; border-radius: 16px; width: 100%; border: 1px solid #e2e8f0; }
        .legends-title { font-size: 0.85rem; color: #64748b; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; }
        .counter-val { font-size: 1.8rem; font-weight: 800; color: var(--primary-indigo); font-variant-numeric: tabular-nums; }
        .badges { display: flex; justify-content: center; gap: 1rem; margin-top: 0.5rem; }
        .badge { font-size: 1.4rem; filter: drop-shadow(0 0 5px rgba(0,0,0,0.1)); transition: transform 0.3s ease; cursor: default; }
        .badge:hover { transform: scale(1.2) rotate(10deg); }

        /* Easter Egg Toast */
        .toast {
            position: fixed; bottom: -100px; left: 50%; transform: translateX(-50%);
            background: linear-gradient(135deg, var(--secondary-indigo), var(--primary-indigo));
            color: white; padding: 1rem 2rem; border-radius: 30px; font-weight: bold;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5); transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            z-index: 100; text-align: center; white-space: nowrap;
        }
    </style>
    </head>
    <body>

    <div class="particles" id="particles"></div>
    <div class="toast" id="toast">Achievement Unlocked: Chief Caffeine Officer</div>

    <div class="dev-wrapper">
        <!-- Profile Card -->
        <div class="glass-card">
            <div class="profile-content">
                <div class="avatar-container">
                    <div class="avatar-glow">
                        <!-- AVATAR_PLACEHOLDER -->
                    </div>
                </div>
                <h2 class="name">Yogesh Patel</h2>
                <p class="title">Business Intelligence Analyst</p>
                
                <div class="social-links">
                    <a href="https://linkedin.com/in/yogesh-patel-842376158" target="_blank" class="social-btn" title="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                    <a href="https://portfolio-ashy-theta-24.vercel.app/" target="_blank" class="social-btn" title="Portfolio Website"><i class="fas fa-globe"></i></a>
                    <a href="mailto:yogesh.dav99@gmail.com" class="social-btn" title="Email"><i class="fas fa-envelope"></i></a>
                </div>
            </div>
        </div>

        <!-- Support Card -->
        <div class="glass-card">
            <div class="coffee-content">
                <div class="coffee-cup-container" style="color: var(--coffee-gold); font-size: 3rem; margin-bottom: 2rem;" id="coffee-btn" title="Click me 5 times!">
                    <div class="steam steam-1"><i class="fas fa-wind"></i></div>
                    <div class="steam steam-2"><i class="fas fa-wind"></i></div>
                    <div class="coffee-cup"><i class="fas fa-mug-hot"></i></div>
                </div>
                
                <div class="rotating-msg" id="rotating-msg">This app runs on Python and caffeine.</div>
                
                <button class="support-btn" id="support-btn" onclick="window.open('https://buymeacoffee.com/yogeshpatel', '_blank')">Buy Me a Coffee</button>

                <div class="legends-container">
                    <div class="legends-title">Developers Fueled</div>
                    <div class="counter-val" id="counter">0</div>
                    <div class="badges">
                        <span class="badge" title="Gold Supporter"><i class="fas fa-medal" style="color: #ffd700;"></i></span>
                        <span class="badge" title="Silver Supporter"><i class="fas fa-medal" style="color: #c0c0c0;"></i></span>
                        <span class="badge" title="Bronze Supporter"><i class="fas fa-medal" style="color: #cd7f32;"></i></span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Generate subtle background particles
        const particlesContainer = document.getElementById('particles');
        for (let i = 0; i < 20; i++) {
            let p = document.createElement('div');
            p.className = 'particle';
            let size = Math.random() * 4 + 2;
            p.style.width = size + 'px'; p.style.height = size + 'px';
            p.style.left = Math.random() * 100 + '%';
            p.style.animationDuration = (Math.random() * 5 + 5) + 's';
            p.style.animationDelay = (Math.random() * 5) + 's';
            particlesContainer.appendChild(p);
        }

        // Funny Rotating Messages
        const msgs = [
            "This app runs on Python and caffeine.",
            "Every coffee adds +10 coding speed.",
            "Warning: Donations may result in more features.",
            "Powered by curiosity and espresso shots"
        ];
        let msgIdx = 0;
        const msgEl = document.getElementById('rotating-msg');
        setInterval(() => {
            msgEl.style.opacity = 0;
            setTimeout(() => {
                msgIdx = (msgIdx + 1) % msgs.length;
                msgEl.innerText = msgs[msgIdx];
                msgEl.style.opacity = 1;
            }, 500);
        }, 4000);

        // Animated Number Counter on Load
        const targetCount = 127;
        const counterEl = document.getElementById('counter');
        let count = 0;
        const updateCounter = () => {
            if(count < targetCount) {
                count += Math.ceil((targetCount - count) / 10) || 1;
                counterEl.innerText = count;
                setTimeout(updateCounter, 40);
            }
        };
        setTimeout(updateCounter, 600);

        // Floating Hearts on Hover
        const supportBtn = document.getElementById('support-btn');
        supportBtn.addEventListener('mouseenter', () => {
            for(let i=0; i<4; i++) {
                let heart = document.createElement('div');
                heart.className = 'heart';
                heart.innerText = ['+', '*', '·', '°'][Math.floor(Math.random()*4)];
                heart.style.left = 20 + Math.random() * 60 + '%';
                heart.style.bottom = '10px';
                supportBtn.appendChild(heart);
                setTimeout(() => heart.remove(), 1000);
            }
        });

        // 5-Click Easter Egg
        let clicks = 0;
        const coffeeBtn = document.getElementById('coffee-btn');
        const toast = document.getElementById('toast');
        coffeeBtn.addEventListener('click', () => {
            clicks++;
            // Add slight bump feedback on click
            coffeeBtn.style.transform = 'scale(0.9) translateY(-10px)';
            setTimeout(() => coffeeBtn.style.transform = 'none', 150);
            
            if(clicks === 5) {
                toast.style.bottom = '40px';
                setTimeout(() => { toast.style.bottom = '-100px'; clicks = 0; }, 4000);
            }
        });
    </script>
    </body>
    </html>
    """
    
    html_content = html_content.replace('<!-- AVATAR_PLACEHOLDER -->', avatar_html)
    
    # Embed seamlessly into Streamlit while allowing all JS and Animations to execute safely
    components.html(html_content, height=650, scrolling=False)