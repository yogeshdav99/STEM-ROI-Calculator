import streamlit as st
import requests
import math
import numpy as np

def inject_premium_styles(dark_mode: bool = False):
    """Injects the complete Material Design 3 design system."""

    # --- Font Loading (link tag is faster than @import inside <style>) ---
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    # --- Dark mode toggle script ---
    import streamlit.components.v1 as components
    if dark_mode:
        components.html("""<script>window.parent.document.documentElement.setAttribute('data-theme','dark');</script>""", height=0, width=0)
    else:
        components.html("""<script>window.parent.document.documentElement.removeAttribute('data-theme');</script>""", height=0, width=0)

    st.markdown("""
    <style>
        /* ===================================================================
           MATERIAL DESIGN 3 — DESIGN TOKENS (CSS Custom Properties)
           =================================================================== */
        :root {
            /* Primary palette — Google Blue */
            --md-primary: #1a73e8;
            --md-primary-hover: #1557b0;
            --md-primary-container: #d2e3fc;
            --md-on-primary: #ffffff;
            --md-on-primary-container: #062e6f;

            /* Surface & Background */
            --md-surface: #ffffff;
            --md-surface-dim: #f8fafc;
            --md-surface-container: #f1f5f9;
            --md-surface-container-high: #e8ecf1;
            --md-on-surface: #1f1f1f;
            --md-on-surface-variant: #5f6368;

            /* Outline */
            --md-outline: #dadce0;
            --md-outline-variant: #e8eaed;

            /* Status */
            --md-error: #d93025;
            --md-success: #1e8e3e;
            --md-warning: #f9ab00;

            /* Elevation Shadows */
            --md-shadow-1: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
            --md-shadow-2: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.05);
            --md-shadow-3: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.04);

            /* Shape */
            --md-radius: 14px;
            --md-radius-sm: 8px;
            --md-radius-lg: 20px;

            /* Typography */
            --md-font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

            /* Spacing */
            --md-space-xs: 0.25rem;
            --md-space-sm: 0.5rem;
            --md-space-md: 1rem;
            --md-space-lg: 1.5rem;
            --md-space-xl: 2rem;
        }

        /* ===================================================================
           DARK MODE OVERRIDES
           =================================================================== */
        [data-theme="dark"] {
            --md-primary: #8ab4f8;
            --md-primary-hover: #aecbfa;
            --md-primary-container: #1a3a6b;
            --md-on-primary: #062e6f;
            --md-on-primary-container: #d2e3fc;

            --md-surface: #1c1b1f;
            --md-surface-dim: #141218;
            --md-surface-container: #252329;
            --md-surface-container-high: #302e33;
            --md-on-surface: #e6e1e5;
            --md-on-surface-variant: #c4c0c8;

            --md-outline: #49454f;
            --md-outline-variant: #383540;

            --md-shadow-1: 0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.25);
            --md-shadow-2: 0 4px 6px -1px rgba(0,0,0,0.35), 0 2px 4px -2px rgba(0,0,0,0.25);
            --md-shadow-3: 0 10px 15px -3px rgba(0,0,0,0.4), 0 4px 6px -4px rgba(0,0,0,0.3);
        }

        /* Dark mode — Streamlit overrides */
        [data-theme="dark"] [data-testid="stAppViewContainer"],
        [data-theme="dark"] .main,
        [data-theme="dark"] [data-testid="stApp"] {
            background-color: var(--md-surface-dim) !important;
        }
        [data-theme="dark"] section[data-testid="stSidebar"] {
            background-color: var(--md-surface-container) !important;
        }
        [data-theme="dark"] section[data-testid="stSidebar"] * {
            color: var(--md-on-surface) !important;
        }
        [data-theme="dark"] h1, [data-theme="dark"] h2,
        [data-theme="dark"] h3, [data-theme="dark"] h4,
        [data-theme="dark"] h5, [data-theme="dark"] h6,
        [data-theme="dark"] p, [data-theme="dark"] span,
        [data-theme="dark"] label, [data-theme="dark"] div {
            color: var(--md-on-surface) !important;
        }
        [data-theme="dark"] [data-testid="stMetricValue"] > div,
        [data-theme="dark"] [data-testid="stMetricLabel"] label,
        [data-theme="dark"] [data-testid="stMetricDelta"] > div {
            color: var(--md-on-surface) !important;
        }
        [data-theme="dark"] div[data-baseweb="input"] > div,
        [data-theme="dark"] div[data-baseweb="select"] > div {
            background-color: var(--md-surface-container) !important;
            border-color: var(--md-outline) !important;
            color: var(--md-on-surface) !important;
        }
        [data-theme="dark"] div[data-baseweb="input"] > div input,
        [data-theme="dark"] div[data-baseweb="select"] > div input {
            color: var(--md-on-surface) !important;
        }

        /* Button Dark Mode Overrides */
        [data-theme="dark"] div[data-testid="stButton"] button {
            background-color: var(--md-surface-container) !important;
            border-color: var(--md-outline) !important;
            color: var(--md-on-surface) !important;
        }
        [data-theme="dark"] div[data-testid="stButton"] button p {
            color: var(--md-on-surface) !important;
        }
        [data-theme="dark"] div[data-testid="stButton"] button:hover {
            border-color: var(--md-primary) !important;
            color: var(--md-primary) !important;
        }
        [data-theme="dark"] div[data-testid="stButton"] button:hover p {
            color: var(--md-primary) !important;
        }
        [data-theme="dark"] div[data-testid="stButton"] button[kind="primary"] {
            background-color: var(--md-primary) !important;
            color: var(--md-on-primary) !important;
            border-color: var(--md-primary) !important;
        }
        [data-theme="dark"] div[data-testid="stButton"] button[kind="primary"] p {
            color: var(--md-on-primary) !important;
        }

        /* ===================================================================
           BASE TYPOGRAPHY
           =================================================================== */
        html, body, p, h1, h2, h3, h4, h5, h6 {
            font-family: var(--md-font) !important;
            color: var(--md-on-surface);
        }

        h1 {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: var(--md-on-surface) !important;
            letter-spacing: -0.02em !important;
            line-height: 1.2 !important;
        }
        h2 {
            font-size: 1.625rem !important;
            font-weight: 600 !important;
            color: var(--md-on-surface) !important;
            letter-spacing: -0.015em !important;
        }
        h3 {
            font-size: 1.375rem !important;
            font-weight: 600 !important;
            color: var(--md-on-surface-variant) !important;
        }
        h4 {
            font-size: 1.125rem !important;
            font-weight: 600 !important;
            color: var(--md-on-surface-variant) !important;
        }

        /* ===================================================================
           APP LAYOUT
           =================================================================== */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        [data-testid="stAppViewContainer"] {
            background-color: var(--md-surface-dim);
        }

        section[data-testid="stSidebar"] {
            background-color: var(--md-surface) !important;
            border-right: 1px solid var(--md-outline-variant) !important;
        }

        /* Profile Modal Close Button */
        .profile-close-btn div[data-testid="stButton"] button {
            background: transparent !important;
            border: none !important;
            font-size: 1.5rem !important;
            color: var(--md-on-surface-variant) !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin-top: 1rem;
            transition: transform 0.2s ease, color 0.2s ease !important;
        }
        .profile-close-btn div[data-testid="stButton"] button:hover {
            color: var(--md-error) !important;
            transform: scale(1.2) rotate(90deg) !important;
            background: transparent !important;
        }

        /* ===================================================================
           INPUT CONTROLS — Clean & Dense
           =================================================================== */
        [data-testid="stSlider"], [data-testid="stNumberInput"], [data-testid="stSelectbox"] {
            padding-bottom: 0rem !important;
            margin-bottom: -0.5rem !important;
        }
        label {
            font-weight: 500 !important;
            font-size: 0.85rem !important;
            color: var(--md-on-surface-variant) !important;
        }

        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div {
            border-radius: var(--md-radius-sm) !important;
            border: 1px solid var(--md-outline) !important;
            background-color: var(--md-surface) !important;
            color: var(--md-on-surface) !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }
        div[data-baseweb="input"] > div:hover,
        div[data-baseweb="select"] > div:hover {
            border-color: var(--md-on-surface-variant) !important;
        }
        div[data-baseweb="input"] > div:focus-within,
        div[data-baseweb="select"] > div:focus-within {
            border-color: var(--md-primary) !important;
            box-shadow: 0 0 0 2px rgba(26, 115, 232, 0.2) !important;
        }

        /* ===================================================================
           CARDS — Metrics, Containers, Expanders
           =================================================================== */
        [data-testid="stMetric"],
        [data-testid="stVerticalBlockBorderWrapper"],
        [data-testid="stExpander"] {
            padding: 1.25rem;
            background: var(--md-surface) !important;
            border-radius: var(--md-radius) !important;
            box-shadow: var(--md-shadow-1) !important;
            border: 1px solid var(--md-outline-variant) !important;
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease !important;
            max-width: 100%;
            box-sizing: border-box;
            position: relative;
            z-index: 1;
        }
        [data-testid="stMetric"]:hover,
        [data-testid="stVerticalBlockBorderWrapper"]:hover,
        [data-testid="stExpander"]:hover {
            transform: translateY(-3px);
            box-shadow: var(--md-shadow-3) !important;
        }

        /* Metric value sizing */
        [data-testid="stMetricValue"] {
            font-size: clamp(0.9rem, 1.8vw, 1.4rem) !important;
            overflow-wrap: break-word !important;
            word-break: break-word !important;
            max-width: 100% !important;
            font-weight: 700 !important;
        }
        [data-testid="stMetricValue"] > div {
            font-size: clamp(0.9rem, 1.8vw, 1.4rem) !important;
        }

        /* Equal Height Columns */
        [data-testid="column"] > [data-testid="stVerticalBlock"] {
            height: 100%;
        }
        [data-testid="column"] > [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
            height: 100%;
            display: flex;
            flex-direction: column;
        }

        /* ===================================================================
           CONTENT ANIMATIONS — Single-fire, not infinite
           =================================================================== */
        @keyframes mdFadeInUp {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .element-container {
            animation: mdFadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
        }
        
        /* Staggered animation delays for child elements if possible */
        .element-container:nth-child(1) { animation-delay: 0.05s; }
        .element-container:nth-child(2) { animation-delay: 0.1s; }
        .element-container:nth-child(3) { animation-delay: 0.15s; }
        .element-container:nth-child(4) { animation-delay: 0.2s; }
        .element-container:nth-child(5) { animation-delay: 0.25s; }

        [data-testid="stPlotlyChart"] {
            border-radius: var(--md-radius);
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        [data-testid="stPlotlyChart"]:hover {
            transform: scale(1.005);
        }

        [data-testid="stDataFrame"], [data-testid="stTable"] {
            border-radius: var(--md-radius);
            overflow: hidden;
            box-shadow: var(--md-shadow-1);
            transition: box-shadow 0.2s ease;
        }
        [data-testid="stDataFrame"]:hover, [data-testid="stTable"]:hover {
            box-shadow: var(--md-shadow-2);
        }

        /* Result values — smooth opacity transition for live updates */
        [data-testid="stMetricValue"],
        [data-testid="stMetricDelta"] {
            transition: opacity 0.3s ease;
        }

        /* ===================================================================
           HERO SECTION
           =================================================================== */
        .md-hero {
            background: var(--md-surface);
            border: 1px solid var(--md-outline-variant);
            border-radius: var(--md-radius-lg);
            padding: 2.5rem 2rem;
            text-align: center;
            margin-bottom: var(--md-space-lg);
            box-shadow: var(--md-shadow-2);
            position: relative;
            overflow: hidden;
        }
        @keyframes gradientSweep {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .md-hero::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: linear-gradient(270deg, var(--md-primary), #34a853, #fbbc04, #ea4335, var(--md-primary));
            background-size: 200% 200%;
            animation: gradientSweep 4s ease infinite;
            border-radius: var(--md-radius-lg) var(--md-radius-lg) 0 0;
        }
        .md-hero-title {
            font-size: 2.25rem;
            font-weight: 700;
            color: var(--md-on-surface) !important;
            margin: 0.75rem 0 0.5rem 0;
            letter-spacing: -0.02em;
        }
        .md-hero-subtitle {
            font-size: 1.05rem;
            font-weight: 400;
            color: var(--md-on-surface-variant);
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.6;
        }

        /* ===================================================================
           SVG LOGO
           =================================================================== */
        .md-logo {
            display: inline-block;
            width: 64px;
            height: 64px;
            margin-bottom: 0.5rem;
        }
        .md-logo svg {
            width: 100%;
            height: 100%;
        }

        /* ===================================================================
           FEATURE CARDS (Landing Page)
           =================================================================== */
        .feature-card {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.5);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
            border-radius: var(--md-radius);
            padding: 1.5rem;
            text-align: center;
            height: 100%;
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease, border-color 0.3s ease;
        }
        [data-theme="dark"] .feature-card {
            background: rgba(30, 30, 30, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        }
        .feature-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--md-shadow-3);
            border-color: var(--md-primary);
        }
        .feature-icon {
            font-size: 2rem;
            color: var(--md-primary);
            margin-bottom: 0.75rem;
            display: block;
        }
        .feature-title {
            font-size: 1rem;
            font-weight: 600;
            color: var(--md-on-surface);
            margin-bottom: 0.5rem;
        }
        .feature-text {
            font-size: 0.875rem;
            color: var(--md-on-surface-variant);
            line-height: 1.6;
        }

        /* ===================================================================
           QUICK-START ALERT
           =================================================================== */
        .preview-alert {
            background: var(--md-primary-container);
            border-left: 4px solid var(--md-primary);
            border-radius: var(--md-radius-sm);
            padding: 1rem 1.25rem;
            margin-bottom: var(--md-space-lg);
            display: flex;
            align-items: center;
            gap: 1rem;
            transition: transform 0.2s ease;
        }
        .preview-alert:hover { transform: translateX(2px); }
        .preview-icon {
            font-size: 1.25rem;
            background: var(--md-surface);
            width: 44px; height: 44px;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            box-shadow: var(--md-shadow-1);
            flex-shrink: 0;
            color: var(--md-primary);
        }
        .preview-content h4 {
            margin: 0 0 0.25rem 0 !important;
            color: var(--md-on-primary-container) !important;
            font-size: 0.95rem !important;
            font-weight: 700 !important;
        }
        .preview-content p {
            margin: 0 !important;
            color: var(--md-on-primary-container) !important;
            font-size: 0.85rem !important;
            line-height: 1.5 !important;
        }
        .highlight-badge {
            background: var(--md-error);
            color: white;
            padding: 0.1rem 0.45rem;
            border-radius: 4px;
            font-weight: 700;
            font-size: 0.85rem;
            display: inline-block;
        }

        /* ===================================================================
           SIDEBAR — Real-Time Tracker Card
           =================================================================== */
        .md-tracker-card {
            background: rgba(210, 227, 252, 0.5);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: var(--md-radius);
            padding: 1rem 1.25rem;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 4px 16px 0 rgba(31, 38, 135, 0.05);
        }
        [data-theme="dark"] .md-tracker-card {
            background: rgba(26, 58, 107, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .md-tracker-card h4 {
            font-size: 0.75rem !important;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--md-on-primary-container) !important;
            font-weight: 600 !important;
            margin-bottom: 0.5rem !important;
        }
        .md-tracker-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--md-primary);
        }

        /* ===================================================================
           STICKY FOOTER NAVIGATION
           =================================================================== */
        .sticky-footer-wrapper {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-top: 1px solid var(--md-outline-variant);
            padding: 1rem 2rem;
            z-index: 999;
            box-shadow: 0 -4px 20px rgba(0,0,0,0.05);
            display: flex;
            justify-content: center;
        }
        [data-theme="dark"] .sticky-footer-wrapper {
            background: rgba(28, 27, 31, 0.85);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 -4px 20px rgba(0,0,0,0.4);
        }
        /* Make sure main content doesn't get hidden behind footer */
        [data-testid="stAppViewContainer"] {
            padding-bottom: 80px;
        }

        /* ===================================================================
           DYNAMIC BACKGROUND MESH
           =================================================================== */
        .main {
            background-color: var(--md-surface-dim);
            background-image: 
                radial-gradient(at 0% 0%, rgba(26, 115, 232, 0.03) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(217, 48, 37, 0.02) 0px, transparent 50%);
            background-attachment: fixed;
            background-size: cover;
        }
        [data-theme="dark"] .main {
            background-image: 
                radial-gradient(at 0% 0%, rgba(138, 180, 248, 0.05) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(242, 139, 130, 0.03) 0px, transparent 50%);
        }    
        .md-tracker-value {
            font-variant-numeric: tabular-nums;
        }
        .md-tracker-label {
            font-size: 0.8rem;
            color: var(--md-on-surface-variant);
            margin-top: 0.25rem;
        }

        /* ===================================================================
           PRIMARY BUTTONS — Clean, no infinite pulse
           =================================================================== */
        [data-testid="baseButton-primary"] {
            background-color: var(--md-primary) !important;
            border-color: var(--md-primary) !important;
            color: var(--md-on-primary) !important;
            border-radius: var(--md-radius-sm) !important;
            font-weight: 600 !important;
            transition: background-color 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease !important;
        }
        [data-testid="baseButton-primary"]:hover {
            background-color: var(--md-primary-hover) !important;
            border-color: var(--md-primary-hover) !important;
            transform: translateY(-1px) !important;
            box-shadow: var(--md-shadow-2) !important;
        }
        [data-testid="baseButton-primary"]:active {
            transform: translateY(0) !important;
        }

        /* ===================================================================
           PROGRESS BAR
           =================================================================== */
        [data-testid="stProgress"] > div > div > div > div {
            background: linear-gradient(90deg, var(--md-primary), #34a853) !important;
            border-radius: 4px;
            transition: width 0.4s ease;
        }

        /* ===================================================================
           NAVIGATION BAR — Sticky Material Pills
           =================================================================== */
        div.element-container:has(.top-nav-anchor) + div.element-container {
            position: sticky;
            top: 2.875rem;
            z-index: 999;
        }

        div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] {
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            background-color: var(--md-surface);
            border: 1px solid var(--md-outline);
            border-radius: var(--md-radius);
            padding: 0.35rem;
            margin-bottom: var(--md-space-md);
            box-shadow: var(--md-shadow-2);
            gap: 0.25rem;
        }

        div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] > label {
            background-color: transparent;
            border: none;
            border-radius: var(--md-radius-sm);
            padding: 0.55rem 0.75rem;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: none;
            flex: 1;
            margin: 0;
        }

        /* Hide default radio circle */
        div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
            display: none;
        }

        /* Nav text */
        div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] > label p {
            margin: 0;
            font-size: 0.875rem;
            font-weight: 500;
            color: var(--md-on-surface-variant);
            z-index: 2;
            transition: color 0.2s ease;
            white-space: nowrap;
        }

        /* Hover */
        div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
            background-color: var(--md-surface-container);
        }
        div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] > label:hover p {
            color: var(--md-on-surface);
        }

        /* Active tab */
        div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
            background-color: var(--md-primary);
            box-shadow: var(--md-shadow-1);
        }
        div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) p {
            color: var(--md-on-primary) !important;
            font-weight: 600;
        }

        /* ===================================================================
           LOCKED TASK INDICATOR
           =================================================================== */
        .md-locked-task {
            text-align: center;
            padding: 3rem 2rem;
            color: var(--md-on-surface-variant);
        }
        .md-locked-task i {
            font-size: 2.5rem;
            color: var(--md-outline);
            margin-bottom: 1rem;
            display: block;
        }
        .md-locked-task h3 {
            font-size: 1.25rem !important;
            font-weight: 600 !important;
            color: var(--md-on-surface-variant) !important;
            margin-bottom: 0.5rem;
        }
        .md-locked-task p {
            font-size: 0.9rem;
            color: var(--md-on-surface-variant);
        }

        /* ===================================================================
           STEP INDICATOR CHIPS
           =================================================================== */
        .md-step-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.3rem 0.75rem;
            border-radius: 100px;
            font-size: 0.8rem;
            font-weight: 500;
            background: var(--md-surface-container);
            color: var(--md-on-surface-variant);
            border: 1px solid var(--md-outline-variant);
        }
        .md-step-chip.active {
            background: var(--md-primary-container);
            color: var(--md-on-primary-container);
            border-color: var(--md-primary);
        }

        /* ===================================================================
           MOBILE RESPONSIVE (< 768px)
           =================================================================== */
        @media (max-width: 768px) {
            .block-container {
                padding-top: 1rem;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }

            /* Stack nav vertically on mobile */
            div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] {
                flex-direction: column;
                gap: 0.2rem;
            }
            div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] > label {
                padding: 0.5rem 0.75rem;
            }
            div.element-container:has(.top-nav-anchor) + div.element-container [data-testid="stRadio"] > div[role="radiogroup"] > label p {
                font-size: 0.8rem;
            }

            .md-hero {
                padding: 1.5rem 1rem;
            }
            .md-hero-title {
                font-size: 1.625rem;
            }

            h1 { font-size: 1.5rem !important; }
            h2 { font-size: 1.25rem !important; }
            h3 { font-size: 1.125rem !important; }

            .feature-card {
                padding: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

BASE_USD_RANGES = {
    "tuition": {"min": 10_000, "max": 100_000, "default": 40_000, "step": 1_000},
    "living": {"min": 5_000, "max": 50_000, "default": 20_000, "step": 500},
    "salary": {"min": 0, "max": 200_000, "default": 50_000, "step": 5_000},
}

STEM_DEGREES = [
    "Aerospace Engineering", "Architecture", "Artificial Intelligence", "Bioinformatics", 
    "Biomedical Engineering", "Business Analytics", "Chemical Engineering", "Civil Engineering", 
    "Computer Engineering", "Computer Science", "Cybersecurity", "Data Science", 
    "Electrical Engineering", "Environmental Science", "Industrial Engineering", 
    "Information Systems", "Information Technology", "Machine Learning", "Mathematics", 
    "Mechanical Engineering", "Mechatronics", "Physics", "Robotics", "Software Engineering", 
    "Statistics", "Urban Planning"
]

STEM_JOBS = [
    "Aerospace Engineer", "AI Engineer", "Architect", "Bioinformatician", 
    "Biomedical Engineer", "Business Analyst", "Chemical Engineer", "Civil Engineer", 
    "Cloud Architect", "Data Analyst", "Data Engineer", "Data Scientist", 
    "DevOps Engineer", "Electrical Engineer", "Environmental Engineer", 
    "Flight Dynamics Engineer", "Full Stack Developer", "Industrial Engineer", 
    "IT Consultant", "Machine Learning Engineer", "Mechanical Engineer", 
    "Mechatronics Engineer", "Product Manager", "Quantitative Analyst", 
    "Robotics Engineer", "Software Engineer", "Systems Analyst", "Urban Planner"
]

DEGREE_JOB_MAPPING = {
    "Aerospace Engineering": ["Aerospace Engineer", "Flight Dynamics Engineer"],
    "Architecture": ["Architect", "Urban Planner"],
    "Artificial Intelligence": ["AI Engineer", "Machine Learning Engineer", "Data Scientist", "Software Engineer"],
    "Bioinformatics": ["Bioinformatician", "Data Scientist"],
    "Biomedical Engineering": ["Biomedical Engineer"],
    "Business Analytics": ["Business Analyst", "Data Analyst", "Data Scientist", "Product Manager", "Systems Analyst", "Quantitative Analyst"],
    "Chemical Engineering": ["Chemical Engineer"],
    "Civil Engineering": ["Civil Engineer", "Urban Planner"],
    "Computer Engineering": ["Software Engineer", "Cloud Architect", "DevOps Engineer", "Electrical Engineer"],
    "Computer Science": ["Software Engineer", "Full Stack Developer", "Cloud Architect", "DevOps Engineer", "AI Engineer", "Data Scientist"],
    "Cybersecurity": ["Software Engineer", "Cloud Architect"],
    "Data Science": ["Data Scientist", "Data Analyst", "Data Engineer", "Machine Learning Engineer", "AI Engineer"],
    "Electrical Engineering": ["Electrical Engineer", "Robotics Engineer", "Mechatronics Engineer"],
    "Environmental Science": ["Environmental Engineer", "Civil Engineer"],
    "Industrial Engineering": ["Industrial Engineer", "Product Manager", "Systems Analyst"],
    "Information Systems": ["Systems Analyst", "IT Consultant", "Business Analyst", "Cloud Architect"],
    "Information Technology": ["IT Consultant", "Systems Analyst", "DevOps Engineer", "Cloud Architect"],
    "Machine Learning": ["Machine Learning Engineer", "AI Engineer", "Data Scientist", "Software Engineer"],
    "Mathematics": ["Quantitative Analyst", "Data Scientist", "Data Analyst", "Machine Learning Engineer"],
    "Mechanical Engineering": ["Mechanical Engineer", "Aerospace Engineer", "Robotics Engineer", "Mechatronics Engineer"],
    "Mechatronics": ["Mechatronics Engineer", "Robotics Engineer", "Electrical Engineer", "Mechanical Engineer"],
    "Physics": ["Quantitative Analyst", "Data Scientist", "Aerospace Engineer"],
    "Robotics": ["Robotics Engineer", "Mechatronics Engineer", "AI Engineer"],
    "Software Engineering": ["Software Engineer", "Full Stack Developer", "Cloud Architect", "DevOps Engineer"],
    "Statistics": ["Data Analyst", "Data Scientist", "Quantitative Analyst", "Machine Learning Engineer"],
    "Urban Planning": ["Urban Planner", "Architect", "Civil Engineer"]
}

def calculate_opportunity_cost(current_salary: float, growth_rate_pct: float, duration: float) -> float:
    """Calculates foregone income over the study period, factoring in expected annual raises."""
    if current_salary <= 0 or duration <= 0:
        return 0.0
        
    salary_growth_rate = growth_rate_pct / 100.0
    total_lost_income = 0.0
    
    full_years = int(duration)
    for year in range(full_years):
        total_lost_income += current_salary * ((1 + salary_growth_rate) ** year)
        
    fraction = duration - full_years
    if fraction > 0:
        total_lost_income += (current_salary * ((1 + salary_growth_rate) ** full_years)) * fraction
        
    return total_lost_income

def calculate_capitalized_principal(total_loan: float, annual_rate: float, program_duration: float, grace_months: int) -> tuple[float, float]:
    """Simulates monthly interest compounding during the study and grace periods."""
    if total_loan <= 0:
        return 0.0, 0.0
        
    monthly_rate = annual_rate / 100.0 / 12.0
    study_months = int(program_duration * 12)
    total_moratorium_months = study_months + grace_months
    
    num_disbursements = math.ceil(program_duration)
    disbursement_amount = total_loan / num_disbursements
    
    principal_balance = 0.0
    accrued_simple_interest = 0.0
    
    for month in range(1, total_moratorium_months + 1):
        if month <= study_months and (month - 1) % 12 == 0:
            principal_balance += disbursement_amount
            
        accrued_simple_interest += principal_balance * monthly_rate
        
    total_capitalized_balance = principal_balance + accrued_simple_interest
    return total_capitalized_balance, accrued_simple_interest

def calculate_amortization(principal: float, annual_rate: float, months: int = 120, shock_month: int = 36, shock_rate_increase: float = 2.0, custom_payment: float = 0.0):
    """Calculates amortization schedules. Handles both standard 10-year terms and custom monthly payments."""
    if principal <= 0:
        return 0.0, 0.0, 0.0, [0.0], [0.0]

    monthly_rate = annual_rate / 100.0 / 12.0

    if monthly_rate > 0:
        standard_payment = principal * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
    else: 
        standard_payment = principal / months
        
    actual_payment = custom_payment if custom_payment > 0 else standard_payment
    
    if actual_payment <= principal * monthly_rate and custom_payment > 0:
        return actual_payment, float('inf'), float('inf'), [principal] * 120, [principal] * 120
        
    baseline_history = []
    balance = principal
    total_baseline_interest = 0.0
    max_sim_months = 360 if custom_payment > 0 else months
    
    for _ in range(max_sim_months + 1):
        baseline_history.append(balance)
        if balance <= 0:
            break
        interest = balance * monthly_rate
        total_baseline_interest += interest
        payment = min(actual_payment, balance + interest)
        balance -= (payment - interest)

    shock_history = []
    balance = principal
    total_shock_interest = 0.0
    shocked_annual_rate = annual_rate + shock_rate_increase
    shocked_monthly_rate = shocked_annual_rate / 100.0 / 12.0
    
    for m in range(max_sim_months + 1):
        shock_history.append(balance)
        if balance <= 0:
            break
            
        if m < shock_month:
            interest = balance * monthly_rate
            total_shock_interest += interest
            payment = min(actual_payment, balance + interest)
            balance -= (payment - interest)
        else:
            interest = balance * shocked_monthly_rate
            total_shock_interest += interest
            if custom_payment > 0:
                payment = min(actual_payment, balance + interest)
            else:
                remaining_months_at_shock = months - shock_month
                if shocked_monthly_rate > 0 and remaining_months_at_shock > 0:
                    shocked_payment = balance * (shocked_monthly_rate * (1 + shocked_monthly_rate)**remaining_months_at_shock) / ((1 + shocked_monthly_rate)**remaining_months_at_shock - 1)
                else:
                    shocked_payment = balance / remaining_months_at_shock if remaining_months_at_shock > 0 else balance + interest
                payment = min(shocked_payment, balance + interest)
            balance -= (payment - interest)

    extra_interest = max(0.0, total_shock_interest - total_baseline_interest)
    return actual_payment, total_baseline_interest, extra_interest, baseline_history, shock_history

def calculate_irr(cash_flows: list[float], iterations: int = 100) -> float:
    """Calculates Internal Rate of Return (IRR) using the bisection method to find where NPV = 0."""
    low, high = -0.99, 1.0
    for _ in range(iterations):
        mid = (low + high) / 2
        npv = sum(cf / ((1 + mid) ** t) for t, cf in enumerate(cash_flows))
        if npv > 0:
            low = mid
        else:
            high = mid
    return mid * 100

def calculate_roi_metrics(starting_salary: float, growth_rate: float, discount_rate: float, year_0_cost: float, years: int = 10) -> tuple[float, int, list[float]]:
    """Projects 10-year cash flows, Net Present Value (NPV), and Break-Even point."""
    cash_flows = [-year_0_cost]
    current_salary = starting_salary
    cumulative_earnings = 0.0
    break_even_year = None
    
    for year in range(1, years + 1):
        cash_flows.append(current_salary)
        cumulative_earnings += current_salary
        if break_even_year is None and cumulative_earnings >= year_0_cost:
            break_even_year = year
        current_salary *= (1 + (growth_rate / 100.0))
        
    npv = sum(cf / ((1 + (discount_rate / 100.0)) ** t) for t, cf in enumerate(cash_flows))
    return npv, break_even_year, cash_flows

def run_monte_carlo_roi(starting_salary: float, growth_rate: float, discount_rate: float, year_0_cost: float, iterations: int = 1000) -> dict:
    """Runs a Monte Carlo simulation using normal distributions to measure ROI risk."""
    # Vectorized operations for ~100x performance boost
    sim_salary = np.random.normal(starting_salary, starting_salary * 0.10, iterations)
    sim_growth = np.random.normal(growth_rate, 1.5, iterations)
    
    npvs = np.full(iterations, -year_0_cost, dtype=float)
    
    for t in range(1, 11):
        cf = sim_salary * ((1 + sim_growth / 100.0) ** (t - 1))
        npvs += cf / ((1 + discount_rate / 100.0) ** t)
        
    return {
        "npvs": npvs,
        "prob_positive": (npvs > 0).mean() * 100,
        "mean_npv": npvs.mean(),
        "worst_case_5th": np.percentile(npvs, 5),
        "best_case_95th": np.percentile(npvs, 95)
    }

def round_to_nearest(value: float, nearest: int) -> int:
    if nearest <= 0: return int(round(value))
    return int(round(value / nearest) * nearest)

def build_currency_config(symbol: str, exchange_rate: float, rounding: dict[str, int]) -> dict[str, dict[str, int] | str | float]:
    config = {"symbol": symbol, "exchange_rate": exchange_rate, "tuition": {}, "living": {}, "salary": {}}
    for key, base_values in BASE_USD_RANGES.items():
        nearest = rounding[key]
        config[key] = {
            "min": round_to_nearest(base_values["min"] * exchange_rate, nearest),
            "max": round_to_nearest(base_values["max"] * exchange_rate, nearest),
            "default": round_to_nearest(base_values["default"] * exchange_rate, nearest),
            "step": max(nearest, round_to_nearest(base_values["step"] * exchange_rate, nearest)),
        }
    return config

@st.cache_data(ttl=86_400)
def fetch_live_exchange_rates() -> dict:
    import json
    import os
    cache_file = "rates_cache.json"

    fallbacks = {
        "_last_updated": "Offline (Using Hardcoded Fallbacks)",
        "USD": 1.0, "INR": 83.5, "NZD": 1.65, "EUR": 0.92, "GBP": 0.79,
        "PKR": 278.0, "JPY": 150.0, "CNY": 7.2, "KRW": 1350.0,
        "SAR": 3.75, "MYR": 4.7, "VND": 25000.0, "IRR": 42000.0
    }
    
    # Try to load cached rates from a previous successful API call
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                cached_rates = json.load(f)
                cached_rates["_last_updated"] = f"Offline (Last fetched: {cached_rates.get('_last_updated', 'Unknown')})"
                fallbacks = cached_rates
        except Exception:
            pass

    try:
        response = requests.get("https://api.frankfurter.dev/v1/latest?base=USD", timeout=1.5)
        response.raise_for_status()
        data = response.json()
        rates = data.get("rates", {})
        
        latest_rates = {
            "_last_updated": data.get("date", "Recently"),
            "USD": 1.0, 
            "INR": rates.get("INR", fallbacks["INR"]), 
            "NZD": rates.get("NZD", fallbacks["NZD"]), 
            "EUR": rates.get("EUR", fallbacks["EUR"]), 
            "GBP": rates.get("GBP", fallbacks["GBP"]),
            "PKR": rates.get("PKR", fallbacks["PKR"]),
            "JPY": rates.get("JPY", fallbacks["JPY"]),
            "CNY": rates.get("CNY", fallbacks["CNY"]),
            "KRW": rates.get("KRW", fallbacks["KRW"]),
            "SAR": rates.get("SAR", fallbacks["SAR"]),
            "MYR": rates.get("MYR", fallbacks["MYR"]),
            "VND": rates.get("VND", fallbacks["VND"]),
            "IRR": rates.get("IRR", fallbacks["IRR"])
        }
        
        # Save to file for future fallback
        try:
            # We save the exact dictionary fetched, so next time it's used as fallback
            save_data = latest_rates.copy()
            save_data["_last_updated"] = save_data["_last_updated"]
            with open(cache_file, "w") as f:
                json.dump(save_data, f)
        except Exception:
            pass
            
        return latest_rates
    except Exception:
        return fallbacks

LIVE_RATES = fetch_live_exchange_rates()
CURRENCY_CONFIGS = {
    "USD ($)": build_currency_config("$", LIVE_RATES["USD"], {"tuition": 1_000, "living": 500, "salary": 5_000}), 
    "INR (₹)": build_currency_config("₹", LIVE_RATES["INR"], {"tuition": 50_000, "living": 25_000, "salary": 100_000}), 
    "NZD (NZ$)": build_currency_config("NZ$", LIVE_RATES["NZD"], {"tuition": 1_000, "living": 500, "salary": 5_000}), 
    "EUR (€)": build_currency_config("€", LIVE_RATES["EUR"], {"tuition": 1_000, "living": 500, "salary": 2_000}), 
    "GBP (£)": build_currency_config("£", LIVE_RATES["GBP"], {"tuition": 1_000, "living": 500, "salary": 2_000}),
    "PKR (₨)": build_currency_config("₨", LIVE_RATES["PKR"], {"tuition": 100_000, "living": 50_000, "salary": 200_000}),
    "JPY (¥)": build_currency_config("¥", LIVE_RATES["JPY"], {"tuition": 100_000, "living": 50_000, "salary": 100_000}),
    "CNY (¥)": build_currency_config("¥", LIVE_RATES["CNY"], {"tuition": 10_000, "living": 5_000, "salary": 10_000}),
    "KRW (₩)": build_currency_config("₩", LIVE_RATES["KRW"], {"tuition": 1_000_000, "living": 500_000, "salary": 2_000_000}),
    "SAR (﷼)": build_currency_config("﷼", LIVE_RATES["SAR"], {"tuition": 5_000, "living": 2_500, "salary": 10_000}),
    "MYR (RM)": build_currency_config("RM", LIVE_RATES["MYR"], {"tuition": 5_000, "living": 2_500, "salary": 10_000}),
    "VND (₫)": build_currency_config("₫", LIVE_RATES["VND"], {"tuition": 10_000_000, "living": 5_000_000, "salary": 20_000_000}),
    "IRR (﷼)": build_currency_config("﷼", LIVE_RATES["IRR"], {"tuition": 10_000_000, "living": 5_000_000, "salary": 20_000_000})
}
def local_to_usd(amount: float, exchange_rate: float) -> float: 
    if exchange_rate <= 0: return amount # Prevent ZeroDivisionError fallback
    return amount / exchange_rate
def format_currency_markdown(symbol: str, amount: float) -> str: return f"{symbol.replace('$', r'\$')}{amount:,.0f}"