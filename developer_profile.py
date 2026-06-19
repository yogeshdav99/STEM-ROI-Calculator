import streamlit as st
import streamlit.components.v1 as components
import base64
import os

def render():
    """
    Renders the modern, premium 'Cyberpunk/FinTech' developer profile card.
    """
    
    avatar_html = '<div class="avatar-img"><i class="fas fa-user-astronaut"></i></div>'
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
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --accent-primary: #ffffff;
            --accent-secondary: #94a3b8;
            --accent-glow: rgba(255, 255, 255, 0.15);
            --dark-bg: #0b0f19;
            --glass-bg: rgba(15, 23, 42, 0.65);
            --text-main: #f8fafc;
            --text-muted: #cbd5e1;
        }

        body {
            margin: 0;
            padding: 2rem;
            font-family: 'Inter', -apple-system, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            background: transparent;
            overflow: hidden;
            perspective: 1200px;
        }

        /* Animated Background Studio Lighting */
        .bg-orbs {
            position: absolute;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }
        .orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.25;
            animation: floatOrb 12s infinite alternate ease-in-out;
        }
        .orb-1 { width: 400px; height: 400px; background: #3b82f6; top: -100px; left: -100px; animation-delay: 0s; }
        .orb-2 { width: 350px; height: 350px; background: #64748b; bottom: -100px; right: -100px; animation-delay: -6s; }

        @keyframes floatOrb {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(30px, 30px) scale(1.1); }
        }

        /* 3D Glass Card Container */
        .card-wrapper {
            position: relative;
            width: 100%;
            max-width: 450px;
            border-radius: 24px;
            /* Premium Metallic Gradient Border */
            background: linear-gradient(60deg, rgba(255,255,255,0.05), rgba(255,255,255,0.3), rgba(255,255,255,0.05), rgba(255,255,255,0.2));
            background-size: 300% 300%;
            animation: gradientSpin 6s ease infinite;
            padding: 1px; /* Super thin elite border */
            transition: transform 0.1s ease;
            transform-style: preserve-3d;
        }

        @keyframes gradientSpin {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .glass-card {
            background: var(--glass-bg);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border-radius: 23px;
            padding: 3rem 2.5rem;
            text-align: center;
            color: var(--text-main);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.1), 0 20px 40px -10px rgba(0,0,0,0.4);
            transform: translateZ(40px); /* Lifts content above card */
        }

        /* Avatar */
        .avatar-container {
            position: relative;
            width: 130px;
            height: 130px;
            margin: 0 auto 1.5rem;
            border-radius: 50%;
            padding: 3px;
            background: linear-gradient(135deg, rgba(255,255,255,0.4), rgba(255,255,255,0.05));
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease;
        }
        
        .avatar-container:hover {
            transform: scale(1.05);
        }

        .avatar-img {
            width: 100%; height: 100%;
            border-radius: 50%;
            background: #0f172a;
            display: flex; align-items: center; justify-content: center;
            font-size: 3.5rem; color: var(--accent-primary);
        }

        /* Typography */
        h2.name {
            font-size: 2.2rem;
            font-weight: 700;
            margin: 0;
            color: var(--accent-primary);
            letter-spacing: -0.5px;
        }
        p.title {
            font-size: 1rem;
            color: var(--accent-secondary);
            font-weight: 500;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-top: 0.5rem;
            margin-bottom: 1.5rem;
        }
        p.bio {
            font-size: 0.95rem;
            color: var(--text-muted);
            line-height: 1.6;
            margin-bottom: 2.5rem;
            font-weight: 300;
        }

        /* Social Icons */
        .social-links {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }
        .social-btn {
            color: var(--text-muted);
            font-size: 1.3rem;
            text-decoration: none;
            transition: all 0.3s ease;
            position: relative;
            padding: 0.5rem;
        }
        .social-btn:hover {
            color: var(--accent-primary);
            transform: translateY(-3px);
        }

        /* Interactive Coffee Button */
        .coffee-btn {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-main);
            padding: 1rem 2rem;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 30px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
            width: 100%;
            position: relative;
            overflow: hidden;
            z-index: 1;
        }
        
        .coffee-btn::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            transition: all 0.5s ease;
            z-index: -1;
        }

        .coffee-btn:hover {
            border-color: rgba(255,255,255,0.4);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            transform: scale(1.02);
            background: rgba(255, 255, 255, 0.1);
        }
        .coffee-btn:hover::before {
            left: 100%;
        }
        .coffee-btn:hover i {
            color: var(--accent-primary);
        }

        @keyframes shake {
            0%, 100% { transform: rotate(0deg); }
            25% { transform: rotate(-10deg); }
            75% { transform: rotate(10deg); }
        }

    </style>
    </head>
    <body>

    <div class="bg-orbs">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
    </div>

    <div class="card-wrapper" id="tilt-card">
        <div class="glass-card">
            <div class="avatar-container">
                <!-- AVATAR_PLACEHOLDER -->
            </div>
            
            <h2 class="name">Yogesh Patel</h2>
            <p class="title">BI Analyst & Creator</p>
            <p class="bio">Building tools to help global students navigate the complex world of international education finance. Data-driven clarity, zero BS.</p>
            
            <div class="social-links">
                <a href="https://linkedin.com/in/yogesh-patel-842376158" target="_blank" class="social-btn"><i class="fab fa-linkedin-in"></i></a>
                <a href="https://portfolio-ashy-theta-24.vercel.app/" target="_blank" class="social-btn"><i class="fas fa-globe"></i></a>
                <a href="mailto:yogesh.dav99@gmail.com" class="social-btn"><i class="fas fa-envelope"></i></a>
            </div>

            <button class="coffee-btn" onclick="window.open('https://buymeacoffee.com/yogeshpatel', '_blank')">
                <i class="fas fa-mug-hot"></i> Fuel the Next Feature
            </button>
        </div>
    </div>

    <script>
        // 3D Tilt Effect
        const card = document.getElementById('tilt-card');
        const body = document.body;

        body.addEventListener('mousemove', (e) => {
            const xAxis = (window.innerWidth / 2 - e.pageX) / 25;
            const yAxis = (window.innerHeight / 2 - e.pageY) / 25;
            card.style.transform = `rotateY(${xAxis}deg) rotateX(${yAxis}deg)`;
        });

        // Reset transform on mouse leave
        body.addEventListener('mouseleave', () => {
            card.style.transition = 'transform 0.5s ease';
            card.style.transform = `rotateY(0deg) rotateX(0deg)`;
            setTimeout(() => card.style.transition = 'transform 0.1s ease', 500);
        });
    </script>

    </body>
    </html>
    """
    
    html_content = html_content.replace('<!-- AVATAR_PLACEHOLDER -->', avatar_html)
    
    components.html(html_content, height=650)